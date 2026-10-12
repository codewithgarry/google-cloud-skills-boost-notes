# Build and Optimize Data Warehouses with BigQuery: Challenge Lab (GSP340)

![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?logo=googlecloud&logoColor=white)
![Lab](https://img.shields.io/badge/Lab-GSP340-34A853)
![BigQuery](https://img.shields.io/badge/BigQuery-669DF6?logo=googlebigquery&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?logo=mysql&logoColor=white)

Reference solution for the Google Cloud Skills Boost challenge lab **Build and Optimize Data Warehouses with BigQuery** (GSP340).

## 📖 Overview

You build a **date-partitioned** COVID-19 table and enrich it with data from other public datasets:

- Population from the ECDC dataset.
- Country area from the US Census Bureau dataset.
- Average mobility changes, stored as a nested **STRUCT**, from the Google Mobility Report.

## 🧰 Services used

BigQuery · Partitioned tables · `STRUCT` columns · DML (`ALTER`, `UPDATE`) · BigQuery public datasets

## ✅ Prerequisites

Create a dataset named `ecommerce`, or use the name from your lab:

```bash
bq mk ecommerce
```

Run the queries below in the **BigQuery console** query editor.

## 🚀 Solution

### Task 1: Create a table partitioned by date

```sql
CREATE OR REPLACE TABLE ecommerce.oxford_policy_tracker
PARTITION BY date
OPTIONS (
  partition_expiration_days = 90,
  description = "Oxford policy tracker table partitioned by date"
) AS
SELECT *
FROM `bigquery-public-data.covid19_govt_response.oxford_policy_tracker`
WHERE alpha_3_code NOT IN ('USA', 'GBR');
```

> Use the table name and the excluded country codes listed in your lab.

### Task 2: Add new columns

```sql
ALTER TABLE ecommerce.oxford_policy_tracker
ADD COLUMN IF NOT EXISTS population INT64,
ADD COLUMN IF NOT EXISTS country_area FLOAT64,
ADD COLUMN IF NOT EXISTS mobility STRUCT<
  avg_retail      FLOAT64,
  avg_grocery     FLOAT64,
  avg_parks       FLOAT64,
  avg_transit     FLOAT64,
  avg_workplace   FLOAT64,
  avg_residential FLOAT64
>;
```

### Task 3: Populate country population

```sql
UPDATE ecommerce.oxford_policy_tracker t0
SET population = t2.pop_data_2019
FROM (
  SELECT DISTINCT country_territory_code, pop_data_2019
  FROM `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide`
) AS t2
WHERE t0.alpha_3_code = t2.country_territory_code;
```

### Task 4: Populate country area

```sql
UPDATE ecommerce.oxford_policy_tracker t0
SET country_area = t1.country_area
FROM `bigquery-public-data.census_bureau_international.country_names_area` AS t1
WHERE t0.country_name = t1.country_name;
```

### Task 5: Populate the mobility record

```sql
UPDATE ecommerce.oxford_policy_tracker t0
SET mobility = STRUCT(
  t1.avg_retail, t1.avg_grocery, t1.avg_parks,
  t1.avg_transit, t1.avg_workplace, t1.avg_residential
)
FROM (
  SELECT
    country_region,
    date,
    AVG(retail_and_recreation_percent_change_from_baseline) AS avg_retail,
    AVG(grocery_and_pharmacy_percent_change_from_baseline)  AS avg_grocery,
    AVG(parks_percent_change_from_baseline)                 AS avg_parks,
    AVG(transit_stations_percent_change_from_baseline)      AS avg_transit,
    AVG(workplaces_percent_change_from_baseline)            AS avg_workplace,
    AVG(residential_percent_change_from_baseline)           AS avg_residential
  FROM `bigquery-public-data.covid19_google_mobility.mobility_report`
  GROUP BY country_region, date
) AS t1
WHERE t0.country_name = t1.country_region
  AND t0.date = t1.date;
```

### Task 6: Find countries with missing data

```sql
SELECT DISTINCT country_name
FROM ecommerce.oxford_policy_tracker
WHERE population IS NULL
UNION ALL
SELECT DISTINCT country_name
FROM ecommerce.oxford_policy_tracker
WHERE country_area IS NULL
ORDER BY country_name ASC;
```

## 💡 Key concepts

- **Partitioning by date** lets BigQuery scan only the partitions a query needs, which cuts cost.
- **`partition_expiration_days`** removes old partitions automatically.
- A **`STRUCT`** column groups related fields, which keeps wide tables readable.

---

## ⚠️ Notes

- Resource names, zones, regions and ports are generated per lab session. Always use the values shown in **your** lab instructions.
- These steps were written when the lab was live. Google revises labs over time, so the current version may differ.

## 📌 Disclaimer

This repository is a study reference. Attempt the lab on your own first, then compare approaches. It is not affiliated with or endorsed by Google.

## 👤 Author

**Girish Sharma** · Cloud & DevOps Engineer · [GitHub](https://github.com/codewithgarry) · [LinkedIn](https://www.linkedin.com/in/codewithgarry/)
