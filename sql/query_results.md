# Tamil Nadu Air Quality - SQL Analytical Query Results

This document contains the execution results of the 6 core analytical questions and the multi-year trend analysis executed directly against DuckDB (`data/air_quality.duckdb`).

## Execution Summary

| # | Analysis | Output File | Rows Returned | Status |
|---|---|---|---:|---:|
| 1 | Monthly Pollution Trends | [`monthly_pollution_trends.csv`](../outputs/monthly_pollution_trends.csv) | 48 | SUCCESS |
| 2 | City Pollution Comparison | [`city_pollution_comparison.csv`](../outputs/city_pollution_comparison.csv) | 32 | SUCCESS |
| 3 | Station Hotspots | [`station_hotspots.csv`](../outputs/station_hotspots.csv) | 124 | SUCCESS |
| 4 | Location Type Comparison | [`location_type_comparison.csv`](../outputs/location_type_comparison.csv) | 8 | SUCCESS |
| 5 | Extreme Pollution Events | [`extreme_pollution_events.csv`](../outputs/extreme_pollution_events.csv) | 90 | SUCCESS |
| 6 | Data Coverage | [`data_coverage.csv`](../outputs/data_coverage.csv) | 31 | SUCCESS |
| 7 | Yearly Pollution Trends | [`yearly_pollution_trends.csv`](../outputs/yearly_pollution_trends.csv) | 5 | SUCCESS |

## Query Outputs & Analytical Previews

### 1. Monthly Pollution Trends
- **Output File:** `outputs/monthly_pollution_trends.csv`
- **Total Rows:** 48

| pollutant   |   month_number | month_name   |   valid_observations |   years_represented |   active_cities |   active_stations |   mean_concentration |   median_concentration |   monthly_rank_by_mean |
|:------------|---------------:|:-------------|---------------------:|--------------------:|----------------:|------------------:|---------------------:|-----------------------:|-----------------------:|
| NO2         |              1 | January      |                  932 |                   5 |               8 |                31 |                20.26 |                  20.15 |                      3 |
| NO2         |              2 | February     |                  948 |                   5 |               8 |                31 |                20.11 |                  20    |                      7 |
| NO2         |              3 | March        |                  970 |                   5 |               8 |                31 |                20.14 |                  20.3  |                      5 |
| NO2         |              4 | April        |                  958 |                   5 |               8 |                31 |                20.14 |                  20.2  |                      5 |
| NO2         |              5 | May          |                  930 |                   5 |               8 |                31 |                20.47 |                  20.5  |                      1 |
| NO2         |              6 | June         |                  903 |                   5 |               8 |                31 |                20.11 |                  20    |                      7 |
| NO2         |              7 | July         |                  958 |                   5 |               8 |                31 |                19.74 |                  19.95 |                     11 |
| NO2         |              8 | August       |                  951 |                   5 |               8 |                31 |                19.79 |                  19.6  |                     10 |
| NO2         |              9 | September    |                  730 |                   5 |               8 |                31 |                19.6  |                  19.7  |                     12 |
| NO2         |             10 | October      |                  960 |                   5 |               8 |                31 |                20.42 |                  20    |                      2 |
| NO2         |             11 | November     |                  842 |                   5 |               8 |                31 |                20.22 |                  20    |                      4 |
| NO2         |             12 | December     |                  883 |                   5 |               8 |                31 |                19.83 |                  19.8  |                      9 |
| PM10        |              1 | January      |                  944 |                   5 |               8 |                31 |                56.43 |                  56    |                     10 |
| PM10        |              2 | February     |                  949 |                   5 |               8 |                31 |                58.28 |                  57.7  |                      2 |
| PM10        |              3 | March        |                  978 |                   5 |               8 |                31 |                58.11 |                  57.7  |                      5 |

*Showing preview of first 15 of 48 rows. Complete results saved in `outputs/monthly_pollution_trends.csv`.*

### 2. City Pollution Comparison
- **Output File:** `outputs/city_pollution_comparison.csv`
- **Total Rows:** 32

