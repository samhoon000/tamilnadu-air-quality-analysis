# Tamil Nadu Air Quality - SQL Analytical Query Results

This document contains the execution results of the 6 core analytical questions and the multi-year trend analysis executed directly against DuckDB (`data/air_quality.duckdb`).

## Execution Summary

| # | Analysis | Output File | Rows Returned | Status |
|---|---|---|---:|---:|
| 1 | Monthly Pollution Trends | [`monthly_pollution_trends.csv`](../outputs/monthly_pollution_trends.csv) | 48 | SUCCESS |
| 2 | City Pollution Comparison | [`city_pollution_comparison.csv`](../outputs/city_pollution_comparison.csv) | 32 | SUCCESS |
| 3 | Station Hotspots | [`station_hotspots.csv`](../outputs/station_hotspots.csv) | 128 | SUCCESS |
| 4 | Location Type Comparison | [`location_type_comparison.csv`](../outputs/location_type_comparison.csv) | 8 | SUCCESS |
| 5 | Extreme Pollution Events | [`extreme_pollution_events.csv`](../outputs/extreme_pollution_events.csv) | 48 | SUCCESS |
| 6 | Data Coverage | [`data_coverage.csv`](../outputs/data_coverage.csv) | 32 | SUCCESS |
| 7 | Yearly Pollution Trends | [`yearly_pollution_trends.csv`](../outputs/yearly_pollution_trends.csv) | 5 | SUCCESS |

## Query Outputs & Analytical Previews

### 1. Monthly Pollution Trends
- **Output File:** `outputs/monthly_pollution_trends.csv`
- **Total Rows:** 48

| pollutant   |   month_number | month_name   |   valid_observations |   years_represented |   active_cities |   active_stations |   mean_concentration |   median_concentration |   monthly_rank_by_mean |
|:------------|---------------:|:-------------|---------------------:|--------------------:|----------------:|------------------:|---------------------:|-----------------------:|-----------------------:|
| NO2         |              1 | January      |                  812 |                   5 |               8 |                30 |                21.49 |                     21 |                      9 |
| NO2         |              2 | February     |                  886 |                   5 |               8 |                30 |                20.87 |                     21 |                     11 |
| NO2         |              3 | March        |                  968 |                   5 |               8 |                30 |                20.99 |                     21 |                     10 |
| NO2         |              4 | April        |                  881 |                   5 |               8 |                31 |                22.34 |                     21 |                      2 |
| NO2         |              5 | May          |                  972 |                   5 |               8 |                30 |                22.63 |                     22 |                      1 |
| NO2         |              6 | June         |                  866 |                   5 |               8 |                30 |                21.96 |                     21 |                      4 |
| NO2         |              7 | July         |                  935 |                   5 |               8 |                31 |                21.67 |                     21 |                      6 |
| NO2         |              8 | August       |                  950 |                   5 |               8 |                31 |                22.07 |                     21 |                      3 |
| NO2         |              9 | September    |                  747 |                   5 |               8 |                30 |                21.5  |                     20 |                      8 |
| NO2         |             10 | October      |                  923 |                   5 |               8 |                31 |                21.62 |                     21 |                      7 |
| NO2         |             11 | November     |                  934 |                   5 |               8 |                31 |                21.75 |                     20 |                      5 |
| NO2         |             12 | December     |                  906 |                   5 |               8 |                31 |                20.82 |                     20 |                     12 |
| PM10        |              1 | January      |                  813 |                   5 |               8 |                30 |                69.11 |                     58 |                      5 |
| PM10        |              2 | February     |                  885 |                   5 |               8 |                30 |                68.52 |                     58 |                      7 |
| PM10        |              3 | March        |                  971 |                   5 |               8 |                30 |                71    |                     60 |                      1 |

*Showing preview of first 15 of 48 rows. Complete results saved in `outputs/monthly_pollution_trends.csv`.*

### 2. City Pollution Comparison
- **Output File:** `outputs/city_pollution_comparison.csv`
- **Total Rows:** 32

