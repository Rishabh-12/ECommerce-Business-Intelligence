# E-Commerce Business Intelligence & Decision Dashboard

## Project Overview

This project transforms raw e-commerce transactional data into a comprehensive **Business Intelligence Dashboard** that delivers actionable management insights. Built using Python and Streamlit, the dashboard goes beyond simple data visualization to provide a complete decision-support system following the Business Intelligence flow:

**RAW DATA → DATA CLEANING → EXPLORATORY DATA ANALYSIS → KPI IDENTIFICATION → TREND ANALYSIS → BUSINESS DRIVERS → RISKS → OPPORTUNITIES → RECOMMENDED ACTIONS**

The dashboard answers seven critical business questions:
1. What is happening?
2. Why is it happening?
3. What are the important trends?
4. What are the key business drivers?
5. What risks exist?
6. What opportunities exist?
7. What should management do?

## Problem Statement

E-commerce businesses generate vast amounts of transactional data daily, but raw data alone does not provide business value. Management teams need clear, data-driven insights to make informed strategic decisions. This project bridges the gap between raw transactional records and actionable business intelligence by automatically analyzing over 1 million transactions across 43 countries to identify trends, risks, opportunities, and recommended actions.

## Objective

- Convert raw e-commerce transaction data into meaningful business intelligence
- Identify key performance indicators (KPIs) and track their trends
- Analyze sales patterns, product performance, and customer behavior
- Detect business risks supported by quantitative evidence
- Identify growth opportunities with data-backed justification
- Generate actionable management recommendations using the Fact → Insight → Risk/Opportunity → Action methodology
- Present all findings through a professional, interactive Streamlit dashboard

## Business Intelligence Approach

The project follows a structured BI methodology:

```
FACT          → What the data actually shows (quantitative evidence)
INSIGHT       → What that fact means from a business perspective
RISK/OPP      → Whether it represents a threat or growth opportunity
ACTION        → What management should specifically do about it
```

Every numerical statement, percentage, trend, and finding in the dashboard is calculated directly from the dataset. No values are fabricated or assumed.

## Dataset