| pollutant   | city        |   valid_observations |   years_monitored |   monitoring_stations |   mean_concentration |   median_concentration |   min_concentration |   max_concentration |   city_rank | meets_30_observation_screen   |
|:------------|:------------|---------------------:|------------------:|----------------------:|---------------------:|-----------------------:|--------------------:|--------------------:|------------:|:------------------------------|
| NO2         | Salem       |                  360 |                 5 |                     1 |                22    |                  21.95 |                 5   |                36   |           1 | True                          |
| NO2         | Coimbatore  |                 1023 |                 5 |                     3 |                20.94 |                  21    |                 5   |                52   |           2 | True                          |
| NO2         | Mettur      |                  832 |                 5 |                     2 |                20.89 |                  20.9  |                 6.3 |                49   |           3 | True                          |
| NO2         | Madurai     |                 1192 |                 5 |                     3 |                20.81 |                  20.6  |                 5   |                48   |           4 | True                          |
| NO2         | Chennai     |                 3964 |                 5 |                    11 |                19.96 |                  19.8  |                 5   |                73   |           5 | True                          |
| NO2         | Cuddalore   |                 1068 |                 5 |                     3 |                19.68 |                  20    |                 5   |                36.5 |           6 | True                          |
| NO2         | Trichy      |                 1500 |                 5 |                     5 |                19.27 |                  19.3  |                 5   |                37.7 |           7 | True                          |
| NO2         | Thoothukudi |                 1026 |                 5 |                     3 |                19.09 |                  19.2  |                 5   |                33.3 |           8 | True                          |
| PM10        | Thoothukudi |                 1041 |                 5 |                     3 |                63.99 |                  59    |                12   |               289   |           1 | True                          |
| PM10        | Trichy      |                 1519 |                 5 |                     5 |                60.49 |                  57.7  |                12   |               148   |           2 | True                          |
| PM10        | Madurai     |                 1203 |                 5 |                     3 |                58.54 |                  57.9  |                12   |               169   |           3 | True                          |
| PM10        | Cuddalore   |                 1079 |                 5 |                     3 |                57.07 |                  56.8  |                12   |               114   |           4 | True                          |
| PM10        | Salem       |                  365 |                 5 |                     1 |                56.15 |                  56    |                12   |               122   |           5 | True                          |
| PM10        | Chennai     |                 4005 |                 5 |                    11 |                55.95 |                  54.8  |                 6   |               263   |           6 | True                          |
| PM10        | Mettur      |                  844 |                 5 |                     2 |                55.08 |                  54.4  |                12   |               109.4 |           7 | True                          |

*Showing preview of first 15 of 32 rows. Complete results saved in `outputs/city_pollution_comparison.csv`.*

### 3. Station Hotspots
- **Output File:** `outputs/station_hotspots.csv`
- **Total Rows:** 124