| pollutant   | city        |   valid_observations |   years_monitored |   monitoring_stations |   mean_concentration |   median_concentration |   min_concentration |   max_concentration |   city_rank | meets_30_observation_screen   |
|:------------|:------------|---------------------:|------------------:|----------------------:|---------------------:|-----------------------:|--------------------:|--------------------:|------------:|:------------------------------|
| NO2         | Coimbatore  |                 1345 |                 5 |                     3 |                27.09 |                     25 |                 0   |                 315 |           1 | True                          |
| NO2         | Salem       |                  641 |                 5 |                     1 |                24.77 |                     24 |                 2   |                  55 |           2 | True                          |
| NO2         | Madurai     |                 1408 |                 5 |                     3 |                24.06 |                     23 |                12   |                 274 |           3 | True                          |
| NO2         | Mettur      |                  486 |                 3 |                     2 |                24.04 |                     23 |                13   |                  69 |           4 | True                          |
| NO2         | Chennai     |                 3729 |                 5 |                    11 |                21.14 |                     19 |                 4.5 |                 245 |           5 | True                          |
| NO2         | Cuddalore   |                  647 |                 3 |                     3 |                19.78 |                     21 |                 6   |                  27 |           6 | True                          |
| NO2         | Trichy      |                 1160 |                 4 |                     5 |                18.2  |                     18 |                 9   |                  53 |           7 | True                          |
| NO2         | Thoothukudi |                 1364 |                 5 |                     3 |                16.71 |                     15 |                 7   |                 146 |           8 | True                          |
| PM10        | Thoothukudi |                 1374 |                 5 |                     3 |               104.82 |                     88 |                15   |                 776 |           1 | True                          |
| PM10        | Trichy      |                 1178 |                 4 |                     5 |                84.9  |                     96 |                22   |                 414 |           2 | True                          |
| PM10        | Chennai     |                 3742 |                 5 |                    11 |                64.36 |                     55 |                 3   |                 363 |           3 | True                          |
| PM10        | Coimbatore  |                 1361 |                 5 |                     3 |                61.6  |                     55 |                11   |                 443 |           4 | True                          |
| PM10        | Salem       |                  650 |                 5 |                     1 |                61.1  |                     57 |                19   |                 169 |           5 | True                          |
| PM10        | Cuddalore   |                  651 |                 3 |                     3 |                57.53 |                     56 |                13   |                 114 |           6 | True                          |
| PM10        | Mettur      |                  486 |                 3 |                     2 |                52.04 |                     48 |                17   |                 182 |           7 | True                          |

*Showing preview of first 15 of 32 rows. Complete results saved in `outputs/city_pollution_comparison.csv`.*

### 3. Station Hotspots
- **Output File:** `outputs/station_hotspots.csv`
- **Total Rows:** 128

