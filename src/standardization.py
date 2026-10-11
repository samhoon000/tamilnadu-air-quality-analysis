"""
Schema Standardization Layer for Tamil Nadu Air Quality Analytics Pipeline.

Maps diverse historical and multi-year column conventions into the canonical schema:
- stn_code
- sampling_date
- state
- city_town_village_area
- location_of_monitoring_station
- agency
- type_of_location
- so2
- no2
- rspm_pm10
- pm_2_5
- data_year
- source_file
"""

import re
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

# Canonical column definitions
CANONICAL_COLUMNS = [
    "data_year",
    "source_file",
    "stn_code",
    "sampling_date",
    "state",
    "city_town_village_area",
    "location_of_monitoring_station",
    "agency",
    "type_of_location",
    "so2",
    "no2",
    "rspm_pm10",
    "pm_2_5"
]

# Mapping dictionary from normalized name to canonical column
COLUMN_MAPPING_RULES: Dict[str, str] = {
    # Station code
    "stn_code": "stn_code",
    "station_code": "stn_code",
    "stationcode": "stn_code",
    "stn": "stn_code",
    "stn_no": "stn_code",
    
    # Sampling date
    "sampling_date": "sampling_date",
    "date": "sampling_date",
    "samplingdate": "sampling_date",
    "sample_date": "sampling_date",
    
    # State
    "state": "state",
    "state_name": "state",
    
    # City / Area
    "city_town_village_area": "city_town_village_area",
    "city": "city_town_village_area",
    "city_town": "city_town_village_area",
    "town": "city_town_village_area",
    "area": "city_town_village_area",
    
    # Location
    "location_of_monitoring_station": "location_of_monitoring_station",
    "location": "location_of_monitoring_station",
    "station_location": "location_of_monitoring_station",
    "monitoring_station_location": "location_of_monitoring_station",
    "monitoring_station": "location_of_monitoring_station",
    
    # Agency
    "agency": "agency",
    "monitoring_agency": "agency",
    
    # Type of location
    "type_of_location": "type_of_location",
    "location_type": "type_of_location",
    "type": "type_of_location",
    
    # Pollutants
    "so2": "so2",
    "sulphur_dioxide": "so2",
    "so_2": "so2",
    
    "no2": "no2",
    "nitrogen_dioxide": "no2",
    "no_2": "no2",
    
    "rspm_pm10": "rspm_pm10",
    "rspm": "rspm_pm10",
    "pm10": "rspm_pm10",
    "pm_10": "rspm_pm10",
    "rspm_pm_10": "rspm_pm10",
    
    "pm_2_5": "pm_2_5",
    "pm2_5": "pm_2_5",
    "pm25": "pm_2_5",
    "pm_25": "pm_2_5",
    
    # Lineage columns
    "data_year": "data_year",
    "source_file": "source_file"
}


def normalize_column_name(col: str) -> str:
    """
    Normalizes a column name by stripping whitespace, lowercasing,
    and replacing non-alphanumeric characters with underscores.
    """
    clean = col.strip().lower()
    clean = re.sub(r"[^a-z0-9]+", "_", clean)
    clean = clean.strip("_")
    return clean


def map_columns_to_canonical(columns: List[str]) -> Tuple[Dict[str, str], List[str]]:
    """
    Generates a mapping from raw column names to canonical names.
    Returns (mapping_dict, unmapped_columns).
    """
    mapping = {}
    unmapped = []
    
    for raw_col in columns:
        normalized = normalize_column_name(raw_col)
        canonical = COLUMN_MAPPING_RULES.get(normalized)
        
        if canonical:
            mapping[raw_col] = canonical
        else:
            unmapped.append(raw_col)
            
    return mapping, unmapped


def standardize_schema(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Standardizes the schema of a DataFrame to the canonical format.
    - Renames recognized columns to canonical names.
    - Preserves unmapped columns as metadata info.
    - Safely adds any missing canonical columns with NaN (never imputes with 0).
    - Ensures standard column ordering.
    """
    df_std = df.copy()
    col_mapping, unmapped = map_columns_to_canonical(list(df_std.columns))
    
    df_std = df_std.rename(columns=col_mapping)
    
    missing_canonical = []
    for col in CANONICAL_COLUMNS:
        if col not in df_std.columns:
            missing_canonical.append(col)
            df_std[col] = np.nan
            
    # Standardize column order, placing any extra unmapped columns at the end
    extra_cols = [c for c in df_std.columns if c not in CANONICAL_COLUMNS]
    ordered_cols = CANONICAL_COLUMNS + extra_cols
    df_std = df_std[ordered_cols]
    
    report = {
        "column_mapping": col_mapping,
        "missing_canonical_columns": missing_canonical,
        "extra_columns": extra_cols
    }
    
    return df_std, report
