-- ============================================================================
-- Tamil Nadu Ambient Air Quality - Multi-Year Analytical Queries
-- Database: DuckDB (air_quality table)
-- 
-- Principles:
-- 1. Preserves genuine missingness (NULL), never treats missing as zero.
-- 2. Includes observation counts alongside averages to prevent sample size bias.
-- 3. Distinguishes pollutant concentrations; does not conflate raw values with AQI.
-- 4. Accounts for structural differences across years (e.g., historical PM2.5 absence).
-- ============================================================================


-- ============================================================================
-- 1. MONTHLY POLLUTION PATTERNS
-- Question: Which months recorded the highest average concentration of each pollutant?
-- ============================================================================
-- Query Name: monthly_pollution_trends
WITH monthly_stats AS (
    SELECT
        EXTRACT(MONTH FROM sampling_date) AS month_number,
        strftime(sampling_date, '%B') AS month_name,
        pollutant,
        COUNT(concentration) AS valid_observations,
        COUNT(DISTINCT data_year) AS years_represented,
        COUNT(DISTINCT city) FILTER (WHERE concentration IS NOT NULL) AS active_cities,
        COUNT(DISTINCT stn_code) FILTER (WHERE concentration IS NOT NULL) AS active_stations,
        ROUND(AVG(concentration), 2) AS mean_concentration,
        ROUND(quantile_cont(concentration, 0.50), 2) AS median_concentration
    FROM air_quality
    CROSS JOIN LATERAL (
        VALUES
            ('SO2', so2),
            ('NO2', no2),
            ('PM10', rspm_pm10),
            ('PM2.5', pm_2_5)
    ) AS p(pollutant, concentration)
    GROUP BY month_number, month_name, pollutant
)
SELECT
    pollutant,
    month_number,
    month_name,
    valid_observations,
    years_represented,
    active_cities,
    active_stations,
    mean_concentration,
    median_concentration,
    RANK() OVER (PARTITION BY pollutant ORDER BY mean_concentration DESC NULLS LAST) AS monthly_rank_by_mean
FROM monthly_stats
ORDER BY pollutant, month_number;


-- ============================================================================
-- 2. CITY-LEVEL POLLUTION COMPARISON
-- Question: Which cities/areas recorded the highest average pollution?
-- (Includes a minimum 30-observation screening floor for reliability)
-- ============================================================================
-- Query Name: city_pollution_comparison
WITH city_stats AS (
    SELECT
        city,
        pollutant,
        COUNT(*) AS total_records,
        COUNT(concentration) AS valid_observations,
        COUNT(*) FILTER (WHERE concentration IS NULL) AS missing_observations,
        COUNT(DISTINCT data_year) AS years_monitored,
        COUNT(DISTINCT stn_code) FILTER (WHERE concentration IS NOT NULL) AS monitoring_stations,
        ROUND(AVG(concentration), 2) AS mean_concentration,
        ROUND(quantile_cont(concentration, 0.50), 2) AS median_concentration,
        ROUND(MIN(concentration), 2) AS min_concentration,
        ROUND(MAX(concentration), 2) AS max_concentration
    FROM air_quality
    CROSS JOIN LATERAL (
        VALUES
            ('SO2', so2),
            ('NO2', no2),
            ('PM10', rspm_pm10),
            ('PM2.5', pm_2_5)
    ) AS p(pollutant, concentration)
    GROUP BY city, pollutant
)
SELECT
    pollutant,
    city,
    valid_observations,
    years_monitored,
    monitoring_stations,
    mean_concentration,
    median_concentration,
    min_concentration,
    max_concentration,
    RANK() OVER (PARTITION BY pollutant ORDER BY mean_concentration DESC NULLS LAST) AS city_rank,
    (valid_observations >= 30) AS meets_30_observation_screen
FROM city_stats
ORDER BY pollutant, mean_concentration DESC NULLS LAST, city;