| pollutant   |   stn_code | city       | location_of_monitoring_station                                   | type_of_location                   | agency                                                |   valid_observations |   distinct_sampling_dates |   years_active |   mean_concentration |   median_concentration |   p90_concentration |   max_concentration |   station_rank | meets_30_observation_screen   |
|:------------|-----------:|:-----------|:-----------------------------------------------------------------|:-----------------------------------|:------------------------------------------------------|---------------------:|--------------------------:|---------------:|---------------------:|-----------------------:|--------------------:|--------------------:|---------------:|:------------------------------|
| NO2         |        237 | Coimbatore | SIDCO Office, Coimbatore                                         | Industrial Area                    | Tamilnadu State Pollution Control Board               |                  451 |                       455 |              5 |                29.68 |                     26 |                  37 |                 315 |              1 | True                          |
| NO2         |        766 | Chennai    | Thiyagaraya Nagar, Chennai                                       | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  305 |                       310 |              3 |                28.77 |                     27 |                  36 |                 118 |              2 | True                          |
| NO2         |        763 | Mettur     | SIDCO Industrial Complex, Mettur                                 | Industrial Area                    | Tamilnadu State Pollution Control Board               |                  243 |                       243 |              3 |                26.67 |                     26 |                  32 |                  69 |              3 | True                          |
| NO2         |        238 | Coimbatore | Distt. Collector's Office, Coimbatore                            | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  450 |                       455 |              5 |                26.64 |                     25 |                  35 |                  75 |              4 | True                          |
| NO2         |        767 | Chennai    | Kilpauk, Chennai                                                 | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  313 |                       305 |              3 |                26.18 |                     26 |                  34 |                  59 |              5 | True                          |
| NO2         |        307 | Madurai    | Fenner (I) Ltd. Employees Assiciation Building Kochadai, Madurai | Industrial Area                    | Tamilnadu State Pollution Control Board               |                  475 |                       475 |              5 |                25.02 |                     24 |                  30 |                 274 |              6 | True                          |
| NO2         |        375 | Coimbatore | Poniarajapuram, On the top of DEL, Coimbatore                    | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  444 |                       467 |              5 |                24.91 |                     22 |                  34 |                  76 |              7 | True                          |
| NO2         |        309 | Salem      | Sowdeswari College Building, Salem                               | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  641 |                       652 |              5 |                24.77 |                     24 |                  31 |                  55 |              8 | True                          |
| NO2         |        308 | Madurai    | Kunnathur Chatram East Avani Mollai Street, Madurai              | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  465 |                       465 |              5 |                24.68 |                     24 |                  30 |                 189 |              9 | True                          |
| NO2         |        306 | Madurai    | Highway (Project -I) Building, Madurai                           | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  468 |                       468 |              5 |                22.48 |                     22 |                  27 |                  49 |             10 | True                          |
| NO2         |        765 | Chennai    | Anna Nagar, Chennai                                              | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  300 |                       302 |              3 |                22.32 |                     21 |                  30 |                  59 |             11 | True                          |
| NO2         |        762 | Mettur     | Raman Nagar, Mettur                                              | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  243 |                       243 |              3 |                21.4  |                     21 |                  26 |                  45 |             12 | True                          |
| NO2         |        759 | Cuddalore  | Eachangadu Villagae                                              | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  215 |                       217 |              3 |                21.17 |                     22 |                  25 |                  26 |             13 | True                          |
| NO2         |        161 | Chennai    | Thiruvottiyur Municipal Office, Chennai                          | Industrial Area                    | National Environmental Engineering Research Institute |                  355 |                       359 |              4 |                20.57 |                     19 |                  36 |                  67 |             14 | True                          |
| NO2         |        773 | Trichy     | Central Bus Stand, Trichy                                        | Residential, Rural and other Areas | Tamilnadu State Pollution Control Board               |                  232 |                       236 |              4 |                20.51 |                     20 |                  23 |                  33 |             15 | True                          |

*Showing preview of first 15 of 128 rows. Complete results saved in `outputs/station_hotspots.csv`.*

### 4. Location Type Comparison
- **Output File:** `outputs/location_type_comparison.csv`
- **Total Rows:** 8

| type_of_location                   | pollutant   |   total_records |   valid_observations |   missing_observations |   missing_pct |   stations_represented |   cities_represented |   mean_concentration |   median_concentration |   stddev_concentration |   max_concentration |
|:-----------------------------------|:------------|----------------:|---------------------:|-----------------------:|--------------:|-----------------------:|---------------------:|---------------------:|-----------------------:|-----------------------:|--------------------:|
| Industrial Area                    | NO2         |            3613 |                 3595 |                     18 |          0.5  |                      9 |                    6 |                22    |                   21   |                  12.4  |                 315 |
| Residential, Rural and other Areas | NO2         |            7277 |                 7185 |                     92 |          1.26 |                     22 |                    8 |                21.48 |                   21   |                   7.98 |                 189 |
| Industrial Area                    | PM10        |            3613 |                 3598 |                     15 |          0.42 |                      9 |                    6 |                68.54 |                   54   |                  51.14 |                 601 |
| Residential, Rural and other Areas | PM10        |            7277 |                 7252 |                     25 |          0.34 |                     22 |                    8 |                67.87 |                   57   |                  39.26 |                 776 |
| Industrial Area                    | PM2.5       |            3613 |                  151 |                   3462 |         95.82 |                      9 |                    6 |                29.68 |                   27.9 |                  10.86 |                  82 |
| Residential, Rural and other Areas | PM2.5       |            7277 |                  303 |                   6974 |         95.84 |                     22 |                    8 |                29.49 |                   24   |                  19.08 |                 141 |
| Industrial Area                    | SO2         |            3613 |                 3594 |                     19 |          0.53 |                      9 |                    6 |                12.03 |                   12   |                  16.21 |                 909 |
| Residential, Rural and other Areas | SO2         |            7277 |                 7182 |                     95 |          1.31 |                     22 |                    8 |                10.56 |                   10   |                   5.33 |                  70 |

