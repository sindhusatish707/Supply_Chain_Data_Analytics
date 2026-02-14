# End-to-End Supply Chain Optimization Pipeline
## From Local Infrastructure to Cloud Analytics

### 📌 Project Overview
A comprehensive Data Engineering pipeline designed to optimize warehouse efficiency and identify financial risk. This project automates the journey of 180k+ records of messy, legacy ERP data through a Medallion Architecture, moving from local containerized environments to a cloud-native BigQuery warehouse for executive-level storytelling.

### 🏗️ Architecture & Stack
- **Ingestion:** Python (SQLAlchemy/Pandas) extracting from legacy CSV into **PostgreSQL**.
- **Infrastructure:** **Docker** for local database containerization and environment isolation.
- **Cloud Warehouse:** **Google BigQuery** (Gold Layer) for high-performance analytical storage.
- **Statistical Modeling:** Advanced SQL (CTEs, Window Functions) to calculate Lead Time Volatility and Revenue at Risk.
- **Visualization:** **Tableau** for interactive financial risk and profitability heatmaps.

### 📈 Key Analytical Insights
- **Revenue at Risk:** Quantified potential losses by cross-referencing late delivery status with total sales volume.
- **Profit Volatility Score:** Utilized the **Coefficient of Variation (CV)** to normalize financial risk across disparate product categories and shipping modes.
- **Lead Time Reliability:** Analyzed the standard deviation between scheduled and real shipping dates to identify logistical bottlenecks.

### 🛠️ How to Run
1. **Local Setup:** `docker-compose up -d` to spin up the Postgres instance.
2. **Data Audit:** Run `data_audit.py` for initial distribution analysis and outlier detection.
3. **Cleaning & Ingestion:** Execute `data_cleaning.py` to handle type-casting and schema standardization.
4. **Cloud Migration:** Run `pipeline_to_cloud.py` to push cleaned datasets to BigQuery using Service Account credentials.
