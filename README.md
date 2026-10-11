# Tamil Nadu Air Quality Analysis & Multi-Year Analytics Pipeline

A production-quality, reproducible analytics pipeline for ingesting, profiling, cleaning, standardizing, and analyzing multi-year ambient air quality monitoring data across Tamil Nadu, India.

---

## 1. Project Overview

This project transforms fragmented, historical Central Pollution Control Board (CPCB) and Tamil Nadu Pollution Control Board (TNPCB) ambient air quality data into a standardized, reliable multi-year analytics database.

### Analytical & Engineering Focus
- **Eliminate Silent Errors:** Handles heterogeneous historical schemas, varying date formats, and missing pollutant monitoring without silently dropping rows or inventing values.
- **Defensible Data Principles:** Distinguishes genuine missingness from zero concentrations; preserves data lineage (`source_file`, `data_year`); flags anomalies (negative readings, duplicate keys) for auditability.
- **Dual-Layer Analytics:** Delivers high-performance analytical storage (Parquet + DuckDB) and automated reporting across 6 core analytical questions plus longitudinal Year-over-Year (YoY) trends.

---

## 2. Pipeline Architecture

```text
       +------------------------------------+
       |   Raw CSVs in data/raw/            |
       |   (e.g., air_quality_2011 to 2015) |
       +-----------------+------------------+
                         |
                         v
       +-----------------+------------------+
       |   Python Ingestion & Discovery     |
       |   (Character encoding resilience)  |
       +-----------------+------------------+
                         |
                         v
       +-----------------+------------------+
       |   Schema Standardization Layer     |
       |   (Maps historical headers to      |
       |    canonical schema)               |
       +-----------------+------------------+
                         |
                         v
       +-----------------+------------------+
       |   Data Cleaning & Validation       |
       |   (Multi-format date parsing,      |
       |    numeric conversion, flags)      |
       +-----------------+------------------+
                         |
                         v
       +-----------------+------------------+
       |   Data Quality Report Generator    |
       |   (outputs/data_quality_report.md) |
       +-----------------+------------------+
                         |
                         v
       +-----------------+------------------+
       |   Parquet Storage & DuckDB Load    |
       |   (data/air_quality.duckdb)        |
       +-----------------+------------------+
                         |
                         v
       +-----------------+------------------+
       |   Modular SQL Analytics            |
       |   (sql/Analysis-1.sql)             |
       +-----------------+------------------+
                         |
        +----------------+----------------+
        |                                 |
        v                                 v
+-------+--------+              +---------+----------+
| Analytical CSV |              | Power BI Dashboard |
| Outputs & MD   |              | (Direct Parquet/   |
| (outputs/*.csv)|              |  DuckDB ingestion) |
+----------------+              +--------------------+
```

---

## 3. Historical Datasets & Schema Evolution

The pipeline processes multi-year monitoring files (e.g., 2011–2015+). Over these years, official CPCB data collection underwent several structural transitions:

| Year | Historical Column Variations | Date Format Observed | Pollutant Peculiarities |
|---|---|---|---|
| **2011** | `Station Code`, `Sampling Date`, `SPM`, `RSPM/PM10` | `DD/MM/YYYY` | Routine PM2.5 not yet established under NAMP; SPM monitored |
| **2012** | `stn_code`, `sampling_date`, `pm10` (lowercase) | `YYYY-MM-DD` | PM2.5 not present in schema; RSPM named `pm10` |
| **2013** | `Stn Code`, `Sampling Date`, `RSPM/PM10` | `DD-MM-YYYY` | Pre-PM2.5 national routine monitoring |
| **2014** | `Stn Code`, `Sampling Date`, `RSPM/PM10`, `PM 2.5` | `DD-MM-YY` | Early pilot monitoring of PM2.5 (~10% coverage) |
| **2015** | `Stn Code`, `Sampling Date`, `RSPM/PM10`, `PM 2.5` | `DD-MM-YY` | Baseline authentic dataset; PM2.5 present at subset of stations (~19.7% coverage) |