### 5. Extreme Pollution Events
- **Output File:** `outputs/extreme_pollution_events.csv`
- **Total Rows:** 48

| pollutant   |   peak_rank |   data_year | sampling_date       | city        |   stn_code | location_of_monitoring_station                                   | type_of_location                   |   recorded_concentration |
|:------------|------------:|------------:|:--------------------|:------------|-----------:|:-----------------------------------------------------------------|:-----------------------------------|-------------------------:|
| NO2         |           1 |        2011 | 2011-04-01 00:00:00 | Coimbatore  |        237 | SIDCO Office, Coimbatore                                         | Industrial Area                    |                      315 |
| NO2         |           2 |        2011 | 2011-05-20 00:00:00 | Coimbatore  |        237 | SIDCO Office, Coimbatore                                         | Industrial Area                    |                      303 |
| NO2         |           3 |        2011 | 2011-08-17 00:00:00 | Madurai     |        307 | Fenner (I) Ltd. Employees Assiciation Building Kochadai, Madurai | Industrial Area                    |                      274 |
| NO2         |           4 |        2011 | 2011-07-02 00:00:00 | Chennai     |         71 | Govt. High School, Manali, Chennai.                              | Industrial Area                    |                      245 |
| NO2         |           5 |        2011 | 2011-05-08 00:00:00 | Madurai     |        308 | Kunnathur Chatram East Avani Mollai Street, Madurai              | Residential, Rural and other Areas |                      189 |
| NO2         |           6 |        2011 | 2011-06-07 00:00:00 | Thoothukudi |        240 | Raja Agencies, Tuticorin                                         | Industrial Area                    |                      146 |
| NO2         |           7 |        2013 | 2013-01-29 00:00:00 | Chennai     |        766 | Thiyagaraya Nagar, Chennai                                       | Residential, Rural and other Areas |                      118 |
| NO2         |           8 |        2012 | 2012-12-26 00:00:00 | Chennai     |        160 | NEERI, CSIR Campus Chennai                                       | Residential, Rural and other Areas |                      117 |
| NO2         |           9 |        2011 | 2011-09-27 00:00:00 | Coimbatore  |        237 | SIDCO Office, Coimbatore                                         | Industrial Area                    |                      111 |
| NO2         |          10 |        2011 | 2011-09-23 00:00:00 | Coimbatore  |        237 | SIDCO Office, Coimbatore                                         | Industrial Area                    |                      107 |
| PM10        |           1 |        2011 | 2011-08-29 00:00:00 | Thoothukudi |        239 | Fisheries College, Tuticorin                                     | Residential, Rural and other Areas |                      776 |
| PM10        |           2 |        2011 | 2011-05-15 00:00:00 | Thoothukudi |        240 | Raja Agencies, Tuticorin                                         | Industrial Area                    |                      601 |
| PM10        |           3 |        2011 | 2011-06-04 00:00:00 | Thoothukudi |        240 | Raja Agencies, Tuticorin                                         | Industrial Area                    |                      597 |
| PM10        |           4 |        2012 | 2012-10-18 00:00:00 | Thoothukudi |        239 | Fisheries College, Tuticorin                                     | Residential, Rural and other Areas |                      551 |
| PM10        |           5 |        2011 | 2011-07-12 00:00:00 | Thoothukudi |        240 | Raja Agencies, Tuticorin                                         | Industrial Area                    |                      516 |