| Property | Details |
|----------|---------|
| **Dataset Name** | Online Retail II |
| **Source** | UCI Machine Learning Repository |
| **Dataset URL** | [https://archive.ics.uci.edu/dataset/502/online+retail+ii](https://archive.ics.uci.edu/dataset/502/online+retail+ii) |
| **Description** | All transactions occurring for a UK-based and registered, non-store online retail between 01/12/2009 and 09/12/2011. The company mainly sells unique all-occasion gift-ware. Many customers of the company are wholesalers. |
| **Total Rows** | 1,067,371 |
| **Total Columns** | 8 |
| **Date Range** | December 2009 – December 2011 |
| **Countries** | 43 |
| **Unique Customers** | 5,942 |
| **Unique Products** | 5,305 |

### Data Dictionary

| Column | Description | Data Type |
|--------|-------------|-----------|
| Invoice | Invoice number (6-digit, prefix 'C' = cancellation) | String |
| StockCode | Product/item code (5-digit) | String |
| Description | Product name | String |
| Quantity | Quantity per transaction | Integer |
| InvoiceDate | Date and time of transaction | DateTime |
| Price | Unit price in GBP (£) | Float |
| Customer ID | Unique customer identifier (5-digit) | Float |
| Country | Country of the customer | String |

## Data Cleaning

The following preprocessing steps are performed automatically:

1. **Duplicate Removal** — Removed 34,335 duplicate rows
2. **Cancelled Transaction Filtering** — Removed 19,494 cancelled transactions (invoices starting with 'C')
3. **Missing Description Handling** — Removed 4,382 rows with missing product descriptions
4. **Missing Customer ID** — Flagged 243,007 rows with missing customer IDs (retained for sales analysis)
5. **Date Validation** — Ensured all dates are valid datetime objects
6. **Non-positive Quantity Removal** — Removed rows with zero or negative quantities (returns/adjustments)
7. **Non-positive Price Removal** — Removed rows with zero or negative prices (6,207 rows)
8. **Extreme Outlier Removal** — Removed outlier transactions (Quantity or Price > 10,000)
9. **Derived Column Creation** — Created Revenue (Quantity × Price), Year, Month, YearMonth, DayOfWeek, Hour

## KPIs

The dashboard calculates and displays the following KPIs:

- **Total Revenue** — Sum of all transaction revenues
- **Total Orders** — Count of unique invoices
- **Total Customers** — Count of unique customer IDs
- **Average Order Value (AOV)** — Revenue divided by order count
- **Total Quantity Sold** — Sum of all quantities
- **Unique Products** — Count of distinct product descriptions
- **Countries Served** — Count of unique countries
- **Average Items per Order** — Quantity divided by order count
- **Repeat Purchase Rate** — Percentage of customers with multiple orders
- **Month-over-Month Revenue Growth** — Percentage change in monthly revenue

## Dashboard Pages

### Page 1: Executive Overview
- KPI summary cards with key business metrics
- Monthly revenue trend with interactive line chart
- Monthly orders and quantity bar charts
- Month-over-month revenue growth analysis
- 5 data-driven executive insights (Fact + Insight format)

### Page 2: Sales & Product Analysis
- Revenue by country (top 15 bar chart + pie distribution)
- Top 10 products by revenue and quantity
- Bottom 10 products by revenue (minimum 5 orders)
- Revenue by day of week and hour of day
- Data-driven sales insights

### Page 3: Customer & Risk Analysis
- Customer KPIs (total, average revenue, repeat rate, median revenue)
- Top 10 customers by revenue
- Customer revenue distribution histogram
- Customer concentration curve (Lorenz curve)
- Pareto analysis (top 20% customer contribution)
- Monthly active customers trend
- Quantified risk assessments with evidence and impact

### Page 4: Opportunities
- Data-backed business opportunities
- International market growth potential
- High-demand product analysis (bubble chart)
- Revenue trend with growth trajectory
- Each opportunity includes evidence and business justification

### Page 5: Recommended Actions
- Structured recommendations: Fact → Insight → Risk/Opportunity → Action
- Action priority matrix (Impact vs Urgency)
- Action summary table with priority levels
- Specific, actionable management recommendations

### Page 6: Data Quality
- Complete dataset information and metadata
- Missing values analysis with visualization
- Data types documentation
- Step-by-step cleaning log
- Cleaned data summary statistics

## Business Insights

Insights are generated algorithmically from actual data calculations. Each insight follows a structured format:

- **FACT**: A specific, quantified finding from the data
- **INSIGHT**: The business interpretation of that fact

No generic or fabricated statements are used. Every percentage, currency value, and trend referenced is computed from the dataset.

## Risks and Opportunities

### Risk Identification Methodology
Risks are identified by scanning for:
- Geographic revenue concentration (>70% in one market)
- Declining revenue trends in recent months
- Customer concentration (top 10 customer dependency)
- Incomplete customer data (missing IDs)
- High volume of low-value transactions

### Opportunity Identification Methodology
Opportunities are identified by analyzing:
- International market expansion potential
- High-performing product growth potential
- Day-of-week/time optimization
- Customer retention improvement potential
- Seasonal demand optimization

Each risk and opportunity includes quantitative evidence and potential business impact.

## Recommended Actions

The Fact → Insight → Risk/Opportunity → Action methodology ensures recommendations are:

1. **Evidence-based** — Grounded in actual data findings
2. **Contextualized** — Explained in business terms
3. **Categorized** — Classified as risk mitigation or opportunity capitalization
4. **Actionable** — Specific enough for management to implement
5. **Prioritized** — Ranked by impact and urgency

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.x | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computations |
| Streamlit | Interactive web dashboard framework |
| Plotly | Interactive data visualizations |
| OpenPyXL | Excel file reading |

## Project Structure

```
ECommerce-Business-Intelligence/
│
├── RishabhSingh_ECommerceBusinessIntelligence.py   # Main application (Streamlit dashboard)
├── requirements.txt                                  # Python dependencies
├── RishabhSingh_ProjectReport.docx                  # Project report document
├── README.md                                         # Project documentation
│
└── data/
    └── online_retail_II.xlsx                         # Dataset file
```

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/ECommerce-Business-Intelligence.git
cd ECommerce-Business-Intelligence
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Dataset (Auto-Download):**
The application automatically downloads the dataset from the UCI Machine Learning Repository on first run. No manual download is required. If you prefer to download manually, place `online_retail_II.xlsx` in a `data/` directory:
[https://archive.ics.uci.edu/dataset/502/online+retail+ii](https://archive.ics.uci.edu/dataset/502/online+retail+ii)

## Running the Application

```bash
streamlit run RishabhSingh_ECommerceBusinessIntelligence.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

### Interactive Features
- **Sidebar Navigation** — Switch between dashboard pages
- **Date Range Filter** — Filter data by date range
- **Country Filter** — Filter by specific countries
- **Interactive Charts** — Hover, zoom, and pan on all Plotly visualizations

## Future Scope

1. **Customer Segmentation** — Implement RFM (Recency, Frequency, Monetary) analysis for targeted marketing
2. **Demand Forecasting** — Add time-series forecasting models to predict future revenue
3. **Real-time Data Integration** — Connect to live e-commerce databases for real-time monitoring
4. **Automated Alerting** — Set up threshold-based alerts for KPI anomalies
5. **A/B Testing Framework** — Integrate experiment tracking for marketing campaign evaluation
6. **Product Recommendation Engine** — Build collaborative filtering for cross-selling suggestions
7. **Profitability Analysis** — Incorporate cost data for true profit margin calculation
8. **Export Functionality** — Add PDF/Excel report generation from the dashboard

## Conclusion

This E-Commerce Business Intelligence & Decision Dashboard demonstrates the complete journey from raw transactional data to strategic business recommendations. By applying structured analytical methodology — cleaning, exploring, quantifying, contextualizing, and recommending — the project transforms over 1 million transaction records into a decision-support tool that empowers management with evidence-based insights.

The dashboard is designed for business users who need answers, not just charts. Every finding is supported by data, every risk is backed by evidence, and every recommendation follows a clear logical path from fact to action.

---

**Author:** Rishabh Singh  
**Dataset Source:** [UCI Machine Learning Repository - Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)  
**Technology:** Python | Streamlit | Pandas | Plotly
