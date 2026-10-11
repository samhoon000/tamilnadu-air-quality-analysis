"""
Test Suite for Tamil Nadu Air Quality Analytics Pipeline.

Validates core requirements:
- Column standardization and canonical mapping
- Date parsing across formats without record dropping
- Numeric conversion preserving genuine missingness (no zero imputation)
- Missing column handling (e.g. unmonitored PM2.5 in historical years)
- Duplicate detection (exact rows and station-date keys)
- Negative pollutant detection
- Multi-file ingestion and data_year creation
"""

import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.ingestion import extract_year_from_filename, read_raw_file, discover_raw_files
from src.standardization import standardize_schema, map_columns_to_canonical, CANONICAL_COLUMNS
from src.cleaning import (
    clean_text_columns,
    parse_dates_robustly,
    convert_numeric_pollutants,
    detect_duplicates,
    detect_negative_pollutants,
    clean_dataset
)


def test_year_extraction_from_filename():
    assert extract_year_from_filename("air_quality_2011.csv") == 2011
    assert extract_year_from_filename("2015.csv") == 2015
    assert extract_year_from_filename("cpcb_tn_2014_daily.csv") == 2014
    assert extract_year_from_filename("random_file.csv") is None


def test_column_standardization_and_canonical_mapping():
    raw_cols = [
        "Station Code",
        "Sampling Date",
        "State",
        "City/Town/Village/Area",
        "Location of Monitoring Station",
        "Agency",
        "Type of Location",
        "SO2",
        "NO2",
        "RSPM/PM10"
    ]
    mapping, unmapped = map_columns_to_canonical(raw_cols)
    assert mapping["Station Code"] == "stn_code"
    assert mapping["Sampling Date"] == "sampling_date"
    assert mapping["RSPM/PM10"] == "rspm_pm10"
    assert len(unmapped) == 0


def test_missing_column_handling_does_not_fill_zero():
    # Simulate older dataset missing PM 2.5
    df_raw = pd.DataFrame({
        "stn_code": [38, 39],
        "sampling_date": ["2011-01-05", "2011-01-08"],
        "so2": [10.5, 12.0],
        "no2": [22.0, 24.5],
        "rspm_pm10": [55.0, 60.0]
    })
    
    std_df, report = standardize_schema(df_raw)
    
    # pm_2_5 must exist in canonical schema
    assert "pm_2_5" in std_df.columns
    # Must be NaN / missing, NEVER zero
    assert std_df["pm_2_5"].isna().all()
    assert (std_df["pm_2_5"] == 0).sum() == 0
    assert "pm_2_5" in report["missing_canonical_columns"]


def test_date_conversion_multiple_formats():
    # Test DD-MM-YY, DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY
    dates = pd.Series([
        "06-01-15",
        "06/01/2011",
        "2012-05-18",
        "15-08-2013",
        "invalid_date_str"
    ])
    parsed, invalid_count = parse_dates_robustly(dates)
    
    assert invalid_count == 1
    assert parsed.iloc[0] == pd.Timestamp("2015-01-06")
    assert parsed.iloc[1] == pd.Timestamp("2011-01-06")
    assert parsed.iloc[2] == pd.Timestamp("2012-05-18")
    assert parsed.iloc[3] == pd.Timestamp("2013-08-15")
    assert pd.isna(parsed.iloc[4])


def test_numeric_pollutant_conversion_preserves_missingness():
    df = pd.DataFrame({
        "so2": ["10.5", "NA", "", "22.3"],
        "no2": ["18.0", None, "invalid", "25.0"],
        "rspm_pm10": ["50", "60", "70", "80"],
        "pm_2_5": [np.nan, "NA", "30.5", ""]
    })
    cleaned_df, non_numeric = convert_numeric_pollutants(df)
    
    # Validate types
    assert pd.api.types.is_float_dtype(cleaned_df["so2"])
    assert pd.api.types.is_float_dtype(cleaned_df["no2"])
    
    # Missingness preserved (not 0)
    assert cleaned_df["so2"].isna().sum() == 2
    assert (cleaned_df["so2"] == 0).sum() == 0
    assert cleaned_df["pm_2_5"].isna().sum() == 3
    assert (cleaned_df["pm_2_5"] == 0).sum() == 0


def test_duplicate_detection():
    df = pd.DataFrame({
        "stn_code": [38, 38, 38],
        "sampling_date": ["2015-01-02", "2015-01-02", "2015-01-03"],
        "location_of_monitoring_station": ["Loc A", "Loc A", "Loc A"],
        "so2": [10.0, 10.0, 12.0]
    })
    exact_dups, station_date_dups = detect_duplicates(df)
    assert exact_dups == 1
    assert station_date_dups == 1


def test_negative_pollutant_detection():
    df = pd.DataFrame({
        "so2": [10.0, -5.0, 15.0],
        "no2": [20.0, 22.0, -1.0],
        "rspm_pm10": [50.0, 55.0, 60.0],
        "pm_2_5": [np.nan, np.nan, np.nan]
    })
    neg = detect_negative_pollutants(df)
    assert neg["so2"] == 1
    assert neg["no2"] == 1
    assert neg["rspm_pm10"] == 0


def test_multi_file_ingestion_and_data_year_creation():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create mock 2011 and 2012 files
        p1 = Path(tmpdir) / "air_quality_2011.csv"
        p2 = Path(tmpdir) / "air_quality_2012.csv"
        
        pd.DataFrame({
            "Station Code": [38],
            "Sampling Date": ["05/01/2011"],
            "SO2": [10.0]
        }).to_csv(p1, index=False)
        
        pd.DataFrame({
            "stn_code": [39],
            "sampling_date": ["2012-01-08"],
            "so2": [12.0]
        }).to_csv(p2, index=False)
        
        files = discover_raw_files(tmpdir)
        assert len(files) == 2
        
        df1 = read_raw_file(files[0])
        df2 = read_raw_file(files[1])
        
        assert df1["data_year"].iloc[0] == 2011
        assert df1["source_file"].iloc[0] == "air_quality_2011.csv"
        assert df2["data_year"].iloc[0] == 2012
        assert df2["source_file"].iloc[0] == "air_quality_2012.csv"
