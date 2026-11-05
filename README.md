# Business Operations & Supply Chain Intelligence Platform

An end-to-end data analytics project built to transform raw e-commerce
data into operational insights. The platform uses **PostgreSQL, Python,
Excel, and Power BI** to explore order performance, delivery delays,
seller performance, customer behavior, and review trends.

> **Dataset note:** This project uses the historical Brazilian
> E-Commerce Public Dataset by Olist. It is an analytical portfolio
> project, not a live shipment-tracking system. Delivery performance is
> measured against the dataset's estimated delivery date, which is used
> as a proxy rather than a verified contractual SLA.

## Table of Contents

-   [Business Problem](#business-problem)
-   [Project Objectives](#project-objectives)
-   [Technology Stack](#technology-stack)
-   [Dataset](#dataset)
-   [Architecture](#architecture)
-   [Data Warehouse Design](#data-warehouse-design)
-   [Key Analytics](#key-analytics)
-   [Power BI Dashboard](#power-bi-dashboard)
-   [Excel Operations Report](#excel-operations-report)
-   [Project Structure](#project-structure)
-   [Setup and Execution](#setup-and-execution)
-   [Data Quality and Assumptions](#data-quality-and-assumptions)
-   [Future Enhancements](#future-enhancements)
-   [Author](#author)
-   [License and Dataset Attribution](#license-and-dataset-attribution)

## Business Problem

E-commerce operations teams need reliable answers to questions such as:

-   How many orders are being placed, delivered, delayed, or cancelled?
-   What proportion of eligible delivered orders arrived on or before
    the estimated delivery date?
-   Which customer regions have the highest number of delayed orders?
-   How do sellers compare in terms of sales value and delivery
    performance?
-   How do review scores vary across customers and orders?
-   Are there data-quality issues that could affect reported KPIs?

This project builds a small analytical data platform to answer these
questions using a structured warehouse and interactive reporting.

## Project Objectives

1.  Ingest raw CSV files into a PostgreSQL staging layer.
2.  Clean, validate, and transform source data into a dimensional
    warehouse.
3.  Build reusable SQL analytics views for operational reporting.
4.  Define and validate business KPIs.
5.  Develop interactive Power BI dashboards.
6.  Create an Excel-based shipment operations report using formulas,
    PivotTables, and charts.
7.  Document assumptions, data quality checks, and business
    recommendations.

## Technology Stack

  -----------------------------------------------------------------------
  Area                                Tools
  ----------------------------------- -----------------------------------
  Database                            PostgreSQL 18

  Database administration             pgAdmin 4

  Data processing                     Python, Pandas, SQLAlchemy

  Data warehouse                      PostgreSQL, dimensional modelling /
                                      star schema

  BI and visualization                Power BI Desktop

  Operational reporting               Microsoft Excel, PivotTables,
                                      formulas, slicers

  Version control                     Git, GitHub
  -----------------------------------------------------------------------

Planned extensions include dbt for transformation testing and
documentation, Prefect for orchestration, and AWS services for cloud
deployment.

## Dataset

**Source:** [Brazilian E-Commerce Public Dataset by Olist on
Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The dataset contains anonymized Brazilian e-commerce orders and related
entities. Source files include:

  -----------------------------------------------------------------------------
  Source file                               Description
  ----------------------------------------- -----------------------------------
  `olist_orders_dataset.csv`                Order status and lifecycle
                                            timestamps

  `olist_order_items_dataset.csv`           Products, sellers, item prices, and
                                            freight

  `olist_customers_dataset.csv`             Customer location and identifiers

  `olist_sellers_dataset.csv`               Seller identifiers and locations

  `olist_products_dataset.csv`              Product attributes and categories

  `olist_order_payments_dataset.csv`        Payment type, installments, and
                                            values

  `olist_order_reviews_dataset.csv`         Review scores and comments

  `olist_geolocation_dataset.csv`           ZIP-code geolocation data

  `product_category_name_translation.csv`   Portuguese-to-English category
                                            mapping
  -----------------------------------------------------------------------------

The original dataset is historical. It does not provide complete
inventory, product acquisition costs, warehouse operating expenses, or
contractual SLA targets. Therefore, this project does **not** claim to
calculate true profit, live inventory, or contractual SLA compliance.

## Architecture

``` text
Olist CSV files
      |
      v
PostgreSQL - staging schema
      |
      v
Data validation and transformation
      |
      v
PostgreSQL - warehouse schema
      |
      +--> Dimension tables
      |
      +--> Fact tables
      |
      v
PostgreSQL - analytics schema
      |
      +--------------------+
      |                    |
      v                    v
Power BI dashboards    Excel operations report
      |
      v
Business insights and recommendations
```

## Data Warehouse Design

The database is organized into three schemas:

-   **`staging`** --- raw source data imported from CSV files. Source
    column names are retained for traceability.
-   **`warehouse`** --- cleaned, structured dimension and fact tables
    used for analysis.
-   **`analytics`** --- SQL views that provide business-ready
    aggregations.

### Dimension tables

  -----------------------------------------------------------------------
  Table                               Purpose
  ----------------------------------- -----------------------------------
  `warehouse.dim_customers`           Customer attributes and location

  `warehouse.dim_sellers`             Seller attributes and location

  `warehouse.dim_products`            Product attributes and translated
                                      categories

  `warehouse.dim_date`                Calendar attributes for date-based
                                      analysis
  -----------------------------------------------------------------------

### Fact tables

  -----------------------------------------------------------------------
  Table                               Grain / purpose
  ----------------------------------- -----------------------------------
  `warehouse.fact_orders`             One row per order; order lifecycle
                                      and delivery measures

  `warehouse.fact_order_items`        One row per order item; product,
                                      seller, price, and freight

  `warehouse.fact_payments`           Payment records associated with
                                      orders

  `warehouse.fact_reviews`            Review records associated with
                                      orders
  -----------------------------------------------------------------------

The order-item fact is at order-item grain, while the order fact is at
order grain. Measures from these tables should be aggregated carefully
to avoid double-counting when tables are joined.

## Key Analytics

The analytics layer includes views for:

-   Monthly business performance
-   Delivery performance
-   Seller performance
-   Customer performance
-   Review analysis
-   Seller delivery analysis
-   Data-quality reporting

### KPI definitions

  -----------------------------------------------------------------------
  KPI                                 Definition
  ----------------------------------- -----------------------------------
  Total Orders                        Distinct count of order IDs

  Delivered Orders                    Orders with delivered status

  Product Sales Value                 Sum of item `price`; excludes
                                      freight and is not profit

  Total Freight                       Sum of item freight values

  Average Order Value                 Product sales value divided by
                                      distinct orders, subject to the
                                      selected filter context

  On-Time Orders                      Delivered orders classified as on
                                      or before estimated delivery

  Delayed Orders                      Delivered orders classified as
                                      later than estimated delivery

  On-Time Delivery %                  On-time orders divided by on-time
                                      plus delayed orders

  Delay %                             Delayed orders divided by on-time
                                      plus delayed orders
  -----------------------------------------------------------------------

Undelivered, unknown, and invalid records should be shown separately or
excluded from eligible delivered-order rate denominators, with the rule
documented in the report.

## Power BI Dashboard

The Power BI report is organized around four analytical perspectives:

1.  **Executive Overview** --- order volume, product sales value,
    average order value, monthly trends, order status, and customer
    geography.
2.  **Supply Chain & Logistics** --- on-time and delayed orders,
    delivery percentages, delivery duration, and regional delay
    patterns.
3.  **Seller Performance** --- seller-level sales value, freight, order
    volume, and delivery performance.
4.  **Customer & Product Analytics** --- customer distribution, product
    categories, repeat-customer analysis, payment methods, and review
    scores.

Suggested report filters include year, month, customer state, seller
state, order status, delivery status, and product category.

## Excel Operations Report

The Excel workbook is designed as a shipment-level operational report.
Planned/implemented elements can include:

-   Exported shipment-level data from PostgreSQL
-   Delivery variance and delay-days calculations
-   SLA status and delivery-stage classifications
-   Delay categories (No Delay, Minor, Moderate, Severe, Pending)
-   PivotTables for delivery by state, delay category, delivery stage,
    and monthly performance
-   Charts, KPI summaries, and slicers

The delay categories are analytical groupings for this project, not
official Olist or contractual SLA classifications. Keep the original
timestamps unchanged and flag anomalous records rather than silently
correcting them.

## Project Structure

A suggested repository structure:

``` text
Business_Operations_and_Supply_Chain_Intelligence_Platform/
│
├── data/
│   └── raw/                         # Downloaded Olist CSV files (not committed)
│
├── sql/
│   ├── 01_create_schemas.sql
│   ├── 02_create_warehouse_tables.sql
│   ├── 03_load_dimensions.sql
│   ├── 04_load_facts.sql
│   ├── 05_data_quality_checks.sql
│   └── 06_create_analytics_views.sql
│
├── etl/
│   ├── __init__.py
│   └── main.py                      # Python ETL entry point, if used
│
├── reports/
│   ├── powerbi/                     # Power BI report file
│   └── excel/                       # Excel operations workbook
│
├── docs/
│   ├── architecture/
│   ├── data_dictionary.md
│   └── business_requirements.md
│
├── tests/
│   └──
│
├── .gitignore
├── requirements.txt
└── README.md
```

Adjust this structure to match the actual files in your repository. Do
not commit the raw dataset, database backups, credentials, or large
generated files unless you intentionally choose an appropriate Git LFS
or external storage strategy.

## Setup and Execution

### 1. Download the dataset

Download the Olist dataset from Kaggle and place the CSV files in
`data/raw/`. Confirm that all required source files are present.

### 2. Create the PostgreSQL database

Create a database, for example:

``` sql
CREATE DATABASE business_operations;
```

Connect to it in pgAdmin and create the schemas:

``` sql
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS analytics;
```

### 3. Load the staging tables

Create staging tables matching the CSV column names and data types, then
import each CSV into its corresponding table. Ensure the CSV import
option **Header** is enabled.

Expected staging table names:

``` text
staging.orders
staging.customers
staging.sellers
staging.products
staging.order_items
staging.payments
staging.reviews
staging.geolocation
staging.category_translation
```

### 4. Create and populate the warehouse

Run the SQL scripts in dependency order:

1.  Create dimension and fact tables.
2.  Load customer, seller, product, and date dimensions.
3.  Load order, order-item, payment, and review facts.
4.  Run data-quality checks.
5.  Create analytics views.

Populate `dim_date` before loading fact tables that reference date keys.
Review foreign-key failures and unmatched source identifiers rather than
dropping records without investigation.

### 5. Connect Power BI

In Power BI Desktop:

1.  Select **Get Data → PostgreSQL database**.
2.  Server: `localhost:5432`.
3.  Database: `business_operations`.
4.  Select Import mode (or DirectQuery if deliberately configured).
5.  Load the required warehouse tables or analytics views.
6.  Create and validate relationships before building measures and
    visuals.

### 6. Build the Excel report

Export the shipment-level query from PostgreSQL to CSV, open it in
Excel, convert the range to a Table, and build operational formulas,
PivotTables, charts, and slicers. Use the actual column names and
positions in the exported workbook when writing formulas.

## Data Quality and Assumptions

Data quality is part of the analysis, not just a preprocessing step.

Checks should include:

-   Duplicate or missing business keys
-   Missing delivery timestamps
-   Timestamp ordering (purchase, approval, carrier handover, customer
    delivery)
-   Missing dimension matches
-   Invalid or unexpected status values
-   Reconciliation of source row counts with warehouse row counts

Important interpretation rules:

-   Missing delivery timestamps do not automatically mean data errors;
    some orders may not have been delivered.
-   Preserve source timestamps and flag sequence anomalies for
    investigation.
-   A delivery is considered on time when the customer delivery
    timestamp is less than or equal to the estimated delivery timestamp.
-   Delay percentage uses only orders classified as either `On Time` or
    `Delayed`.
-   `price + freight_value` is item value plus freight, not profit.
-   `customer_unique_id` is more appropriate than order-specific
    `customer_id` for identifying repeat customers.
-   An order with items from multiple sellers may be represented under
    more than one seller in seller-level analysis.
-   Do not interpret correlation as proof of causation.

## Future Enhancements

-   Add dbt models, schema tests, and generated data documentation.
-   Orchestrate ingestion and transformation with Prefect.
-   Add automated reconciliation and data-quality test reports.
-   Create a documented business RCA with evidence-based
    recommendations.
-   Add GitHub Actions for SQL/Python checks.
-   Deploy PostgreSQL and reporting components to AWS where appropriate.
-   Add incremental loading and refresh monitoring.

## Author

**Piyush Singh**\
B.Tech, Computer Science and Engineering (AI & ML)\
VIT Bhopal University

-   GitHub: [PiyushVIT346](https://github.com/PiyushVIT346)
-   Portfolio: Add your portfolio URL here
-   LinkedIn: Add your LinkedIn URL here

## License and Dataset Attribution

This repository contains project code and documentation. The Olist
dataset is owned and distributed by its original publisher. Refer to the
[Kaggle dataset
page](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) for
dataset terms and attribution requirements. Do not redistribute the
dataset unless its terms permit it.
