"""
Data Cleaning Layer for Tamil Nadu Air Quality Analytics Pipeline.

Converts cleaning logic from exploratory analysis into production-quality,
reusable functions:
- Text trimming & blank normalization
- Robust multi-format date parsing (no silent record loss)
- Safe numeric pollutant conversion (preserves genuine missingness, never 0-imputed)
- Exact and key duplicate detection
- Negative pollutant concentration detection & flagging
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


POLLUTANT_COLUMNS = ["so2", "no2", "rspm_pm10", "pm_2_5"]
TEXT_COLUMNS = [
    "state",
    "city_town_village_area",
    "location_of_monitoring_station",
    "agency",
    "type_of_location"
]


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans text columns by trimming whitespace and normalizing
    empty strings or missing place-holders ('', 'NA', 'N/A', '-') to NaN.
    Also standardizes station code representation.
    """
    df_clean = df.copy()
    
    # Clean station code as clean string without decimal artifact
    if "stn_code" in df_clean.columns:
        df_clean["stn_code"] = (
            df_clean["stn_code"]
            .astype(str)
            .str.strip()
            .replace(["nan", "NaN", "None", ""], np.nan)
        )
        # remove trailing '.0' if parsed as float initially
        df_clean["stn_code"] = df_clean["stn_code"].apply(
            lambda x: str(int(float(x))) if pd.notna(x) and x.replace(".", "", 1).isdigit() and "." in x else x
        )
        
    for col in TEXT_COLUMNS:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace(
                ["nan", "NaN", "None", "", "NA", "N/A", "null", "NULL", "-"],
                np.nan
            )
            
    return df_clean


def parse_dates_robustly(date_series: pd.Series) -> Tuple[pd.Series, int]:
    """
    Parses dates across various Indian CPCB formats:
    - DD-MM-YY (e.g. '06-01-15')
    - DD/MM/YYYY (e.g. '06/01/2015' or '6/1/2015')
    - DD-MM-YYYY (e.g. '06-01-2015')
    - YYYY-MM-DD (e.g. '2015-01-06')
    
    Returns (parsed_datetime_series, invalid_date_count).
    Does NOT discard records; unparseable dates become NaT.
    """
    # Clean strings
    s = date_series.astype(str).str.strip()
    s = s.replace(["nan", "NaN", "None", "", "NA", "N/A"], np.nan)
    
    # Try multiple specific formats sequentially
    formats = ["%d-%m-%y", "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%m/%d/%Y"]
    parsed = pd.Series(pd.NaT, index=date_series.index)
    
    for fmt in formats:
        mask = parsed.isna() & s.notna()
        if not mask.any():
            break
        parsed.loc[mask] = pd.to_datetime(s.loc[mask], format=fmt, errors="coerce")
        
    # Final fallback with flexible parser for any remaining
    mask_remaining = parsed.isna() & s.notna()
    if mask_remaining.any():
        parsed.loc[mask_remaining] = pd.to_datetime(s.loc[mask_remaining], errors="coerce")
        
    invalid_dates_count = int((s.notna() & parsed.isna()).sum())
    return parsed, invalid_dates_count


def convert_numeric_pollutants(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Converts pollutant columns to numeric floats.
    Invalid strings are coerced to NaN (genuine missingness preserved).
    Does NOT impute with 0 or mean/median.
    
    Returns (cleaned_df, non_numeric_counts).
    """
    df_clean = df.copy()
    non_numeric_counts = {}
    
    for col in POLLUTANT_COLUMNS:
        if col in df_clean.columns:
            # check non-numeric values before coercion (excluding known blanks)
            raw_s = df_clean[col].astype(str).str.strip().str.upper()
            non_numeric = (
                ~raw_s.isin(["", "NAN", "NONE", "NA", "N/A", "NULL"]) &
                pd.to_numeric(df_clean[col], errors="coerce").isna()
            ).sum()
            non_numeric_counts[col] = int(non_numeric)
            
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
            
    return df_clean, non_numeric_counts


def detect_negative_pollutants(df: pd.DataFrame) -> Dict[str, int]:
    """
    Detects negative pollutant measurements for validation.
    Does NOT silently delete records.
    """
    neg_counts = {}
    for col in POLLUTANT_COLUMNS:
        if col in df.columns:
            neg = int((df[col] < 0).sum())
            neg_counts[col] = neg
    return neg_counts


def detect_duplicates(df: pd.DataFrame) -> Tuple[int, int]:
    """
    Detects:
    1. Exact duplicate rows
    2. Duplicate station-date combinations
    """
    exact_duplicates = int(df.duplicated().sum())
    
    key_cols = ["stn_code", "sampling_date", "location_of_monitoring_station"]
    available_keys = [c for c in key_cols if c in df.columns]
    
    if len(available_keys) >= 2:
        station_date_dups = int(df.duplicated(subset=available_keys).sum())
    else:
        station_date_dups = 0
        
    return exact_duplicates, station_date_dups


def clean_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Executes the comprehensive cleaning sequence:
    1. Text normalization & whitespace trimming
    2. Date parsing & validation
    3. Numeric conversion preserving genuine missingness
    4. Duplicate and negative value checks
    
    Returns (cleaned_dataframe, audit_dictionary).
    """
    # 1. Clean text
    df_clean = clean_text_columns(df)
    
    # 2. Parse dates
    df_clean["sampling_date"], invalid_dates = parse_dates_robustly(df_clean["sampling_date"])
    
    # If data_year was missing or None, infer from sampling_date
    if "data_year" in df_clean.columns:
        inferred_years = df_clean["sampling_date"].dt.year
        df_clean["data_year"] = df_clean["data_year"].fillna(inferred_years)
        # Convert to nullable integer
        df_clean["data_year"] = df_clean["data_year"].astype("Int64")
        
    # 3. Numeric conversion
    df_clean, non_numeric_counts = convert_numeric_pollutants(df_clean)
    
    # 4. Negative values audit
    negative_counts = detect_negative_pollutants(df_clean)
    
    # 5. Duplicate checks
    exact_dups, station_date_dups = detect_duplicates(df_clean)
    
    # Only drop 100% exact duplicates if present
    if exact_dups > 0:
        df_clean = df_clean.drop_duplicates()
        
    audit_report = {
        "invalid_dates": invalid_dates,
        "exact_duplicates_found": exact_dups,
        "station_date_duplicates": station_date_dups,
        "negative_pollutant_counts": negative_counts,
        "non_numeric_coerced_counts": non_numeric_counts
    }
    
    return df_clean, audit_report