| pollutant   |   stn_code | city       | location_of_monitoring_station                                   | type_of_location                   | agency                                                |   valid_observations |   distinct_sampling_dates |   years_active |   mean_concentration |   median_concentration |   p90_concentration |   max_concentration |   station_rank | meets_30_observation_screen   |
|:------------|-----------:|:-----------|:-----------------------------------------------------------------|:-----------------------------------|:------------------------------------------------------|---------------------:|--------------------------:|---------------:|---------------------:|-----------------------:|--------------------:|--------------------:|---------------:|:------------------------------|
| NO2         |        309 | Salem      | Sowdeswari College Building, Salem                               | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  360 |                       367 |              5 |                22    |                  21.95 |               29.64 |                36   |              1 | True                          |
| NO2         |        763 | Mettur     | SIDCO Industrial Complex, Mettur                                 | Industrial Area                    | Tamilnadu State Pollution Control Board               |                  403 |                       413 |              5 |                21.62 |                  21.6  |               28.96 |                49   |              2 | True                          |
| NO2         |        238 | Coimbatore | Distt. Collector's Office, Coimbatore                            | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  336 |                       344 |              5 |                21.46 |                  21.9  |               27    |                38   |              3 | True                          |
| NO2         |        307 | Madurai    | Fenner (I) Ltd. Employees Assiciation Building Kochadai, Madurai | Industrial Area                    | Tamilnadu State Pollution Control Board               |                  403 |                       409 |              5 |                21.28 |                  21.1  |               27.58 |                48   |              4 | True                          |
| NO2         |        237 | Coimbatore | SIDCO Office, Coimbatore                                         | Industrial Area                    | Tamilnadu State Pollution Control Board               |                  332 |                       338 |              5 |                20.99 |                  20.7  |               28    |                52   |              5 | True                          |
| NO2         |        308 | Madurai    | Kunnathur Chatram East Avani Mollai Street, Madurai              | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  425 |                       432 |              5 |                20.88 |                  20.5  |               28    |                48   |              6 | True                          |
| NO2         |        161 | Chennai    | Thiruvottiyur Municipal Office, Chennai                          | Industrial Area                    | National Environmental Engineering Research Institute |                  434 |                       444 |              5 |                20.81 |                  20.3  |               29    |                67   |              7 | True                          |
| NO2         |        767 | Chennai    | Kilpauk, Chennai                                                 | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  331 |                       344 |              5 |                20.76 |                  20.9  |               27    |                36.6 |              8 | True                          |
| NO2         |        160 | Chennai    | NEERI, CSIR Campus Chennai                                       | Residential, Rural and other Areas | National Environmental Engineering Research Institute |                  371 |                       382 |              5 |                20.7  |                  20.1  |               28.5  |                73   |              9 | True                          |
| NO2         |        766 | Chennai    | Thiyagaraya Nagar, Chennai                                       | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  390 |                       403 |              5 |                20.68 |                  20.7  |               27    |                38   |             10 | True                          |
| NO2         |        765 | Chennai    | Anna Nagar, Chennai                                              | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  344 |                       348 |              5 |                20.42 |                  20.55 |               26.27 |                37   |             11 | True                          |
| NO2         |        375 | Coimbatore | Poniarajapuram, On the top of DEL, Coimbatore                    | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  355 |                       361 |              5 |                20.4  |                  21    |               26.24 |                34.1 |             12 | True                          |
| NO2         |        306 | Madurai    | Highway (Project -I) Building, Madurai                           | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  364 |                       370 |              5 |                20.22 |                  20.1  |               27    |                36   |             13 | True                          |
| NO2         |        762 | Mettur     | Raman Nagar, Mettur                                              | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  429 |                       436 |              5 |                20.2  |                  20    |               26.1  |                45   |             14 | True                          |
| NO2         |        761 | Cuddalore  | District Environmental Engineer Office, Imperial Road, Cuddalore | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  391 |                       394 |              5 |                19.96 |                  20.2  |               25.4  |                36.5 |             15 | True                          |

*Showing preview of first 15 of 124 rows. Complete results saved in `outputs/station_hotspots.csv`.*

### 4. Location Type Comparison
- **Output File:** `outputs/location_type_comparison.csv`
- **Total Rows:** 8

| type_of_location                   | pollutant   |   total_records |   valid_observations |   missing_observations |   missing_pct |   stations_represented |   cities_represented |   mean_concentration |   median_concentration |   stddev_concentration |   max_concentration |
|:-----------------------------------|:------------|----------------:|---------------------:|-----------------------:|--------------:|-----------------------:|---------------------:|---------------------:|-----------------------:|-----------------------:|--------------------:|
| Industrial Area                    | NO2         |            3399 |                 3330 |                     69 |          2.03 |                      9 |                    6 |                20.17 |                   20   |                   5.58 |                  67 |
| Residential, Rural and other Areas | NO2         |            7787 |                 7635 |                    152 |          1.95 |                     22 |                    8 |                20.04 |                   20   |                   5.43 |                  73 |
| Residential, Rural and other Areas | PM10        |            7787 |                 7722 |                     65 |          0.83 |                     22 |                    8 |                58.23 |                   56.8 |                  22.72 |                 263 |
| Industrial Area                    | PM10        |            3399 |                 3366 |                     33 |          0.97 |                      9 |                    6 |                55.73 |                   54.1 |                  20.51 |                 289 |
| Industrial Area                    | PM2.5       |            3399 |                  225 |                   3174 |         93.38 |                      9 |                    6 |                29.76 |                   28   |                  10.66 |                  82 |
| Residential, Rural and other Areas | PM2.5       |            7787 |                  452 |                   7335 |         94.2  |                     22 |                    8 |                29.54 |                   26   |                  16.65 |                 141 |
| Industrial Area                    | SO2         |            3399 |                 3323 |                     76 |          2.24 |                      9 |                    6 |                10.17 |                   10.1 |                   3.69 |                  40 |
| Residential, Rural and other Areas | SO2         |            7787 |                 7635 |                    152 |          1.95 |                     22 |                    8 |                10.12 |                   10   |                   3.87 |                  25 |