*Showing preview of first 15 of 48 rows. Complete results saved in `outputs/extreme_pollution_events.csv`.*

### 6. Data Coverage
- **Output File:** `outputs/data_coverage.csv`
- **Total Rows:** 32

| city        |   stn_code | location_of_monitoring_station                                   | type_of_location                   |   years_active |   total_sampling_days |   total_rows |   valid_so2_samples |   valid_no2_samples |   valid_pm10_samples |   valid_pm25_samples |   so2_completeness_pct |   no2_completeness_pct |   pm10_completeness_pct |   pm25_completeness_pct | earliest_date       | latest_date         |
|:------------|-----------:|:-----------------------------------------------------------------|:-----------------------------------|---------------:|----------------------:|-------------:|--------------------:|--------------------:|---------------------:|---------------------:|-----------------------:|-----------------------:|------------------------:|------------------------:|:--------------------|:--------------------|
| Salem       |        309 | Sowdeswari College Building, Salem                               | Residential, Rural and other Areas |              5 |                   652 |          652 |                 641 |                 641 |                  650 |                   27 |                   98.3 |                   98.3 |                    99.7 |                     4.1 | 2011-01-04 00:00:00 | 2015-12-30 00:00:00 |
| Madurai     |        307 | Fenner (I) Ltd. Employees Assiciation Building Kochadai, Madurai | Industrial Area                    |              5 |                   475 |          475 |                 475 |                 475 |                  475 |                   22 |                  100   |                  100   |                   100   |                     4.6 | 2011-01-06 00:00:00 | 2015-12-30 00:00:00 |
| Chennai     |         38 | Kathivakkam, Municipal Kalyana Mandapam, Chennai                 | Industrial Area                    |              5 |                   474 |          474 |                 472 |                 472 |                  472 |                   65 |                   99.6 |                   99.6 |                    99.6 |                    13.7 | 2011-01-02 00:00:00 | 2015-12-31 00:00:00 |
| Chennai     |         71 | Govt. High School, Manali, Chennai.                              | Industrial Area                    |              5 |                   469 |          469 |                 469 |                 469 |                  464 |                    0 |                  100   |                  100   |                    98.9 |                     0   | 2011-01-08 00:00:00 | 2015-12-31 00:00:00 |
| Madurai     |        306 | Highway (Project -I) Building, Madurai                           | Residential, Rural and other Areas |              5 |                   468 |          468 |                 468 |                 468 |                  468 |                    0 |                  100   |                  100   |                   100   |                     0   | 2011-01-08 00:00:00 | 2015-12-31 00:00:00 |
| Coimbatore  |        375 | Poniarajapuram, On the top of DEL, Coimbatore                    | Residential, Rural and other Areas |              5 |                   467 |          468 |                 437 |                 444 |                  460 |                   45 |                   93.4 |                   94.9 |                    98.3 |                     9.6 | 2011-01-04 00:00:00 | 2015-12-30 00:00:00 |
| Madurai     |        308 | Kunnathur Chatram East Avani Mollai Street, Madurai              | Residential, Rural and other Areas |              5 |                   465 |          465 |                 465 |                 465 |                  465 |                    0 |                  100   |                  100   |                   100   |                     0   | 2011-01-02 00:00:00 | 2015-12-29 00:00:00 |
| Thoothukudi |        240 | Raja Agencies, Tuticorin                                         | Industrial Area                    |              5 |                   461 |          462 |                 460 |                 460 |                  460 |                    0 |                   99.6 |                   99.6 |                    99.6 |                     0   | 2011-01-06 00:00:00 | 2015-10-31 00:00:00 |
| Thoothukudi |        366 | AVM Jewellery Building, Tuticorin                                | Residential, Rural and other Areas |              5 |                   458 |          458 |                 454 |                 453 |                  458 |                    0 |                   99.1 |                   98.9 |                   100   |                     0   | 2011-01-02 00:00:00 | 2015-10-30 00:00:00 |
| Thoothukudi |        239 | Fisheries College, Tuticorin                                     | Residential, Rural and other Areas |              5 |                   457 |          457 |                 450 |                 451 |                  456 |                   51 |                   98.5 |                   98.7 |                    99.8 |                    11.2 | 2011-01-08 00:00:00 | 2015-10-29 00:00:00 |
| Coimbatore  |        237 | SIDCO Office, Coimbatore                                         | Industrial Area                    |              5 |                   455 |          456 |                 450 |                 451 |                  451 |                   38 |                   98.7 |                   98.9 |                    98.9 |                     8.3 | 2011-01-02 00:00:00 | 2015-12-29 00:00:00 |
| Coimbatore  |        238 | Distt. Collector's Office, Coimbatore                            | Residential, Rural and other Areas |              5 |                   455 |          455 |                 450 |                 450 |                  450 |                   42 |                   98.9 |                   98.9 |                    98.9 |                     9.2 | 2011-01-08 00:00:00 | 2015-12-31 00:00:00 |
| Chennai     |         72 | Thiruvottiyur,  Chennai                                          | Industrial Area                    |              4 |                   373 |          373 |                 371 |                 371 |                  372 |                    0 |                   99.5 |                   99.5 |                    99.7 |                     0   | 2011-01-04 00:00:00 | 2014-12-31 00:00:00 |
| Chennai     |        160 | NEERI, CSIR Campus Chennai                                       | Residential, Rural and other Areas |              4 |                   365 |          366 |                 363 |                 363 |                  365 |                    0 |                   99.2 |                   99.2 |                    99.7 |                     0   | 2011-01-08 00:00:00 | 2015-12-30 00:00:00 |
| Chennai     |        159 | Madras Medical College, Chennai                                  | Residential, Rural and other Areas |              4 |                   360 |          360 |                 355 |                 355 |                  359 |                    0 |                   98.6 |                   98.6 |                    99.7 |                     0   | 2011-01-02 00:00:00 | 2015-12-30 00:00:00 |

