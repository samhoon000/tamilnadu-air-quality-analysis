"""
Main Pipeline Orchestrator for Tamil Nadu Air Quality Analysis.

Executes the full end-to-end data pipeline:
1. Discovers raw CSV files dynamically
2. Ingests raw data with character encoding resilience
3. Standardizes heterogeneous schemas to the canonical schema
4. Cleans text, parses dates, and safely casts pollutants without 0-imputation
5. Validates data quality, flagging negative values and duplicate keys
6. Generates comprehensive Data Quality Reports (Markdown + CSV)
7. Combines multi-year data into an optimized Parquet dataset
8. Loads into DuckDB with typed columns and analytical aliases
9. Executes analytical SQL answering the 6 core questions + multi-year trends
10. Exports result tables to outputs/ and compiles sql/query_results.md
"""

import sys
import time
from pathlib import Path
import pandas as pd

from src.ingestion import ingest_all_raw_files
from src.standardization import standardize_schema
from src.cleaning import clean_dataset
from src.validation import profile_dataset, generate_quality_reports
from src.duckdb_loader import export_to_parquet, load_into_duckdb
from src.analysis import run_analytical_queries


def run_pipeline(
    raw_dir: str = "data/raw",
    processed_dir: str = "data/processed",
    db_path: str = "data/air_quality.duckdb",
    sql_path: str = "sql/Analysis-1.sql",
    outputs_dir: str = "outputs"
) -> bool:
    """
    Runs the complete multi-year air quality pipeline.
    """
    start_time = time.time()
    print("=" * 70)
    print("TAMIL NADU AIR QUALITY - MULTI-YEAR ANALYTICS PIPELINE")
    print("=" * 70)
    
    # Step 1: Ingestion
    print(f"\n[1/7] Ingesting raw CSV files from '{raw_dir}'...")
    raw_files = ingest_all_raw_files(raw_dir)
    print(f"      Discovered {len(raw_files)} raw files.")
    
    cleaned_dfs = []
    profiles = []
    
    # Step 2-4: Process each file individually
    print(f"\n[2/7] Standardizing schemas and cleaning yearly datasets...")
    for filepath, raw_df in raw_files:
        filename = Path(filepath).name
        year = raw_df["data_year"].iloc[0] if "data_year" in raw_df.columns else "Unknown"
        print(f"      - Processing '{filename}' (Year: {year}, Raw rows: {len(raw_df):,})")
        
        # Standardize schema
        std_df, std_report = standardize_schema(raw_df)
        if std_report["missing_canonical_columns"]:
            print(f"        Notice: Unmonitored canonical columns initialized to NULL: {std_report['missing_canonical_columns']}")
            
        # Clean dataset
        clean_df, clean_audit = clean_dataset(std_df)
        if clean_audit["exact_duplicates_found"] > 0:
            print(f"        Audit: Dropped {clean_audit['exact_duplicates_found']} exact duplicate row(s)")
        if clean_audit["invalid_dates"] > 0:
            print(f"        Warning: Flagged {clean_audit['invalid_dates']} invalid date(s)")
            
        cleaned_dfs.append(clean_df)
        
        # Profile dataset
        profile = profile_dataset(clean_df, filename, year, clean_audit)
        profiles.append(profile)
        
    # Step 5: Combine datasets & validate quality
    print(f"\n[3/7] Combining datasets & generating Data Quality Report...")
    combined_df = pd.concat(cleaned_dfs, ignore_index=True)
    print(f"      Total multi-year records: {len(combined_df):,}")
    
    summary_df, report_path = generate_quality_reports(profiles, combined_df, outputs_dir)
    print(f"      Data Quality Report generated at: '{report_path}'")
    print(f"      Yearly summary CSV generated at: '{outputs_dir}/yearly_data_quality_summary.csv'")
    
    # Step 6: Parquet & DuckDB storage
    print(f"\n[4/7] Writing processed Parquet dataset...")
    parquet_path = f"{processed_dir}/tamil_nadu_air_quality.parquet"
    export_to_parquet(combined_df, parquet_path)
    print(f"      Parquet dataset saved to: '{parquet_path}'")
    
    print(f"\n[5/7] Loading into DuckDB ('{db_path}')...")
    conn = load_into_duckdb(combined_df, db_path=db_path)
    conn.close()
    print(f"      DuckDB table 'air_quality' loaded successfully.")
    
    # Step 7: Analytical SQL execution
    print(f"\n[6/7] Running analytical SQL queries from '{sql_path}'...")
    query_results = run_analytical_queries(
        db_path=db_path,
        sql_path=sql_path,
        outputs_dir=outputs_dir,
        results_md_path="sql/query_results.md"
    )
    for q_name, q_df in query_results.items():
        print(f"      - {q_name}: {len(q_df):,} rows -> 'outputs/{q_name}.csv'")
    print(f"      Full query results compiled in: 'sql/query_results.md'")
    
    elapsed = round(time.time() - start_time, 2)
    print("\n[7/7] Pipeline execution completed successfully!")
    print(f"      Execution time: {elapsed} seconds.")
    print("=" * 70)
    return True


if __name__ == "__main__":
    success = run_pipeline()
    if not success:
        sys.exit(1)
