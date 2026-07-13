# databricks-medallion-pipeline


# 🚀 Databricks Medallion Architecture Data Pipeline

## 📌 Project Overview
This project is a **Mini Data Engineering Pipeline** that implements the industry-standard **Medallion Architecture** (Bronze, Silver, Gold layers) using **Databricks**, **PySpark**, and **Delta Lake**. 

It demonstrates how to ingest raw data, apply data quality checks and transformations, and finally aggregate the data into a business-ready format. The entire pipeline is designed to be orchestrated using **Databricks Workflows (Jobs)**.

## 🏗️ Architecture: The Medallion Approach

1. **🥉 Bronze Layer (Raw):** 
   - Ingests raw CSV data from the source (DBFS/Cloud Storage) into a Delta Table.
   - Appends an `ingestion_timestamp` to keep a raw historical record without applying any filters.

2. **🥈 Silver Layer (Cleansed & Transformed):**
   - Reads data from the Bronze table.
   - **Transformations applied:**
     - Dropped rows with missing `order_id` or `customer_id`.
     - Filtered out negative product quantities.
     - Created a new derived column `total_amount` (`quantity * product_price`).
   - Saved as a reliable Delta Table ready for ad-hoc querying.

3. **🥇 Gold Layer (Business Aggregates):**
   - Reads the cleansed Silver data.
   - Aggregates the data to calculate `daily_revenue` and `total_orders` grouped by `order_date` and `product_category`.
   - Saved as an optimized Delta Table ready for BI tools (e.g., Tableau, PowerBI) and business reporting.
  
## 📊 Business Insights & Analytics (Gold Layer)
Once the pipeline runs successfully, data is ready for BI consumption. Here is an example of an analytical query running on top of the Gold Layer:

| category    | total_revenue | total_orders | average_order_value |
|-------------|---------------|--------------|---------------------|
| Electronics | 1948.99       | 4            | 487.25              |
| Home        | 314.98        | 3            | 104.99              |
| Clothing    | 159.98        | 3            | 53.33               |
| Books       | 64.90         | 2            | 32.45               |

### 🛠️ Production Best Practices Implemented
* **Idempotency:** The Silver and Gold layers use `overwrite` mode, ensuring that rerunning the pipeline with the same data won't create duplicates.
* **Data Lineage:** Added `ingestion_time` and `source_file_name` in the Bronze layer for strict auditability.

## ⚙️ Tech Stack
* **Compute & Processing:** Databricks, Apache Spark (PySpark)
* **Storage format:** Delta Lake
* **Orchestration:** Databricks Workflows (Jobs)
* **Language:** Python

## 🚀 How to Run in Databricks

1. Clone this repository into your Databricks Workspace.
2. Upload the sample data (`raw_ecommerce_sales.csv`) to DBFS or your cloud storage.
3. Open **Databricks Workflows**.
4. Create a new Job and add three sequential tasks:
   - **Task 1:** Run `01_bronze_ingestion`
   - **Task 2:** Run `02_silver_transformation` (Depends on Task 1)
   - **Task 3:** Run `03_gold_aggregation` (Depends on Task 2)
5. Run the workflow and monitor the job execution.