### Canonical Schema
The standardization layer guarantees the following schema for every processed row:
- `data_year` *(INTEGER)*: Calendar monitoring year.
- `source_file` *(VARCHAR)*: Lineage back to the original CSV filename.
- `stn_code` *(VARCHAR)*: Monitoring station identifier.
- `sampling_date` *(DATE)*: Standardized sampling date (`YYYY-MM-DD`).
- `state` *(VARCHAR)*: State name (`Tamil Nadu`).
- `city_town_village_area` *(VARCHAR)*: Monitored city/urban agglomeration.
- `location_of_monitoring_station` *(VARCHAR)*: Specific site/station description.
- `agency` *(VARCHAR)*: Responsible monitoring body (TNPCB / CPCB).
- `type_of_location` *(VARCHAR)*: Zone type (`Industrial`, `Residential, Rural and other Areas`).
- `so2` *(DOUBLE)*: Sulphur Dioxide concentration ($\mu\text{g/m}^3$).
- `no2` *(DOUBLE)*: Nitrogen Dioxide concentration ($\mu\text{g/m}^3$).
- `rspm_pm10` *(DOUBLE)*: Respirable Suspended Particulate Matter / PM10 ($\mu\text{g/m}^3$).
- `pm_2_5` *(DOUBLE)*: Fine Particulate Matter ($\mu\text{g/m}^3$).

---

## 4. Critical Data Quality Principles & Analytical Caveats

1. **No Artificial Zero-Imputation:**
   - Missing pollutant measurements represent unmeasured intervals, sensor downtime, or pre-installation phases.
   - Replacing missing values with `0` would severely bias means downward and distort compliance calculations. Genuine missingness is strictly maintained as `NULL` / `NaN`.
2. **PM2.5 Longitudinal Comparability Limitation:**
   - Prior to 2014, PM2.5 was not part of standard NAMP routine protocols in Tamil Nadu. Even in 2015, only ~19.7% of station-dates had active PM2.5 monitors.
   - Long-term YoY trends for PM2.5 reflect the gradual expansion of the monitoring network, **not** a true environmental shift.
3. **Uneven Station Schedules & Coverage:**
   - NAMP stations are designed for non-continuous monitoring (typically 2 days per week, ~104 possible sampling days per year).
   - Any comparison between cities or stations must review observation counts alongside averages (enforced via the $\ge 30$ sample screening filter).
4. **Pollutants are Not Equivalent to AQI:**
   - Raw mass concentrations ($\mu\text{g/m}^3$) of different pollutants cannot be directly compared against each other (e.g., $50\,\mu\text{g/m}^3$ of SO2 is not directly comparable to $50\,\mu\text{g/m}^3$ of PM10).

---

## 5. SQL Analysis: Core Questions & Multi-Year Extensions

The analytical queries in `sql/Analysis-1.sql` answer the 6 core business/environmental questions plus longitudinal trends:

1. **Monthly Pollution Patterns (`monthly_pollution_trends.csv`)**:
   - Identifies seasonal variations per pollutant across all monitored years.
   - Tracks active stations and cities per month to separate seasonal weather effects from network coverage changes.
2. **City-Level Comparison (`city_pollution_comparison.csv`)**:
   - Ranks cities within each pollutant with median, mean, min, and max.
   - Enforces a `meets_30_observation_screen` boolean flag to prevent low-sample skew.
3. **Station Hotspots (`station_hotspots.csv`)**:
   - Identifies the highest-pollution stations with station metadata, location type, and 90th percentile values ($P_{90}$).
4. **Location-Type Comparison (`location_type_comparison.csv`)**:
   - Compares industrial zones against residential, rural, and other areas with standard deviation and missingness metrics.
5. **Extreme Pollution Observations (`extreme_pollution_events.csv`)**:
   - Identifies top individual peak observations per pollutant with exact dates, locations, and station codes.
6. **Data Coverage & Reliability (`data_coverage.csv`)**:
   - Evaluates station longevity, active years, sampling frequency, and pollutant-specific completeness percentages.
