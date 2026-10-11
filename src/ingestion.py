"""
Ingestion Layer for Tamil Nadu Air Quality Analytics Pipeline.

Discovers raw CSV files, handles character encodings, extracts data years,
and attaches lineage metadata (source file and data year).
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Tuple
import pandas as pd


def extract_year_from_filename(filename: str) -> Optional[int]:
    """
    Extract a 4-digit year (e.g., 2011 to 2030) from a filename.
    Returns the integer year if found, otherwise None.
    """
    match = re.search(r"\b(20\d{2})\b", filename)
    if match:
        return int(match.group(1))
    
    # Also check patterns like "2015-cpcb" or "air_quality_2015"
    match = re.search(r"(20\d{2})", filename)
    if match:
        return int(match.group(1))
    
    return None


def discover_raw_files(raw_dir: str = "data/raw") -> List[str]:
    """
    Discovers all CSV files inside the raw data directory, sorted chronologically.
    """
    raw_path = Path(raw_dir)
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw data directory '{raw_dir}' does not exist.")
    
    csv_files = [str(p) for p in raw_path.glob("*.csv") if not p.name.startswith(".")]
    
    # Sort files by extracted year if available, else alphabetically
    def sort_key(f: str):
        y = extract_year_from_filename(Path(f).name)
        return (0, y) if y is not None else (1, Path(f).name)
    
    return sorted(csv_files, key=sort_key)


def read_raw_file(filepath: str) -> pd.DataFrame:
    """
    Reads a single raw CSV file safely using UTF-8 or CP1252/Latin-1 fallback.
    Attaches 'source_file' and 'data_year' metadata columns.
    """
    path = Path(filepath)
    filename = path.name
    
    # Try reading with utf-8, fallback to cp1252/latin1
    encodings_to_try = ["utf-8", "cp1252", "latin1"]
    df = None
    last_err = None
    
    for enc in encodings_to_try:
        try:
            df = pd.read_csv(filepath, encoding=enc, low_memory=False)
            break
        except UnicodeDecodeError as err:
            last_err = err
            continue
    
    if df is None:
        raise ValueError(f"Failed to read '{filepath}' with tested encodings: {last_err}")
    
    # Extract data year
    extracted_year = extract_year_from_filename(filename)
    
    # Add lineage columns
    df["source_file"] = filename
    if extracted_year is not None:
        df["data_year"] = extracted_year
    else:
        df["data_year"] = None
        
    return df


def ingest_all_raw_files(raw_dir: str = "data/raw") -> List[Tuple[str, pd.DataFrame]]:
    """
    Discovers and reads all raw CSV files in the raw directory.
    Returns a list of (filepath, DataFrame) tuples.
    """
    files = discover_raw_files(raw_dir)
    if not files:
        raise ValueError(f"No CSV files found in '{raw_dir}'.")
    
    ingested = []
    for f in files:
        df = read_raw_file(f)
        ingested.append((f, df))
        
    return ingested
