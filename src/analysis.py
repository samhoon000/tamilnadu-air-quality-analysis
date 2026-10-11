"""
SQL Analysis Runner & Reporting Layer.

Executes analytical queries from sql/Analysis-1.sql against DuckDB,
exports result sets to outputs/*.csv, and compiles a comprehensive
query_results.md document.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import duckdb
import pandas as pd


def parse_sql_file(sql_path: str = "sql/Analysis-1.sql") -> List[Tuple[str, str, str]]:
    """
    Parses sql/Analysis-1.sql into individual named queries.
    Returns list of (query_name, description, sql_text).
    """
    with open(sql_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by query name annotations
    # Pattern looks for: -- Query Name: <name>\n<sql>
    pattern = r"-- Query Name:\s*([a-zA-Z0-9_]+)\s*\n(.*?)(?=(?:-- Query Name:|\Z))"
    matches = re.findall(pattern, content, flags=re.DOTALL)
    
    queries = []
    for name, sql in matches:
        sql_clean = sql.strip()
        # Remove trailing semicolons for DuckDB fetchdf
        sql_clean = re.sub(r";\s*$", "", sql_clean)
        queries.append((name, name.replace("_", " ").title(), sql_clean))
        
    return queries


def df_to_markdown_table(df: pd.DataFrame) -> str:
    """Format DataFrame as a Markdown table without requiring external packages."""
    try:
        return df.to_markdown(index=False)
    except Exception:
        # Fallback manual markdown generator
        headers = [str(c) for c in df.columns]
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |"
        ]
        for _, row in df.iterrows():
            vals = [str(v) if pd.notna(v) else "" for v in row.values]
            lines.append("| " + " | ".join(vals) + " |")
        return "\n".join(lines)


def run_analytical_queries(
    db_path: str = "data/air_quality.duckdb",
    sql_path: str = "sql/Analysis-1.sql",
    outputs_dir: str = "outputs",
    results_md_path: str = "sql/query_results.md"
) -> Dict[str, pd.DataFrame]:
    """
    Executes the analytical queries against DuckDB, saves CSV outputs,
    and updates sql/query_results.md.
    """
    os.makedirs(outputs_dir, exist_ok=True)
    queries = parse_sql_file(sql_path)
    
    conn = duckdb.connect(db_path, read_only=True)
    results = {}
    md_sections = [
        "# Tamil Nadu Air Quality - SQL Analytical Query Results",
        "",
        "This document contains the execution results of the 6 core analytical questions and the multi-year trend analysis executed directly against DuckDB (`data/air_quality.duckdb`).",
        "",
        "## Execution Summary",
        "",
        "| # | Analysis | Output File | Rows Returned | Status |",
        "|---|---|---|---:|---:|"
    ]
    
    detailed_sections = []
    
    for i, (name, title, sql) in enumerate(queries, 1):
        try:
            df = conn.execute(sql).fetchdf()
            csv_filename = f"{name}.csv"
            csv_filepath = os.path.join(outputs_dir, csv_filename)
            df.to_csv(csv_filepath, index=False)
            results[name] = df
            
            md_sections.append(f"| {i} | {title} | [`{csv_filename}`](../outputs/{csv_filename}) | {len(df):,} | SUCCESS |")
            
            # Format preview markdown table (first 15 rows)
            preview_df = df.head(15)
            detailed_sections.extend([
                f"### {i}. {title}",
                f"- **Output File:** `outputs/{csv_filename}`",
                f"- **Total Rows:** {len(df):,}",
                "",
                df_to_markdown_table(preview_df),
                ""
            ])
            if len(df) > 15:
                detailed_sections.extend([
                    f"*Showing preview of first 15 of {len(df):,} rows. Complete results saved in `outputs/{csv_filename}`.*",
                    ""
                ])
                
        except Exception as e:
            md_sections.append(f"| {i} | {title} | {name}.csv | 0 | ERROR: {str(e)[:50]} |")
            detailed_sections.extend([
                f"### {i}. {title}",
                f"**Execution Error:** `{str(e)}`",
                ""
            ])
            
    conn.close()
    
    # Write query_results.md
    full_report = "\n".join(md_sections) + "\n\n## Query Outputs & Analytical Previews\n\n" + "\n".join(detailed_sections)
    with open(results_md_path, "w", encoding="utf-8") as f:
        f.write(full_report)
        
    return results
