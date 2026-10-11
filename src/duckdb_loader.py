"""
DuckDB Loader & Processed Storage Layer.

Saves the cleaned multi-year dataset to Parquet and loads it into a DuckDB database.
Creates typed table 'air_quality' with both canonical columns and standard analytical aliases.
"""

import os
from pathlib import Path
import duckdb
import pandas as pd


def export_to_parquet(df: pd.DataFrame, parquet_path: str = "data/processed/tamil_nadu_air_quality.parquet") -> str:
    """
    Exports the combined cleaned DataFrame to an analytical Parquet file.
    """
    Path(parquet_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(parquet_path, index=False, engine="pyarrow")
    return parquet_path


def load_into_duckdb(
    df: pd.DataFrame,
    db_path: str = "data/air_quality.duckdb",
    table_name: str = "air_quality"
) -> duckdb.DuckDBPyConnection:
    """
    Loads the cleaned multi-year dataset into DuckDB.
    Creates table 'air_quality' with full typed schema and convenient analytical aliases:
    - city (alias for city_town_village_area)
    - station_code (alias for stn_code)
    - station_location (alias for location_of_monitoring_station)
    - location_type (alias for type_of_location)
    - pm10 (alias for rspm_pm10)
    - pm25 (alias for pm_2_5)
    """
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Prepare DataFrame with alias columns for SQL convenience
    df_db = df.copy()
    df_db["station_code"] = df_db["stn_code"]
    df_db["city"] = df_db["city_town_village_area"]
    df_db["station_location"] = df_db["location_of_monitoring_station"]
    df_db["location_type"] = df_db["type_of_location"]
    df_db["pm10"] = df_db["rspm_pm10"]
    df_db["pm25"] = df_db["pm_2_5"]
    
    # Ensure correct types
    df_db["data_year"] = pd.to_numeric(df_db["data_year"], errors="coerce").astype("Int64")
    df_db["sampling_date"] = pd.to_datetime(df_db["sampling_date"]).dt.date
    
    conn = duckdb.connect(db_path)
    
    # Register and create table
    conn.register("df_temp", df_db)
    
    conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.execute(f"""
        CREATE TABLE {table_name} AS 
        SELECT 
            CAST(data_year AS INTEGER) AS data_year,
            CAST(source_file AS VARCHAR) AS source_file,
            CAST(stn_code AS VARCHAR) AS stn_code,
            CAST(station_code AS VARCHAR) AS station_code,
            CAST(sampling_date AS DATE) AS sampling_date,
            CAST(state AS VARCHAR) AS state,
            CAST(city_town_village_area AS VARCHAR) AS city_town_village_area,
            CAST(city AS VARCHAR) AS city,
            CAST(location_of_monitoring_station AS VARCHAR) AS location_of_monitoring_station,
            CAST(station_location AS VARCHAR) AS station_location,
            CAST(agency AS VARCHAR) AS agency,
            CAST(type_of_location AS VARCHAR) AS type_of_location,
            CAST(location_type AS VARCHAR) AS location_type,
            CAST(so2 AS DOUBLE) AS so2,
            CAST(no2 AS DOUBLE) AS no2,
            CAST(rspm_pm10 AS DOUBLE) AS rspm_pm10,
            CAST(pm10 AS DOUBLE) AS pm10,
            CAST(pm_2_5 AS DOUBLE) AS pm_2_5,
            CAST(pm25 AS DOUBLE) AS pm25
        FROM df_temp
    """)
    
    conn.unregister("df_temp")
    return conn