*Showing preview of first 15 of 32 rows. Complete results saved in `outputs/data_coverage.csv`.*

### 7. Yearly Pollution Trends
- **Output File:** `outputs/yearly_pollution_trends.csv`
- **Total Rows:** 5

|   data_year |   total_records |   active_cities |   active_stations |   distinct_sampling_dates |   valid_so2_count |   avg_so2 |   median_so2 |   valid_no2_count |   avg_no2 |   median_no2 |   valid_pm10_count |   avg_pm10 |   median_pm10 |   valid_pm25_count |   avg_pm25 |   median_pm25 |
|------------:|----------------:|----------------:|------------------:|--------------------------:|------------------:|----------:|-------------:|------------------:|----------:|-------------:|-------------------:|-----------:|--------------:|-------------------:|-----------:|--------------:|
|        2011 |            1569 |               5 |                16 |                       303 |              1561 |     10.29 |            8 |              1561 |     22.24 |           21 |               1561 |      78.19 |            56 |                  0 |     nan    |           nan |
|        2012 |            1734 |               6 |                21 |                       304 |              1702 |     10.43 |            9 |              1704 |     20.66 |           20 |               1723 |      72.47 |            60 |                  0 |     nan    |           nan |
|        2013 |            2406 |               8 |                27 |                       299 |              2364 |     11.81 |           12 |              2372 |     21.7  |           20 |               2396 |      71.6  |            60 |                  0 |     nan    |           nan |
|        2014 |            2879 |               8 |                30 |                       302 |              2868 |     11.5  |           12 |              2866 |     22.14 |           22 |               2875 |      62.49 |            55 |                  0 |     nan    |           nan |
|        2015 |            2302 |               8 |                31 |                       281 |              2281 |     10.66 |           11 |              2277 |     21.33 |           21 |               2295 |      61.3  |            53 |                454 |      29.55 |            25 |