7. **Year-over-Year Trends (`yearly_pollution_trends.csv`)**:
   - Computes annual multi-year averages and medians alongside active station and city counts, explicitly noting historical PM2.5 network rollout.

---

## 6. How to Run

### Requirements
- Python 3.10+
- Dependencies: `pandas`, `duckdb`, `pyarrow`, `pytest`

### Run Full Pipeline
To execute the end-to-end ingestion, standardization, cleaning, quality profiling, DuckDB loading, and SQL query execution:

```bash
python -m src.pipeline
```
*(or `python src/pipeline.py`)*

### Run Automated Tests
To run the automated validation test suite:

```bash
python -m pytest -v tests/test_pipeline.py
```

---

## 7. Adding a New Year (e.g., 2016)

The pipeline is completely dynamic and requires zero code modifications to ingest new data:

1. **Drop the new CSV into `data/raw/`**:
   ```bash
   cp /path/to/cpcb_2016.csv data/raw/air_quality_2016.csv
   ```
2. **Execute the pipeline**:
   ```bash
   python -m src.pipeline
   ```
3. **Inspect the Data Quality Report**:
   - Open `outputs/data_quality_report.md` to verify rows, missingness rates, date bounds, and any invalid dates/negative values.
4. **Inspect Updated Analytical Outputs**:
   - Check `outputs/yearly_pollution_trends.csv` and `sql/query_results.md`.
5. **Refresh Power BI**:
   - Open Power BI and click **Refresh** against the updated `data/processed/tamil_nadu_air_quality.parquet` or `data/air_quality.duckdb`.

---

## 8. Power BI Integration

The processed data model is stored in `data/processed/tamil_nadu_air_quality.parquet` and `data/air_quality.duckdb`.

### Recommended Dashboard Model:
- **Filters / Slicers:** `data_year`, `city`, `stn_code`, `type_of_location`, `month`.
- **Card Visuals:** Total Valid Observations, Active Stations, Data Coverage %.
- **Trend Line Chart:** Multi-Year Monthly Trends (`month_number` on X-axis, concentration on Y-axis, legend by `pollutant`).
- **Bar Chart:** City Pollution Ranking with sample count tooltips.
- **Data Quality Indicator:** Visual showing valid sample counts alongside averages to remind users of coverage limitations.

---

## 9. Project Structure

```text
TamilNadu_AQI_Analysis/
├── data/
│   ├── raw/                             # Multi-year input CSVs (2011-2015+)
│   ├── processed/
│   │   └── tamil_nadu_air_quality.parquet  # Combined standardized analytical dataset
│   └── air_quality.duckdb               # DuckDB analytical database
├── dataset/                             # Original baseline datasets
├── notebook/
│   ├── Data-Understanding.ipynb         # Original exploratory analysis
│   └── Data-Cleaning.ipynb              # Original cleaning prototyping
├── outputs/                             # Automated analytical CSV exports
│   ├── data_quality_report.md           # Cross-year Data Quality Report
│   ├── yearly_data_quality_summary.csv  # Yearly quality metrics table
│   ├── monthly_pollution_trends.csv
│   ├── city_pollution_comparison.csv
│   ├── station_hotspots.csv
│   ├── location_type_comparison.csv
│   ├── extreme_pollution_events.csv
│   ├── data_coverage.csv
│   └── yearly_pollution_trends.csv
├── sql/
│   ├── Analysis-1.sql                   # Modular, annotated analytical SQL queries
│   └── query_results.md                 # Complete markdown query execution report
├── src/
│   ├── __init__.py
│   ├── ingestion.py                     # CSV discovery & character encoding resilience
│   ├── standardization.py               # Flexible alias mapping to canonical schema
│   ├── cleaning.py                      # Robust text, date & numeric transformations
│   ├── validation.py                   # Data quality profiler & markdown generator
│   ├── duckdb_loader.py                 # Parquet export & DuckDB table loader
│   ├── analysis.py                      # SQL query executor & Markdown table generator
│   └── pipeline.py                      # Master pipeline entry point
├── tests/
│   └── test_pipeline.py                 # Pytest unit tests for core transformations
├── .gitignore
└── README.md
```