-- ============================================================================
-- 3. MONITORING STATION HOTSPOTS
-- Question: Which monitoring stations recorded the highest pollution?
-- ============================================================================
-- Query Name: station_hotspots
WITH station_stats AS (
    SELECT
        stn_code,
        city,
        location_of_monitoring_station,
        type_of_location,
        agency,
        pollutant,
        COUNT(*) AS total_records,
        COUNT(concentration) AS valid_observations,
        COUNT(DISTINCT sampling_date) AS distinct_sampling_dates,
        COUNT(DISTINCT data_year) AS years_active,
        ROUND(AVG(concentration), 2) AS mean_concentration,
        ROUND(quantile_cont(concentration, 0.50), 2) AS median_concentration,
        ROUND(quantile_cont(concentration, 0.90), 2) AS p90_concentration,
        ROUND(MAX(concentration), 2) AS max_concentration
    FROM air_quality
    CROSS JOIN LATERAL (
        VALUES
            ('SO2', so2),
            ('NO2', no2),
            ('PM10', rspm_pm10),
            ('PM2.5', pm_2_5)
    ) AS p(pollutant, concentration)
    GROUP BY stn_code, city, location_of_monitoring_station, type_of_location, agency, pollutant
)
SELECT
    pollutant,
    stn_code,
    city,
    location_of_monitoring_station,
    type_of_location,
    agency,
    valid_observations,
    distinct_sampling_dates,
    years_active,
    mean_concentration,
    median_concentration,
    p90_concentration,
    max_concentration,
    RANK() OVER (PARTITION BY pollutant ORDER BY mean_concentration DESC NULLS LAST) AS station_rank,
    (valid_observations >= 30) AS meets_30_observation_screen
FROM station_stats
ORDER BY pollutant, mean_concentration DESC NULLS LAST, valid_observations DESC;


-- ============================================================================
-- 4. LOCATION-TYPE COMPARISON
-- Question: How does pollution differ by monitoring location type?
-- ============================================================================
-- Query Name: location_type_comparison
SELECT
    type_of_location,
    pollutant,
    COUNT(*) AS total_records,
    COUNT(concentration) AS valid_observations,
    COUNT(*) FILTER (WHERE concentration IS NULL) AS missing_observations,
    ROUND(100.0 * COUNT(*) FILTER (WHERE concentration IS NULL) / NULLIF(COUNT(*), 0), 2) AS missing_pct,
    COUNT(DISTINCT stn_code) AS stations_represented,
    COUNT(DISTINCT city) AS cities_represented,
    ROUND(AVG(concentration), 2) AS mean_concentration,
    ROUND(quantile_cont(concentration, 0.50), 2) AS median_concentration,
    ROUND(STDDEV_SAMP(concentration), 2) AS stddev_concentration,
    ROUND(MAX(concentration), 2) AS max_concentration
FROM air_quality
CROSS JOIN LATERAL (
    VALUES
        ('SO2', so2),
        ('NO2', no2),
        ('PM10', rspm_pm10),
        ('PM2.5', pm_2_5)
) AS p(pollutant, concentration)
WHERE type_of_location IS NOT NULL
GROUP BY type_of_location, pollutant
ORDER BY pollutant, mean_concentration DESC;


-- ============================================================================
-- 5. EXTREME POLLUTION OBSERVATIONS
-- Question: What are the highest individual pollution observations recorded?
-- ============================================================================
-- Query Name: extreme_pollution_events
WITH unpivoted_observations AS (
    SELECT
        data_year,
        sampling_date,
        city,
        stn_code,
        location_of_monitoring_station,
        type_of_location,
        pollutant,
        concentration
    FROM air_quality
    CROSS JOIN LATERAL (
        VALUES
            ('SO2', so2),
            ('NO2', no2),
            ('PM10', rspm_pm10),
            ('PM2.5', pm_2_5)
    ) AS p(pollutant, concentration)
    WHERE concentration IS NOT NULL
),
ranked_events AS (
    SELECT
        pollutant,
        data_year,
        sampling_date,
        city,
        stn_code,
        location_of_monitoring_station,
        type_of_location,
        ROUND(concentration, 2) AS recorded_concentration,
        DENSE_RANK() OVER (PARTITION BY pollutant ORDER BY concentration DESC) AS peak_rank
    FROM unpivoted_observations
)
SELECT
    pollutant,
    peak_rank,
    data_year,
    sampling_date,
    city,
    stn_code,
    location_of_monitoring_station,
    type_of_location,
    recorded_concentration