### 5. Extreme Pollution Events
- **Output File:** `outputs/extreme_pollution_events.csv`
- **Total Rows:** 90

| pollutant   |   peak_rank |   data_year | sampling_date       | city       |   stn_code | location_of_monitoring_station                                   | type_of_location                   |   recorded_concentration |
|:------------|------------:|------------:|:--------------------|:-----------|-----------:|:-----------------------------------------------------------------|:-----------------------------------|-------------------------:|
| NO2         |           1 |        2015 | 2015-12-15 00:00:00 | Chennai    |        160 | NEERI, CSIR Campus Chennai                                       | Residential, Rural and other Areas |                       73 |
| NO2         |           2 |        2015 | 2015-11-27 00:00:00 | Chennai    |        160 | NEERI, CSIR Campus Chennai                                       | Residential, Rural and other Areas |                       67 |
| NO2         |           2 |        2015 | 2015-11-27 00:00:00 | Chennai    |        161 | Thiruvottiyur Municipal Office, Chennai                          | Industrial Area                    |                       67 |
| NO2         |           3 |        2015 | 2015-11-27 00:00:00 | Chennai    |        159 | Madras Medical College, Chennai                                  | Residential, Rural and other Areas |                       59 |
| NO2         |           4 |        2015 | 2015-12-15 00:00:00 | Chennai    |        159 | Madras Medical College, Chennai                                  | Residential, Rural and other Areas |                       53 |
| NO2         |           5 |        2015 | 2015-05-22 00:00:00 | Chennai    |        161 | Thiruvottiyur Municipal Office, Chennai                          | Industrial Area                    |                       52 |
| NO2         |           5 |        2015 | 2015-08-18 00:00:00 | Coimbatore |        237 | SIDCO Office, Coimbatore                                         | Industrial Area                    |                       52 |
| NO2         |           6 |        2015 | 2015-01-07 00:00:00 | Chennai    |        161 | Thiruvottiyur Municipal Office, Chennai                          | Industrial Area                    |                       49 |
| NO2         |           6 |        2015 | 2015-10-06 00:00:00 | Chennai    |        160 | NEERI, CSIR Campus Chennai                                       | Residential, Rural and other Areas |                       49 |
| NO2         |           6 |        2015 | 2015-10-13 00:00:00 | Mettur     |        763 | SIDCO Industrial Complex, Mettur                                 | Industrial Area                    |                       49 |
| NO2         |           7 |        2015 | 2015-05-06 00:00:00 | Madurai    |        307 | Fenner (I) Ltd. Employees Assiciation Building Kochadai, Madurai | Industrial Area                    |                       48 |
| NO2         |           7 |        2015 | 2015-05-12 00:00:00 | Madurai    |        308 | Kunnathur Chatram East Avani Mollai Street, Madurai              | Residential, Rural and other Areas |                       48 |
| NO2         |           7 |        2015 | 2015-05-22 00:00:00 | Chennai    |        159 | Madras Medical College, Chennai                                  | Residential, Rural and other Areas |                       48 |
| NO2         |           8 |        2015 | 2015-10-09 00:00:00 | Mettur     |        763 | SIDCO Industrial Complex, Mettur                                 | Industrial Area                    |                       46 |
| NO2         |           9 |        2015 | 2015-05-08 00:00:00 | Chennai    |        160 | NEERI, CSIR Campus Chennai                                       | Residential, Rural and other Areas |                       45 |

