# E-Commerce Business Intelligence & Decision Dashboard

## Project Overview

This project transforms real e-commerce transaction data into a decision-oriented Business Intelligence dashboard.

**RAW DATA → DATA CLEANING → KPI ANALYSIS → TREND ANALYSIS → BUSINESS DRIVERS → RISKS → OPPORTUNITIES → RECOMMENDED ACTIONS**

The dashboard is designed to answer:
1. What is happening?
2. Why is it happening?
3. What trends and drivers matter?
4. What risks are visible in the data?
5. What opportunities are visible?
6. What action could management consider?

## Problem Statement

Raw e-commerce transactions contain valuable information about orders, products, customers, time and geography, but the records are difficult to use directly for management decisions. This project converts the transaction data into KPIs, interactive visualizations and evidence-based decision support.

## Objectives

- Clean and validate transaction data.
- Calculate business KPIs from available fields.
- Analyze revenue, orders, products, customers, geography and time.
- Identify measurable risks and opportunities.
- Convert findings into Fact → Insight → Risk/Opportunity → Action recommendations.
- Provide an interactive Streamlit dashboard.

## Dataset

**Dataset:** Online Retail II  
**Source:** UCI Machine Learning Repository  
**Dataset URL:** https://archive.ics.uci.edu/dataset/502/online+retail+ii

The UCI dataset contains 1,067,371 transaction instances from a UK-based non-store online retailer covering 01/12/2009 through 09/12/2011. It contains eight variables: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID and Country.

### Dataset use

The project does **not** use a dataset from the internship masterclasses. Online Retail II is a separately sourced public dataset from the UCI Machine Learning Repository.

## Data Cleaning

The application performs the following steps at runtime:

1. Remove duplicate rows.
2. Exclude cancelled invoices.
3. Flag missing Customer IDs while retaining those rows for sales analysis.
4. Remove rows with missing product descriptions.
5. Convert InvoiceDate to datetime and remove invalid dates.
6. Remove non-positive quantities.
7. Remove non-positive prices.
8. Remove extreme transaction values above the implemented threshold.
9. Create Revenue = Quantity × Price.
10. Create Year, Month, YearMonth, DayOfWeek, Hour and Date fields.
11. Normalize product descriptions and country values.

The **Data Quality** page displays the actual row counts, missing values, data types and cleaning log generated from the dataset at runtime. Cleaning counts are intentionally not hard-coded in this README.

## KPIs

The dashboard calculates:

- Total Revenue
- Total Orders
- Total Customers
- Average Order Value
- Total Quantity Sold
- Unique Products
- Countries Served
- Average Items per Order
- Repeat Purchase Rate
- Month-over-Month Revenue Growth

Profit and profit margin are **not** claimed because the source dataset does not contain cost/profit fields.

## Dashboard Pages

### 1. Executive Overview
- KPI cards
- Monthly revenue trend
- Orders and quantity trends
- Month-over-month growth
- Data-driven executive insights

### 2. Sales & Product Analysis
- Revenue by country
- Top products
- Bottom-performing products
- Day-of-week revenue
- Hour-of-day revenue
- Sales insights

### 3. Customer & Risk Analysis
- Customer KPIs
- Top customers
- Customer revenue distribution
- Customer concentration / Pareto analysis
- Active customer trend
- Quantified risk indicators

### 4. Opportunities
- International market opportunities
- High-demand product analysis
- Revenue growth patterns
- Customer retention opportunities
- Seasonal opportunities

### 5. Recommended Actions
Each recommendation follows:

**FACT → INSIGHT → RISK / OPPORTUNITY → RECOMMENDED ACTION**

The page also includes an Impact vs Urgency matrix and action summary.

### 6. Data Quality
- Dataset metadata
- Missing-value analysis
- Data types
- Cleaning log
- Cleaned-data summary

## Business Intelligence Methodology

**FACT** — What the data quantitatively shows.

**INSIGHT** — What that fact means from a business perspective.

**RISK / OPPORTUNITY** — Why the finding may matter to the business.

**ACTION** — A specific management response derived from the finding.

All numerical findings displayed by the application are calculated from the loaded dataset.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application and analytical logic |
| Pandas | Data cleaning and analysis |
| NumPy | Numerical calculations |
| Streamlit | Interactive dashboard |
| Plotly | Interactive visualizations |
| OpenPyXL | Excel dataset loading |

## Project Structure

```
ECommerce-Business-Intelligence/
├── RishabhSingh_ECommerceBusinessIntelligence.py
├── requirements.txt
├── RishabhSingh_ProjectReport.docx
└── README.md
```

The dataset is intentionally not committed to Git because of its size. The application downloads it from the documented UCI source when it is not available locally.

## Installation

Clone the repository:

```bash
git clone https://github.com/Rishabh-12/ECommerce-Business-Intelligence.git
cd ECommerce-Business-Intelligence
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Dashboard

```bash
streamlit run RishabhSingh_ECommerceBusinessIntelligence.py
```

On first run, if `data/online_retail_II.xlsx` is missing, the application downloads the public dataset from UCI and stores it locally.

## Validation

The repository was reviewed against the internship submission requirements:

- Main Python code file present.
- requirements.txt present.
- Project report DOCX present.
- README.md present.
- Public dataset source documented.
- Main dashboard contained in one Python file.
- No ZIP submission file is required.

The application is designed to calculate cleaning counts and business findings at runtime rather than presenting fabricated fixed values.

The submitted project report includes screenshots of the locally running dashboard UI.

## Limitations

- The dataset is historical rather than current market data.
- Profitability cannot be measured without cost data.
- Missing customer IDs limit customer-level analysis for unidentified transactions.
- The dashboard provides descriptive/diagnostic BI rather than causal inference.
- Recommendations are decision support and should be checked against operational constraints.

## Future Scope

- RFM customer segmentation
- Demand and revenue forecasting
- Real-time database integration
- Automated KPI anomaly alerts
- A/B testing analysis
- Product recommendation systems
- Profitability analysis after adding cost data
- PDF/Excel dashboard exports

## Conclusion

This project demonstrates the complete journey from raw e-commerce transactions to management-oriented business intelligence. It combines data preparation, KPI analysis, trend analysis, customer and geographic analysis, risk identification, opportunity identification and actionable recommendations in one interactive dashboard.

**Author:** Rishabh Singh  
**Dataset:** Online Retail II — UCI Machine Learning Repository