FROM ranked_events
WHERE peak_rank <= 10
ORDER BY pollutant, peak_rank, sampling_date;


-- ============================================================================
-- 6. DATA COVERAGE AND RELIABILITY
-- Question: Which cities/stations have enough data for reliable comparison?
-- ============================================================================
-- Query Name: data_coverage
SELECT
    city,
    stn_code,
    location_of_monitoring_station,
    type_of_location,
    COUNT(DISTINCT data_year) AS years_active,
    COUNT(DISTINCT sampling_date) AS total_sampling_days,
    COUNT(*) AS total_rows,
    COUNT(so2) AS valid_so2_samples,
    COUNT(no2) AS valid_no2_samples,
    COUNT(rspm_pm10) AS valid_pm10_samples,
    COUNT(pm_2_5) AS valid_pm25_samples,
    ROUND(100.0 * COUNT(so2) / NULLIF(COUNT(*), 0), 1) AS so2_completeness_pct,
    ROUND(100.0 * COUNT(no2) / NULLIF(COUNT(*), 0), 1) AS no2_completeness_pct,
    ROUND(100.0 * COUNT(rspm_pm10) / NULLIF(COUNT(*), 0), 1) AS pm10_completeness_pct,
    ROUND(100.0 * COUNT(pm_2_5) / NULLIF(COUNT(*), 0), 1) AS pm25_completeness_pct,
    MIN(sampling_date) AS earliest_date,
    MAX(sampling_date) AS latest_date
FROM air_quality
GROUP BY city, stn_code, location_of_monitoring_station, type_of_location
ORDER BY total_sampling_days DESC, city, stn_code;


-- ============================================================================
-- 7. YEAR-OVER-YEAR POLLUTION TRENDS
-- Multi-year analytical extension: Annual averages alongside coverage metadata.
--
-- METHODOLOGICAL LIMITATION & COMPARABILITY NOTE:
-- * PM2.5 was not routinely monitored prior to 2014; longitudinal trends for PM2.5
--   reflect network introduction, NOT real ambient declines or surges.
-- * Station network and sampling schedules varied across years; averages must
--   always be interpreted alongside valid sample counts and active station counts.
-- ============================================================================
-- Query Name: yearly_pollution_trends
SELECT
    data_year,
    COUNT(*) AS total_records,
    COUNT(DISTINCT city) AS active_cities,
    COUNT(DISTINCT stn_code) AS active_stations,
    COUNT(DISTINCT sampling_date) AS distinct_sampling_dates,
    -- SO2
    COUNT(so2) AS valid_so2_count,
    ROUND(AVG(so2), 2) AS avg_so2,
    ROUND(quantile_cont(so2, 0.50), 2) AS median_so2,
    -- NO2
    COUNT(no2) AS valid_no2_count,
    ROUND(AVG(no2), 2) AS avg_no2,
    ROUND(quantile_cont(no2, 0.50), 2) AS median_no2,
    -- PM10
    COUNT(rspm_pm10) AS valid_pm10_count,
    ROUND(AVG(rspm_pm10), 2) AS avg_pm10,
    ROUND(quantile_cont(rspm_pm10, 0.50), 2) AS median_pm10,
    -- PM2.5
    COUNT(pm_2_5) AS valid_pm25_count,
    ROUND(AVG(pm_2_5), 2) AS avg_pm25,
    ROUND(quantile_cont(pm_2_5, 0.50), 2) AS median_pm25
FROM air_quality
GROUP BY data_year
ORDER BY data_year;