*Showing preview of first 15 of 90 rows. Complete results saved in `outputs/extreme_pollution_events.csv`.*

### 6. Data Coverage
- **Output File:** `outputs/data_coverage.csv`
- **Total Rows:** 31

| city        |   stn_code | location_of_monitoring_station                                   | type_of_location                   |   years_active |   total_sampling_days |   total_rows |   valid_so2_samples |   valid_no2_samples |   valid_pm10_samples |   valid_pm25_samples |   so2_completeness_pct |   no2_completeness_pct |   pm10_completeness_pct |   pm25_completeness_pct | earliest_date       | latest_date         |
|:------------|-----------:|:-----------------------------------------------------------------|:-----------------------------------|---------------:|----------------------:|-------------:|--------------------:|--------------------:|---------------------:|---------------------:|-----------------------:|-----------------------:|------------------------:|------------------------:|:--------------------|:--------------------|
| Chennai     |        161 | Thiruvottiyur Municipal Office, Chennai                          | Industrial Area                    |              5 |                   444 |          444 |                 431 |                 434 |                  440 |                    6 |                   97.1 |                   97.7 |                    99.1 |                     1.4 | 2011-01-02 00:00:00 | 2015-12-30 00:00:00 |
| Mettur      |        762 | Raman Nagar, Mettur                                              | Residential, Rural and other Areas |              5 |                   436 |          436 |                 426 |                 429 |                  435 |                   30 |                   97.7 |                   98.4 |                    99.8 |                     6.9 | 2011-01-02 00:00:00 | 2015-12-31 00:00:00 |
| Madurai     |        308 | Kunnathur Chatram East Avani Mollai Street, Madurai              | Residential, Rural and other Areas |              5 |                   432 |          432 |                 426 |                 425 |                  430 |                   10 |                   98.6 |                   98.4 |                    99.5 |                     2.3 | 2011-01-02 00:00:00 | 2015-12-29 00:00:00 |
| Mettur      |        763 | SIDCO Industrial Complex, Mettur                                 | Industrial Area                    |              5 |                   413 |          413 |                 400 |                 403 |                  409 |                   35 |                   96.9 |                   97.6 |                    99   |                     8.5 | 2011-01-05 00:00:00 | 2015-12-29 00:00:00 |
| Madurai     |        307 | Fenner (I) Ltd. Employees Assiciation Building Kochadai, Madurai | Industrial Area                    |              5 |                   409 |          409 |                 403 |                 403 |                  407 |                   32 |                   98.5 |                   98.5 |                    99.5 |                     7.8 | 2011-01-02 00:00:00 | 2015-12-30 00:00:00 |
| Chennai     |        766 | Thiyagaraya Nagar, Chennai                                       | Residential, Rural and other Areas |              5 |                   403 |          403 |                 396 |                 390 |                  399 |                    7 |                   98.3 |                   96.8 |                    99   |                     1.7 | 2011-01-02 00:00:00 | 2015-12-31 00:00:00 |
| Chennai     |         38 | Kathivakkam, Municipal Kalyana Mandapam, Chennai                 | Industrial Area                    |              5 |                   398 |          398 |                 388 |                 392 |                  390 |                   77 |                   97.5 |                   98.5 |                    98   |                    19.3 | 2011-01-02 00:00:00 | 2015-12-31 00:00:00 |
| Chennai     |         72 | Thiruvottiyur, Chennai                                           | Industrial Area                    |              5 |                   397 |          397 |                 388 |                 391 |                  392 |                    6 |                   97.7 |                   98.5 |                    98.7 |                     1.5 | 2011-01-02 00:00:00 | 2015-12-30 00:00:00 |
| Cuddalore   |        761 | District Environmental Engineer Office, Imperial Road, Cuddalore | Residential, Rural and other Areas |              5 |                   394 |          394 |                 386 |                 391 |                  392 |                   21 |                   98   |                   99.2 |                    99.5 |                     5.3 | 2011-01-02 00:00:00 | 2015-12-31 00:00:00 |
| Chennai     |        160 | NEERI, CSIR Campus Chennai                                       | Residential, Rural and other Areas |              5 |                   382 |          382 |                 374 |                 371 |                  379 |                    9 |                   97.9 |                   97.1 |                    99.2 |                     2.4 | 2011-01-05 00:00:00 | 2015-12-30 00:00:00 |
| Thoothukudi |        239 | Fisheries College, Tuticorin                                     | Residential, Rural and other Areas |              5 |                   374 |          374 |                 369 |                 369 |                  371 |                   58 |                   98.7 |                   98.7 |                    99.2 |                    15.5 | 2011-01-02 00:00:00 | 2015-10-29 00:00:00 |
| Madurai     |        306 | Highway (Project -I) Building, Madurai                           | Residential, Rural and other Areas |              5 |                   370 |          370 |                 364 |                 364 |                  366 |                    3 |                   98.4 |                   98.4 |                    98.9 |                     0.8 | 2011-01-11 00:00:00 | 2015-12-31 00:00:00 |
| Cuddalore   |        760 | SIPCOT Industrial Complex, Cuddalore                             | Industrial Area                    |              5 |                   367 |          367 |                 356 |                 356 |                  367 |                   13 |                   97   |                   97   |                   100   |                     3.5 | 2011-01-08 00:00:00 | 2015-12-29 00:00:00 |
| Salem       |        309 | Sowdeswari College Building, Salem                               | Residential, Rural and other Areas |              5 |                   367 |          367 |                 361 |                 360 |                  365 |                   40 |                   98.4 |                   98.1 |                    99.5 |                    10.9 | 2011-01-05 00:00:00 | 2015-12-30 00:00:00 |
| Chennai     |        764 | Adyar, Chennai                                                   | Residential, Rural and other Areas |              5 |                   365 |          365 |                 358 |                 359 |                  363 |                   48 |                   98.1 |                   98.4 |                    99.5 |                    13.2 | 2011-01-02 00:00:00 | 2015-12-30 00:00:00 |

*Showing preview of first 15 of 31 rows. Complete results saved in `outputs/data_coverage.csv`.*

### 7. Yearly Pollution Trends
- **Output File:** `outputs/yearly_pollution_trends.csv`
- **Total Rows:** 5

|   data_year |   total_records |   active_cities |   active_stations |   distinct_sampling_dates |   valid_so2_count |   avg_so2 |   median_so2 |   valid_no2_count |   avg_no2 |   median_no2 |   valid_pm10_count |   avg_pm10 |   median_pm10 |   valid_pm25_count |   avg_pm25 |   median_pm25 |
|------------:|----------------:|----------------:|------------------:|--------------------------:|------------------:|----------:|-------------:|------------------:|----------:|-------------:|-------------------:|-----------:|--------------:|-------------------:|-----------:|--------------:|
|        2011 |            2232 |               8 |                31 |                       121 |              2182 |      9.63 |          9.6 |              2182 |     19.09 |         19.2 |               2218 |      54.91 |          55.4 |                  0 |     nan    |           nan |
|        2012 |            2270 |               8 |                31 |                       122 |              2212 |      9.89 |          9.9 |              2228 |     19.56 |         19.6 |               2239 |      55.87 |          55.7 |                  0 |     nan    |           nan |
|        2013 |            2158 |               8 |                31 |                       121 |              2111 |     10.11 |         10   |              2115 |     19.88 |         19.8 |               2138 |      56.83 |          57.1 |                  0 |     nan    |           nan |
|        2014 |            2224 |               8 |                31 |                       121 |              2172 |     10.37 |         10.4 |              2163 |     20.48 |         20.7 |               2198 |      58.31 |          58.4 |                223 |      29.73 |            29 |
|        2015 |            2302 |               8 |                31 |                       281 |              2281 |     10.66 |         11   |              2277 |     21.33 |         21   |               2295 |      61.3  |          53   |                454 |      29.55 |            25 |
