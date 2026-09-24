"""
E-Commerce Business Intelligence & Decision Dashboard
Author: Rishabh Singh
Dataset: Online Retail II (UCI Machine Learning Repository)
Description: A comprehensive business intelligence dashboard that transforms
             raw e-commerce transactional data into actionable business insights,
             risk assessments, opportunity identification, and management recommendations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
import warnings

warnings.filterwarnings("ignore")

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="E-Commerce Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    body {
        background-color: #ffffff;
        color: #1f2937;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #111827;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #e94560;
        margin-bottom: 1.5rem;
    }
    .sub-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1f2937;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    .kpi-card-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    .kpi-card-orange {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    .kpi-card-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.3rem 0;
    }
    .kpi-label {
        font-size: 0.85rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .insight-box {
        background: #f8f9fa;
        border-left: 4px solid #4361ee;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        border-radius: 0 8px 8px 0;
    }
    .risk-box {
        background: #fff5f5;
        border-left: 4px solid #e63946;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        border-radius: 0 8px 8px 0;
    }
    .opportunity-box {
        background: #f0fff4;
        border-left: 4px solid #2d6a4f;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        border-radius: 0 8px 8px 0;
    }
    .action-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        border-radius: 0 8px 8px 0;
    }
    .stMetric {
        background-color: #f8fafc;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
    }
    div[data-testid="stSidebar"] {
        background: #f8fafc;
        border-right: 1px solid #e5e7eb;
    }
    div[data-testid="stSidebar"] .stMarkdown,
    div[data-testid="stSidebar"] .stMarkdown p,
    div[data-testid="stSidebar"] label {
        color: #111827 !important;
    }
    div[data-testid="stSidebar"] [data-baseweb="select"] > div,
    div[data-testid="stSidebar"] [data-baseweb="input"] > div {
        background-color: #ffffff;
    }
    div[data-testid="stSidebar"] .stRadio label {
        color: #111827 !important;
    }
    .stApp {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA LOADING AND CLEANING
# ============================================================
@st.cache_data(show_spinner="Loading and cleaning data...")
def load_and_clean_data():
    """Load the Online Retail II dataset and perform comprehensive cleaning."""
    
    # Determine file path
    possible_paths = [
        "data/online_retail_II.xlsx",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "online_retail_II.xlsx"),
    ]
    
    file_path = None
    for p in possible_paths:
        if os.path.exists(p):
            file_path = p
            break
    
    if file_path is None:
        # Auto-download dataset from UCI ML Repository
        st.info("📥 Dataset not found locally. Downloading from UCI Machine Learning Repository...")
        import urllib.request
        import zipfile
        
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        zip_path = os.path.join(data_dir, "online_retail_ii.zip")
        xlsx_path = os.path.join(data_dir, "online_retail_II.xlsx")
        
        try:
            urllib.request.urlretrieve(
                "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip",
                zip_path
            )
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(data_dir)
            if os.path.exists(zip_path):
                os.remove(zip_path)
            file_path = xlsx_path
            st.success("✅ Dataset downloaded successfully!")
        except Exception as e:
            st.error(f"Failed to download dataset: {e}")
            st.info("Please manually download from: https://archive.ics.uci.edu/dataset/502/online+retail+ii")
            st.info("Place 'online_retail_II.xlsx' in the data/ directory.")
            st.stop()
    
    # Load both sheets
    df1 = pd.read_excel(file_path, sheet_name="Year 2009-2010")
    df2 = pd.read_excel(file_path, sheet_name="Year 2010-2011")
    raw_df = pd.concat([df1, df2], ignore_index=True)
    
    # Record raw stats for data quality reporting
    raw_stats = {
        "total_rows": len(raw_df),        "total_columns": len(raw_df.columns),
        "columns": list(raw_df.columns),
        "missing_values": raw_df.isnull().sum().to_dict(),
        "duplicate_rows": int(raw_df.duplicated().sum()),
        "dtypes": raw_df.dtypes.astype(str).to_dict(),
    }
    
    # ---- CLEANING ----
    df = raw_df.copy()
    
    cleaning_log = []
    
    # 1. Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    cleaning_log.append(f"Removed {before - after:,} duplicate rows")
    
    # 2. Convert Invoice to string
    df["Invoice"] = df["Invoice"].astype(str).str.strip()
    
    # 3. Remove cancelled transactions (invoices starting with 'C')
    before = len(df)
    df = df[~df["Invoice"].str.startswith("C")]
    after = len(df)
    cleaning_log.append(f"Removed {before - after:,} cancelled transactions (Invoice starting with 'C')")
    
    # 4. Handle missing Customer ID
    before = len(df)
    missing_cust = df["Customer ID"].isnull().sum()
    cleaning_log.append(f"Found {missing_cust:,} rows with missing Customer ID")
    # Keep rows with missing customer ID for sales analysis but mark them
    df["HasCustomerID"] = df["Customer ID"].notna()
    
    # 5. Remove rows with missing Description
    before = len(df)
    df = df.dropna(subset=["Description"])
    after = len(df)
    cleaning_log.append(f"Removed {before - after:,} rows with missing Description")
    
    # 6. Ensure InvoiceDate is datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    before = len(df)
    df = df.dropna(subset=["InvoiceDate"])
    after = len(df)
    if before - after > 0:
        cleaning_log.append(f"Removed {before - after:,} rows with invalid dates")
    
    # 7. Remove non-positive quantities
    before = len(df)
    df = df[df["Quantity"] > 0]
    after = len(df)
    cleaning_log.append(f"Removed {before - after:,} rows with non-positive Quantity")
    
    # 8. Remove non-positive prices
    before = len(df)
    df = df[df["Price"] > 0]
    after = len(df)
    cleaning_log.append(f"Removed {before - after:,} rows with non-positive Price")
    
    # 9. Remove extreme outliers (Quantity > 10000 or Price > 10000)
    before = len(df)
    df = df[(df["Quantity"] <= 10000) & (df["Price"] <= 10000)]
    after = len(df)
    if before - after > 0:
        cleaning_log.append(f"Removed {before - after:,} extreme outlier rows (Quantity or Price > 10,000)")
    
    # 10. Create derived columns
    df["Revenue"] = df["Quantity"] * df["Price"]
    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.month
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
    df["Hour"] = df["InvoiceDate"].dt.hour
    df["Date"] = df["InvoiceDate"].dt.date
    
    cleaning_log.append("Created derived columns: Revenue, Year, Month, YearMonth, DayOfWeek, Hour, Date")
    
    # Clean up Description
    df["Description"] = df["Description"].str.strip().str.upper()
    
    # Clean up Country
    df["Country"] = df["Country"].str.strip()
    
    # Convert Customer ID to string where available
    df["Customer ID"] = df["Customer ID"].apply(lambda x: str(int(x)) if pd.notna(x) else None)
    
    # Record cleaned stats
    raw_stats["date_min"] = str(df["InvoiceDate"].min())
    raw_stats["date_max"] = str(df["InvoiceDate"].max())
    raw_stats["cleaned_rows"] = len(df)
    raw_stats["cleaning_log"] = cleaning_log
    
    return df, raw_stats


# ============================================================
# COLUMN DETECTION HELPER
# ============================================================
def detect_columns(df):
    """Intelligently detect column roles from the dataframe."""
    cols = {}
    col_lower = {c: c.lower().replace("_", " ").replace("-", " ") for c in df.columns}
    
    # Date column
    for c, cl in col_lower.items():
        if any(kw in cl for kw in ["invoicedate", "invoice date", "date", "order date", "orderdate"]):
            if pd.api.types.is_datetime64_any_dtype(df[c]):
                cols["date"] = c
                break
    
    # Revenue/Sales
    for c, cl in col_lower.items():
        if any(kw in cl for kw in ["revenue", "sales", "total", "amount"]):
            if pd.api.types.is_numeric_dtype(df[c]):
                cols["revenue"] = c
                break
    
    # Quantity
    for c, cl in col_lower.items():
        if any(kw in cl for kw in ["quantity", "qty"]):
            if pd.api.types.is_numeric_dtype(df[c]):
                cols["quantity"] = c
                break
    
    # Price
    for c, cl in col_lower.items():
        if any(kw in cl for kw in ["price", "unit price", "unitprice"]):
            if pd.api.types.is_numeric_dtype(df[c]):
                cols["price"] = c
                break
    
    # Product/Description
    for c, cl in col_lower.items():
        if any(kw in cl for kw in ["description", "product", "item", "stockcode"]):
            cols["product"] = c
            break
    
    # Customer
    for c, cl in col_lower.items():
        if any(kw in cl for kw in ["customer", "cust"]):
            cols["customer"] = c
            break
    
    # Country/Region
    for c, cl in col_lower.items():
        if any(kw in cl for kw in ["country", "region", "state", "city"]):
            cols["country"] = c
            break
    
    # Invoice
    for c, cl in col_lower.items():
        if any(kw in cl for kw in ["invoice", "order", "transaction"]):
            if c != cols.get("date"):
                cols["invoice"] = c
                break
    
    # StockCode
    for c, cl in col_lower.items():
        if any(kw in cl for kw in ["stockcode", "stock code", "sku", "product id", "productid"]):
            cols["stockcode"] = c
            break
    
    return cols


# ============================================================
# HELPER: FORMAT CURRENCY
# ============================================================
def fmt_currency(value):
    """Format a number as currency (GBP for this dataset)."""
    if abs(value) >= 1_000_000:
        return f"£{value/1_000_000:,.2f}M"
    elif abs(value) >= 1_000:
        return f"£{value/1_000:,.1f}K"
    else:
        return f"£{value:,.2f}"


def fmt_number(value):
    """Format a number with commas."""
    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:,.2f}M"
    elif abs(value) >= 1_000:
        return f"{value/1_000:,.1f}K"
    else:
        return f"{value:,.0f}"


# ============================================================
# KPI CARD RENDERER
# ============================================================
def render_kpi_card(label, value, card_class="kpi-card"):
    """Render a styled KPI card."""
    return f"""
    <div class="{card_class}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """

# ============================================================
# MAIN APPLICATION
# ============================================================
def main():
    # Load data
    df, raw_stats = load_and_clean_data()
    cols = detect_columns(df)
    
    # ---- SIDEBAR ----
    st.sidebar.markdown("## 📊 Navigation")
    page = st.sidebar.radio(
        "Select Page",
        [
            "🏠 Executive Overview",
            "📈 Sales & Product Analysis",
            "👥 Customer & Risk Analysis",
            "🌟 Opportunities",
            "🎯 Recommended Actions",
            "🔍 Data Quality"
        ],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🔧 Filters")
    
    # Date range filter
    min_date = df["InvoiceDate"].min().date()
    max_date = df["InvoiceDate"].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Country filter
    countries = sorted(df["Country"].unique())
    selected_countries = st.sidebar.multiselect(
        "Country",
        options=countries,
        default=[]
    )
    
    # Apply filters
    filtered_df = df.copy()
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["InvoiceDate"].dt.date >= start_date) &
            (filtered_df["InvoiceDate"].dt.date <= end_date)
        ]
    
    if selected_countries:
        filtered_df = filtered_df[filtered_df["Country"].isin(selected_countries)]
    
    # Show filter status
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Filtered Records:** {len(filtered_df):,}")
    st.sidebar.markdown(f"**Date Range:** {min_date} to {max_date}")
    st.sidebar.markdown(f"**Countries Selected:** {'All' if not selected_countries else len(selected_countries)}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='text-align: center; color: #aaa; font-size: 0.75rem; padding: 0.5rem;'>
            E-Commerce Business Intelligence<br>
            Rishabh Singh | 2026
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # ---- PAGE ROUTING ----
    if "Executive" in page:
        page_executive_overview(filtered_df, df, cols)
    elif "Sales" in page:
        page_sales_product(filtered_df, cols)
    elif "Customer" in page:
        page_customer_risk(filtered_df, df, cols)
    elif "Opportunities" in page:
        page_opportunities(filtered_df, cols)
    elif "Recommended" in page:
        page_recommended_actions(filtered_df, df, cols)
    elif "Data Quality" in page:
        page_data_quality(df, raw_stats, cols)


# ============================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ============================================================
def page_executive_overview(df, full_df, cols):
    st.markdown('<div class="main-header">📊 Executive Overview</div>', unsafe_allow_html=True)
    
    if len(df) == 0:
        st.warning("No data available for the selected filters.")
        return
    
    # Calculate KPIs
    total_revenue = df["Revenue"].sum()
    total_orders = df["Invoice"].nunique()
    total_quantity = df["Quantity"].sum()
    total_customers = df.loc[df["HasCustomerID"], "Customer ID"].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    total_products = df["Description"].nunique()
    total_countries = df["Country"].nunique()
    avg_items_per_order = total_quantity / total_orders if total_orders > 0 else 0
    
    # KPI Cards - Row 1
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(render_kpi_card("Total Revenue", fmt_currency(total_revenue), "kpi-card"), unsafe_allow_html=True)
    with k2:
        st.markdown(render_kpi_card("Total Orders", fmt_number(total_orders), "kpi-card-green"), unsafe_allow_html=True)
    with k3:
        st.markdown(render_kpi_card("Total Customers", fmt_number(total_customers), "kpi-card-orange"), unsafe_allow_html=True)
    with k4:
        st.markdown(render_kpi_card("Avg Order Value", fmt_currency(avg_order_value), "kpi-card-blue"), unsafe_allow_html=True)
    
    # KPI Cards - Row 2
    k5, k6, k7, k8 = st.columns(4)
    with k5:
        st.markdown(render_kpi_card("Total Quantity Sold", fmt_number(total_quantity), "kpi-card-blue"), unsafe_allow_html=True)
    with k6:
        st.markdown(render_kpi_card("Unique Products", fmt_number(total_products), "kpi-card"), unsafe_allow_html=True)
    with k7:
        st.markdown(render_kpi_card("Countries Served", fmt_number(total_countries), "kpi-card-green"), unsafe_allow_html=True)
    with k8:
        st.markdown(render_kpi_card("Avg Items/Order", f"{avg_items_per_order:.1f}", "kpi-card-orange"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Revenue Over Time
    st.markdown('<div class="sub-header">📈 Revenue Trend</div>', unsafe_allow_html=True)
    
    monthly_revenue = df.groupby("YearMonth").agg(
        Revenue=("Revenue", "sum"),
        Orders=("Invoice", "nunique"),
        Quantity=("Quantity", "sum")
    ).reset_index()
    monthly_revenue = monthly_revenue.sort_values("YearMonth")
    
    fig_rev = go.Figure()
    fig_rev.add_trace(go.Scatter(
        x=monthly_revenue["YearMonth"],
        y=monthly_revenue["Revenue"],
        mode="lines+markers",
        name="Revenue",
        line=dict(color="#4361ee", width=3),
        marker=dict(size=8),
        fill="tozeroy",
        fillcolor="rgba(67, 97, 238, 0.1)"
    ))
    fig_rev.update_layout(
        title="Monthly Revenue Trend",
        xaxis_title="Month",
        yaxis_title="Revenue (£)",
        template="plotly_white",
        height=400,
        hovermode="x unified"
    )
    st.plotly_chart(fig_rev, use_container_width=True)
    
    # Orders and Quantity Trends
    col1, col2 = st.columns(2)
    
    with col1:
        fig_orders = px.bar(
            monthly_revenue,
            x="YearMonth",
            y="Orders",
            title="Monthly Orders",
            color_discrete_sequence=["#2d6a4f"],
            template="plotly_white"
        )
        fig_orders.update_layout(
            xaxis_title="Month",
            yaxis_title="Number of Orders",
            height=350
        )
        st.plotly_chart(fig_orders, use_container_width=True)
    
    with col2:
        fig_qty = px.bar(
            monthly_revenue,
            x="YearMonth",
            y="Quantity",
            title="Monthly Quantity Sold",
            color_discrete_sequence=["#e63946"],
            template="plotly_white"
        )
        fig_qty.update_layout(
            xaxis_title="Month",
            yaxis_title="Quantity",
            height=350
        )
        st.plotly_chart(fig_qty, use_container_width=True)
    
    # Revenue Growth
    st.markdown('<div class="sub-header">📊 Month-over-Month Revenue Growth</div>', unsafe_allow_html=True)
    monthly_revenue["Growth_%"] = monthly_revenue["Revenue"].pct_change() * 100
    
    fig_growth = go.Figure()
    colors = ["#2d6a4f" if g >= 0 else "#e63946" for g in monthly_revenue["Growth_%"].fillna(0)]
    fig_growth.add_trace(go.Bar(
        x=monthly_revenue["YearMonth"],
        y=monthly_revenue["Growth_%"],
        marker_color=colors,
        name="Growth %"
    ))
    fig_growth.update_layout(
        title="Month-over-Month Revenue Growth (%)",
        xaxis_title="Month",
        yaxis_title="Growth (%)",
        template="plotly_white",
        height=350
    )
    st.plotly_chart(fig_growth, use_container_width=True)
    
    # Executive Insights
    st.markdown("---")
    st.markdown('<div class="sub-header">💡 Executive Insights</div>', unsafe_allow_html=True)
    
    # Generate data-driven insights
    insights = generate_executive_insights(df, monthly_revenue, total_revenue, total_orders, total_customers, avg_order_value)
    
    for insight in insights:
        st.markdown(
            f"""<div class="insight-box">
                <strong>📌 FACT:</strong> {insight['fact']}<br><br>
                <strong>💡 INSIGHT:</strong> {insight['insight']}
            </div>""",
            unsafe_allow_html=True
        )


def generate_executive_insights(df, monthly_revenue, total_revenue, total_orders, total_customers, avg_order_value):
    """Generate data-driven executive insights from actual data."""
    insights = []
    
    # 1. Top country contribution
    country_rev = df.groupby("Country")["Revenue"].sum().sort_values(ascending=False)
    top_country = country_rev.index[0]
    top_country_pct = (country_rev.iloc[0] / total_revenue * 100)
    insights.append({
        "fact": f"The United Kingdom accounts for {fmt_currency(country_rev.iloc[0])} ({top_country_pct:.1f}%) of total revenue, making it the dominant market.",
        "insight": f"The business is heavily concentrated in {top_country}. While this indicates a strong domestic market, it also represents a concentration risk. International markets represent only {100-top_country_pct:.1f}% of revenue."
    })
    
    # 2. Revenue trend
    if len(monthly_revenue) >= 3:
        recent_months = monthly_revenue.tail(3)
        first_rev = recent_months["Revenue"].iloc[0]
        last_rev = recent_months["Revenue"].iloc[-1]
        trend_pct = ((last_rev - first_rev) / first_rev * 100) if first_rev > 0 else 0
        trend_word = "increased" if trend_pct > 0 else "decreased"
        insights.append({
            "fact": f"Revenue in the last 3 months of the dataset has {trend_word} by {abs(trend_pct):.1f}%, from {fmt_currency(first_rev)} to {fmt_currency(last_rev)}.",
            "insight": f"The {'upward' if trend_pct > 0 else 'downward'} revenue trend in recent months {'suggests growing demand and effective sales strategies' if trend_pct > 0 else 'signals a potential slowdown that requires management attention to reverse'}."
        })
    
    # 3. Customer value
    if total_customers > 0:
        rev_per_customer = total_revenue / total_customers
        insights.append({
            "fact": f"Average revenue per customer is {fmt_currency(rev_per_customer)}, with {total_customers:,} unique customers placing {total_orders:,} orders.",
            "insight": f"The average order value of {fmt_currency(avg_order_value)} combined with the customer base size suggests a retail model with frequent, moderate-sized transactions. Increasing repeat purchase frequency could significantly boost revenue."
        })
    
    # 4. Peak trading day
    day_revenue = df.groupby("DayOfWeek")["Revenue"].sum()
    peak_day = day_revenue.idxmax()
    peak_day_rev = day_revenue.max()
    peak_day_pct = (peak_day_rev / total_revenue * 100)
    insights.append({
        "fact": f"{peak_day} is the highest-revenue day of the week, generating {fmt_currency(peak_day_rev)} ({peak_day_pct:.1f}% of total revenue).",
        "insight": f"Knowing that {peak_day} drives the most revenue can help optimize staffing, marketing campaigns, and promotional activities to capitalize on peak demand."
    })
    
    # 5. Peak month
    best_month = monthly_revenue.loc[monthly_revenue["Revenue"].idxmax()]
    insights.append({
        "fact": f"The highest revenue month was {best_month['YearMonth']}, generating {fmt_currency(best_month['Revenue'])} with {int(best_month['Orders']):,} orders.",
        "insight": "This peak indicates strong seasonal demand patterns. Management should plan inventory, staffing, and marketing budgets to align with these seasonal peaks to maximize sales potential."
    })
    
    return insights


# ============================================================
# PAGE 2: SALES & PRODUCT ANALYSIS
# ============================================================
def page_sales_product(df, cols):
    st.markdown('<div class="main-header">📈 Sales & Product Analysis</div>', unsafe_allow_html=True)
    
    if len(df) == 0:
        st.warning("No data available for the selected filters.")
        return
    
    # Revenue by Country
    st.markdown('<div class="sub-header">🌍 Revenue by Country</div>', unsafe_allow_html=True)
    
    country_revenue = df.groupby("Country").agg(
        Revenue=("Revenue", "sum"),
        Orders=("Invoice", "nunique"),
        Quantity=("Quantity", "sum")
    ).sort_values("Revenue", ascending=False).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 15 countries by revenue
        top_countries = country_revenue.head(15)
        fig_country = px.bar(
            top_countries,
            x="Revenue",
            y="Country",
            orientation="h",
            title="Top 15 Countries by Revenue",
            color="Revenue",
            color_continuous_scale="Viridis",
            template="plotly_white"
        )
        fig_country.update_layout(
            height=500,
            yaxis=dict(autorange="reversed"),
            showlegend=False
        )
        st.plotly_chart(fig_country, use_container_width=True)
    
    with col2:
        # Country distribution pie (top 10 + Others)
        top10 = country_revenue.head(10).copy()
        others_rev = country_revenue.iloc[10:]["Revenue"].sum()
        if others_rev > 0:
            others_row = pd.DataFrame({"Country": ["Others"], "Revenue": [others_rev]})
            pie_data = pd.concat([top10[["Country", "Revenue"]], others_row], ignore_index=True)
        else:
            pie_data = top10[["Country", "Revenue"]]
        
        fig_pie = px.pie(
            pie_data,
            values="Revenue",
            names="Country",
            title="Revenue Distribution by Country",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(height=500)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    # Top and Bottom Products
    st.markdown('<div class="sub-header">🏆 Product Performance</div>', unsafe_allow_html=True)
    
    product_revenue = df.groupby("Description").agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Invoice", "nunique")
    ).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 products by revenue
        top10_products = product_revenue.nlargest(10, "Revenue")
        fig_top = px.bar(
            top10_products,
            x="Revenue",
            y="Description",
            orientation="h",
            title="Top 10 Products by Revenue",
            color_discrete_sequence=["#2d6a4f"],
            template="plotly_white"
        )
        fig_top.update_layout(
            height=450,
            yaxis=dict(autorange="reversed"),
            yaxis_title=""
        )
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        # Top 10 products by quantity
        top10_qty = product_revenue.nlargest(10, "Quantity")
        fig_topq = px.bar(
            top10_qty,
            x="Quantity",
            y="Description",
            orientation="h",
            title="Top 10 Products by Quantity Sold",
            color_discrete_sequence=["#4361ee"],
            template="plotly_white"
        )
        fig_topq.update_layout(            height=450,
            yaxis=dict(autorange="reversed"),
            yaxis_title=""
        )
        st.plotly_chart(fig_topq, use_container_width=True)
    
    # Bottom performers
    st.markdown('<div class="sub-header">📉 Low-Performing Products</div>', unsafe_allow_html=True)
    
    # Products with meaningful order count but low revenue
    products_min_orders = product_revenue[product_revenue["Orders"] >= 5]
    if len(products_min_orders) > 0:
        bottom10 = products_min_orders.nsmallest(10, "Revenue")
        fig_bottom = px.bar(
            bottom10,
            x="Revenue",
            y="Description",
            orientation="h",
            title="Bottom 10 Products by Revenue (minimum 5 orders)",
            color_discrete_sequence=["#e63946"],
            template="plotly_white"
        )
        fig_bottom.update_layout(
            height=400,
            yaxis=dict(autorange="reversed"),
            yaxis_title=""
        )
        st.plotly_chart(fig_bottom, use_container_width=True)
    
    st.markdown("---")
    
    # Revenue by Day of Week
    st.markdown('<div class="sub-header">📅 Sales Patterns</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_rev = df.groupby("DayOfWeek")["Revenue"].sum().reindex(dow_order).fillna(0).reset_index()
        fig_dow = px.bar(
            dow_rev,
            x="DayOfWeek",
            y="Revenue",
            title="Revenue by Day of Week",
            color_discrete_sequence=["#764ba2"],
            template="plotly_white"
        )
        fig_dow.update_layout(height=350, xaxis_title="", yaxis_title="Revenue (£)")
        st.plotly_chart(fig_dow, use_container_width=True)
    
    with col2:
        hour_rev = df.groupby("Hour")["Revenue"].sum().reset_index()
        fig_hour = px.bar(
            hour_rev,
            x="Hour",
            y="Revenue",
            title="Revenue by Hour of Day",
            color_discrete_sequence=["#f093fb"],
            template="plotly_white"
        )
        fig_hour.update_layout(height=350, xaxis_title="Hour", yaxis_title="Revenue (£)")
        st.plotly_chart(fig_hour, use_container_width=True)
    
    # Sales Insights
    st.markdown("---")
    st.markdown('<div class="sub-header">💡 Sales & Product Insights</div>', unsafe_allow_html=True)
    
    total_rev = df["Revenue"].sum()
    
    # Top performer insight
    top_product = product_revenue.nlargest(1, "Revenue").iloc[0]
    top_prod_pct = top_product["Revenue"] / total_rev * 100
    st.markdown(
        f"""<div class="insight-box">
            <strong>🏆 TOP PERFORMER:</strong> "{top_product['Description']}" is the highest revenue product, 
            generating {fmt_currency(top_product['Revenue'])} ({top_prod_pct:.1f}% of total revenue) 
            from {int(top_product['Orders']):,} orders with {int(top_product['Quantity']):,} units sold.
        </div>""",
        unsafe_allow_html=True
    )
    
    # Country concentration
    uk_rev = country_revenue[country_revenue["Country"] == "United Kingdom"]["Revenue"].sum()
    non_uk_rev = total_rev - uk_rev
    non_uk_countries = len(country_revenue[country_revenue["Country"] != "United Kingdom"])
    st.markdown(
        f"""<div class="insight-box">
            <strong>🌍 MARKET ANALYSIS:</strong> International sales across {non_uk_countries} countries 
            generate {fmt_currency(non_uk_rev)} ({non_uk_rev/total_rev*100:.1f}% of revenue). 
            The top non-UK markets represent significant growth opportunities for market expansion.
        </div>""",
        unsafe_allow_html=True
    )
    
    # Low performer insight
    if len(products_min_orders) > 0:
        bottom_product = products_min_orders.nsmallest(1, "Revenue").iloc[0]
        st.markdown(
            f"""<div class="insight-box">
                <strong>📉 LOW PERFORMER:</strong> "{bottom_product['Description']}" has the lowest revenue 
                among products with at least 5 orders, generating only {fmt_currency(bottom_product['Revenue'])} 
                from {int(bottom_product['Orders']):,} orders. Such products may need pricing review or 
                discontinuation evaluation.
            </div>""",
            unsafe_allow_html=True
        )


# ============================================================
# PAGE 3: CUSTOMER & RISK ANALYSIS
# ============================================================
def page_customer_risk(df, full_df, cols):
    st.markdown('<div class="main-header">👥 Customer & Risk Analysis</div>', unsafe_allow_html=True)
    
    if len(df) == 0:
        st.warning("No data available for the selected filters.")
        return
    
    # Customer Analysis (only rows with customer ID)
    cust_df = df[df["HasCustomerID"]].copy()
    
    st.markdown('<div class="sub-header">👥 Customer Analysis</div>', unsafe_allow_html=True)
    
    if len(cust_df) > 0:
        total_customers = cust_df["Customer ID"].nunique()
        
        # Customer revenue
        customer_revenue = cust_df.groupby("Customer ID").agg(
            Revenue=("Revenue", "sum"),
            Orders=("Invoice", "nunique"),
            Quantity=("Quantity", "sum"),
            FirstPurchase=("InvoiceDate", "min"),
            LastPurchase=("InvoiceDate", "max"),
            Countries=("Country", "first")
        ).reset_index()
        
        # Customer KPIs
        avg_rev_per_cust = customer_revenue["Revenue"].mean()
        median_rev_per_cust = customer_revenue["Revenue"].median()
        repeat_customers = customer_revenue[customer_revenue["Orders"] > 1]
        repeat_rate = len(repeat_customers) / total_customers * 100 if total_customers > 0 else 0
        
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(render_kpi_card("Total Customers", fmt_number(total_customers), "kpi-card"), unsafe_allow_html=True)
        with k2:
            st.markdown(render_kpi_card("Avg Revenue/Customer", fmt_currency(avg_rev_per_cust), "kpi-card-green"), unsafe_allow_html=True)
        with k3:
            st.markdown(render_kpi_card("Repeat Purchase Rate", f"{repeat_rate:.1f}%", "kpi-card-orange"), unsafe_allow_html=True)
        with k4:
            st.markdown(render_kpi_card("Median Revenue/Customer", fmt_currency(median_rev_per_cust), "kpi-card-blue"), unsafe_allow_html=True)
        
        st.markdown("")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 customers by revenue
            top_customers = customer_revenue.nlargest(10, "Revenue")
            fig_topc = px.bar(
                top_customers,
                x="Revenue",
                y="Customer ID",
                orientation="h",
                title="Top 10 Customers by Revenue",
                color_discrete_sequence=["#4361ee"],
                template="plotly_white"
            )
            fig_topc.update_layout(height=400, yaxis=dict(autorange="reversed"), yaxis_title="Customer ID")
            st.plotly_chart(fig_topc, use_container_width=True)
        
        with col2:
            # Customer revenue distribution
            fig_dist = px.histogram(
                customer_revenue,
                x="Revenue",
                nbins=50,
                title="Customer Revenue Distribution",
                color_discrete_sequence=["#2d6a4f"],
                template="plotly_white"
            )
            fig_dist.update_layout(
                height=400,
                xaxis_title="Revenue (£)",
                yaxis_title="Number of Customers"
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        # Customer Concentration Analysis
        st.markdown('<div class="sub-header">📊 Customer Concentration</div>', unsafe_allow_html=True)
        
        customer_revenue_sorted = customer_revenue.sort_values("Revenue", ascending=False)
        customer_revenue_sorted["Cumulative_Revenue"] = customer_revenue_sorted["Revenue"].cumsum()
        customer_revenue_sorted["Cumulative_Pct"] = (customer_revenue_sorted["Cumulative_Revenue"] / customer_revenue_sorted["Revenue"].sum()) * 100
        customer_revenue_sorted["Customer_Rank_Pct"] = (np.arange(1, len(customer_revenue_sorted) + 1) / len(customer_revenue_sorted)) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_lorenz = go.Figure()
            fig_lorenz.add_trace(go.Scatter(
                x=customer_revenue_sorted["Customer_Rank_Pct"],
                y=customer_revenue_sorted["Cumulative_Pct"],
                mode="lines",
                name="Revenue Concentration",
                line=dict(color="#e63946", width=2)
            ))
            fig_lorenz.add_trace(go.Scatter(
                x=[0, 100],
                y=[0, 100],
                mode="lines",
                name="Perfect Equality",
                line=dict(color="gray", dash="dash")
            ))
            fig_lorenz.update_layout(
                title="Customer Revenue Concentration Curve",
                xaxis_title="% of Customers (ranked by revenue)",
                yaxis_title="% of Total Revenue",
                template="plotly_white",
                height=400
            )
            st.plotly_chart(fig_lorenz, use_container_width=True)
        
        with col2:
            # Top 20% customers' contribution
            top20_cutoff = int(total_customers * 0.20)
            top20_revenue = customer_revenue_sorted.head(top20_cutoff)["Revenue"].sum()
            top20_pct = top20_revenue / customer_revenue_sorted["Revenue"].sum() * 100
            
            pareto_data = pd.DataFrame({
                "Segment": ["Top 20% Customers", "Bottom 80% Customers"],
                "Revenue": [top20_revenue, customer_revenue_sorted["Revenue"].sum() - top20_revenue]
            })
            
            fig_pareto = px.pie(
                pareto_data,
                values="Revenue",
                names="Segment",
                title=f"Pareto Analysis: Top 20% Customers = {top20_pct:.1f}% Revenue",
                color_discrete_sequence=["#e63946", "#adb5bd"],
                template="plotly_white"
            )
            fig_pareto.update_layout(height=400)
            st.plotly_chart(fig_pareto, use_container_width=True)
        
        # Monthly active customers
        st.markdown('<div class="sub-header">📈 Monthly Active Customers</div>', unsafe_allow_html=True)
        
        monthly_customers = cust_df.groupby("YearMonth")["Customer ID"].nunique().reset_index()
        monthly_customers.columns = ["YearMonth", "Active_Customers"]
        monthly_customers = monthly_customers.sort_values("YearMonth")
        
        fig_mac = go.Figure()
        fig_mac.add_trace(go.Scatter(
            x=monthly_customers["YearMonth"],
            y=monthly_customers["Active_Customers"],
            mode="lines+markers",
            line=dict(color="#4361ee", width=2),
            marker=dict(size=6)
        ))
        fig_mac.update_layout(
            title="Monthly Active Customers",
            xaxis_title="Month",
            yaxis_title="Active Customers",
            template="plotly_white",
            height=350
        )
        st.plotly_chart(fig_mac, use_container_width=True)
    else:
        st.info("No customer identification data available in the filtered dataset.")
    
    # ---- RISK ANALYSIS ----
    st.markdown("---")
    st.markdown('<div class="sub-header">⚠️ Risk Analysis</div>', unsafe_allow_html=True)
    
    risks = generate_risks(df, full_df, cols)
    
    if risks:
        for i, risk in enumerate(risks, 1):
            st.markdown(
                f"""<div class="risk-box">
                    <strong>⚠️ RISK {i}: {risk['risk']}</strong><br><br>
                    <strong>📊 EVIDENCE:</strong> {risk['evidence']}<br><br>
                    <strong>💥 POTENTIAL IMPACT:</strong> {risk['impact']}
                </div>""",
                unsafe_allow_html=True
            )
    else:
        st.info("No significant risks identified in the current data selection.")


def generate_risks(df, full_df, cols):
    """Generate data-driven risk assessments."""
    risks = []
    total_revenue = df["Revenue"].sum()
    
    # Risk 1: Geographic concentration
    country_rev = df.groupby("Country")["Revenue"].sum().sort_values(ascending=False)
    if len(country_rev) > 0:
        top_country_pct = country_rev.iloc[0] / total_revenue * 100
        if top_country_pct > 70:
            risks.append({
                "risk": "High Geographic Revenue Concentration",
                "evidence": f"{country_rev.index[0]} accounts for {top_country_pct:.1f}% of total revenue ({fmt_currency(country_rev.iloc[0])}). The remaining {len(country_rev)-1} countries contribute only {100-top_country_pct:.1f}%.",
                "impact": f"Any market disruption in {country_rev.index[0]} (economic downturn, regulatory changes, Brexit impacts) could severely affect the business. Over-dependence on a single market limits growth potential and increases vulnerability."
            })
    
    # Risk 2: Revenue decline in recent months
    monthly_rev = df.groupby("YearMonth")["Revenue"].sum().sort_index()
    if len(monthly_rev) >= 4:
        last_4 = monthly_rev.tail(4)
        if last_4.iloc[-1] < last_4.iloc[0]:
            decline_pct = ((last_4.iloc[-1] - last_4.iloc[0]) / last_4.iloc[0]) * 100
            if decline_pct < -10:
                risks.append({
                    "risk": "Declining Revenue Trend",
                    "evidence": f"Revenue declined by {abs(decline_pct):.1f}% over the last 4 months of data, from {fmt_currency(last_4.iloc[0])} to {fmt_currency(last_4.iloc[-1])}.",
                    "impact": "A sustained revenue decline threatens business sustainability, may indicate loss of market share, customer attrition, or product relevance issues that require immediate strategic intervention."
                })
    
    # Risk 3: Customer concentration
    cust_df = df[df["HasCustomerID"]]
    if len(cust_df) > 0:
        cust_rev = cust_df.groupby("Customer ID")["Revenue"].sum().sort_values(ascending=False)
        total_cust = len(cust_rev)
        if total_cust >= 10:
            top10_pct = cust_rev.head(10).sum() / cust_rev.sum() * 100
            if top10_pct > 15:
                risks.append({
                    "risk": "Customer Concentration Risk",
                    "evidence": f"The top 10 customers contribute {top10_pct:.1f}% of customer-attributed revenue ({fmt_currency(cust_rev.head(10).sum())}). Losing even one high-value customer could significantly impact revenue.",
                    "impact": "Heavy reliance on a small number of customers creates vulnerability. Loss of key accounts, changes in purchasing behavior, or competitor poaching could lead to sudden revenue drops."
                })
    
    # Risk 4: Missing customer data
    missing_cust_pct = (~df["HasCustomerID"]).sum() / len(df) * 100
    if missing_cust_pct > 20:
        risks.append({
            "risk": "Incomplete Customer Data",
            "evidence": f"{missing_cust_pct:.1f}% of transactions ({(~df['HasCustomerID']).sum():,} rows) lack customer identification, representing {fmt_currency(df[~df['HasCustomerID']]['Revenue'].sum())} in untracked revenue.",
            "impact": "Without customer IDs, the business cannot effectively analyze customer lifetime value, segment customers, personalize marketing, or measure customer retention. This data gap limits strategic decision-making."
        })
    
    # Risk 5: Low-value transactions
    median_rev = df.groupby("Invoice")["Revenue"].sum().median()
    low_value_orders = df.groupby("Invoice")["Revenue"].sum()
    low_value_pct = (low_value_orders < 10).sum() / len(low_value_orders) * 100
    if low_value_pct > 20:
        risks.append({
            "risk": "High Volume of Low-Value Transactions",
            "evidence": f"{low_value_pct:.1f}% of orders have a total value below £10. The median order value is {fmt_currency(median_rev)}.",
            "impact": "Low-value transactions may not cover fulfillment and shipping costs, reducing overall profitability. High volumes of small orders also strain operational capacity."
        })
    
    return risks


# ============================================================
# PAGE 4: OPPORTUNITIES
# ============================================================
def page_opportunities(df, cols):
    st.markdown('<div class="main-header">🌟 Business Opportunities</div>', unsafe_allow_html=True)
    
    if len(df) == 0:
        st.warning("No data available for the selected filters.")
        return
    
    opportunities = generate_opportunities(df, cols)
    
    for i, opp in enumerate(opportunities, 1):
        st.markdown(
            f"""<div class="opportunity-box">
                <strong>🌟 OPPORTUNITY {i}: {opp['opportunity']}</strong><br><br>
                <strong>📊 EVIDENCE:</strong> {opp['evidence']}<br><br>
                <strong>🎯 WHY IT MATTERS:</strong> {opp['why_it_matters']}
            </div>""",
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Opportunity Visualizations
    st.markdown('<div class="sub-header">📊 Growth Opportunities - Visual Evidence</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # International markets potential
        country_rev = df.groupby("Country").agg(
            Revenue=("Revenue", "sum"),
            Orders=("Invoice", "nunique"),
            Customers=("Customer ID", "nunique")
        ).reset_index()
        
        # Non-UK markets
        intl = country_rev[country_rev["Country"] != "United Kingdom"].nlargest(10, "Revenue")
        if len(intl) > 0:
            fig_intl = px.bar(
                intl,
                x="Revenue",                y="Country",
                orientation="h",
                title="Top 10 International Markets by Revenue",
                color="Revenue",
                color_continuous_scale="Greens",
                template="plotly_white"
            )
            fig_intl.update_layout(height=400, yaxis=dict(autorange="reversed"), showlegend=False)
            st.plotly_chart(fig_intl, use_container_width=True)
    
    with col2:
        # Monthly revenue trend with trendline
        monthly_rev = df.groupby("YearMonth")["Revenue"].sum().reset_index()
        monthly_rev = monthly_rev.sort_values("YearMonth")
        monthly_rev["Month_Num"] = range(len(monthly_rev))
        
        fig_trend = px.scatter(
            monthly_rev,
            x="YearMonth",
            y="Revenue",
            title="Revenue Trend with Growth Potential",
            trendline="ols",
            template="plotly_white",
            color_discrete_sequence=["#4361ee"]
        )
        fig_trend.update_layout(height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Top growing products
    st.markdown('<div class="sub-header">🚀 High-Demand Products</div>', unsafe_allow_html=True)
    
    product_stats = df.groupby("Description").agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Invoice", "nunique"),
        Avg_Price=("Price", "mean")
    ).reset_index()
    
    # Products with high order frequency
    high_demand = product_stats.nlargest(15, "Orders")
    
    fig_demand = px.scatter(
        high_demand,
        x="Orders",
        y="Revenue",
        size="Quantity",
        hover_name="Description",
        title="High-Demand Products: Orders vs Revenue (bubble size = quantity)",
        color="Revenue",
        color_continuous_scale="Viridis",
        template="plotly_white"
    )
    fig_demand.update_layout(height=450)
    st.plotly_chart(fig_demand, use_container_width=True)


def generate_opportunities(df, cols):
    """Generate data-driven opportunity assessments."""
    opportunities = []
    total_revenue = df["Revenue"].sum()
    
    # Opportunity 1: International market expansion
    country_rev = df.groupby("Country").agg(
        Revenue=("Revenue", "sum"),
        Orders=("Invoice", "nunique")
    ).sort_values("Revenue", ascending=False).reset_index()
    
    non_uk = country_rev[country_rev["Country"] != "United Kingdom"]
    if len(non_uk) > 0:
        top_intl = non_uk.head(3)
        intl_names = ", ".join(top_intl["Country"].tolist())
        intl_rev = non_uk["Revenue"].sum()
        opportunities.append({
            "opportunity": "International Market Expansion",
            "evidence": f"{len(non_uk)} international markets already generate {fmt_currency(intl_rev)} ({intl_rev/total_revenue*100:.1f}% of revenue). Top international markets ({intl_names}) show proven demand for the product portfolio.",
            "why_it_matters": "International markets represent untapped growth potential. The existing cross-border demand validates product-market fit across multiple geographies. Targeted marketing, localized pricing, or partnerships in top-performing international markets could significantly increase revenue without the risks of entering entirely new markets."
        })
    
    # Opportunity 2: High-performing products
    product_rev = df.groupby("Description").agg(
        Revenue=("Revenue", "sum"),
        Orders=("Invoice", "nunique"),
        Quantity=("Quantity", "sum")
    ).sort_values("Revenue", ascending=False).reset_index()
    
    top5_products = product_rev.head(5)
    top5_rev = top5_products["Revenue"].sum()
    top5_pct = top5_rev / total_revenue * 100
    
    opportunities.append({
        "opportunity": "Capitalize on Top-Performing Products",
        "evidence": f"The top 5 products by revenue generate {fmt_currency(top5_rev)} ({top5_pct:.1f}% of total revenue). The leading product, \"{top5_products.iloc[0]['Description']}\", alone generates {fmt_currency(top5_products.iloc[0]['Revenue'])} from {int(top5_products.iloc[0]['Orders']):,} orders.",
        "why_it_matters": "High-performing products have proven market demand. Expanding variants, bundling with related products, increasing marketing spend on these items, or ensuring stock availability can drive incremental revenue from established demand."
    })
    
    # Opportunity 3: Day/Time optimization
    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow_rev = df.groupby("DayOfWeek")["Revenue"].sum()
    peak_day = dow_rev.idxmax()
    weak_day = dow_rev.idxmin()
    peak_rev = dow_rev.max()
    weak_rev = dow_rev.min()
    
    opportunities.append({
        "opportunity": "Optimize Sales by Day-of-Week Patterns",
        "evidence": f"{peak_day} generates the highest revenue ({fmt_currency(peak_rev)}) while {weak_day} generates the lowest ({fmt_currency(weak_rev)}). The gap is {fmt_currency(peak_rev - weak_rev)} ({((peak_rev - weak_rev)/weak_rev*100):.0f}% difference).",
        "why_it_matters": "Understanding day-of-week sales patterns enables smarter resource allocation. Targeted promotions on low-performing days could boost sales, while ensuring peak-day operations are optimized can capture maximum revenue from existing demand."
    })
    
    # Opportunity 4: Customer retention
    cust_df = df[df["HasCustomerID"]]
    if len(cust_df) > 0:
        cust_orders = cust_df.groupby("Customer ID")["Invoice"].nunique()
        one_time = (cust_orders == 1).sum()
        repeat = (cust_orders > 1).sum()
        one_time_pct = one_time / len(cust_orders) * 100
        
        if one_time_pct > 30:
            opportunities.append({
                "opportunity": "Improve Customer Retention",
                "evidence": f"{one_time:,} customers ({one_time_pct:.1f}%) made only one purchase. Repeat customers ({repeat:,}) generate significantly higher lifetime value. Average revenue from repeat customers is {fmt_currency(cust_df[cust_df['Customer ID'].isin(cust_orders[cust_orders > 1].index)].groupby('Customer ID')['Revenue'].sum().mean())}.",
                "why_it_matters": "Converting one-time buyers into repeat customers is typically 5-7x more cost-effective than acquiring new customers. Implementing targeted re-engagement campaigns, loyalty programs, or post-purchase follow-ups could significantly increase customer lifetime value."
            })
    
    # Opportunity 5: Peak seasonal planning
    monthly_rev = df.groupby("YearMonth")["Revenue"].sum().sort_index()
    if len(monthly_rev) >= 6:
        peak_month = monthly_rev.idxmax()
        peak_month_rev = monthly_rev.max()
        avg_month_rev = monthly_rev.mean()
        
        opportunities.append({
            "opportunity": "Seasonal Demand Optimization",
            "evidence": f"Peak month ({peak_month}) generated {fmt_currency(peak_month_rev)}, which is {((peak_month_rev/avg_month_rev - 1) * 100):.0f}% above the monthly average of {fmt_currency(avg_month_rev)}.",
            "why_it_matters": "Strong seasonal patterns indicate predictable demand surges. Pre-positioning inventory, scaling fulfillment capacity, and launching marketing campaigns ahead of peak months can maximize revenue capture during high-demand periods."
        })
    
    return opportunities


# ============================================================
# PAGE 5: RECOMMENDED ACTIONS
# ============================================================
def page_recommended_actions(df, full_df, cols):
    st.markdown('<div class="main-header">🎯 Recommended Business Actions</div>', unsafe_allow_html=True)
    
    if len(df) == 0:
        st.warning("No data available for the selected filters.")
        return
    
    st.markdown("""
    <div style="background: #f0f2f6; padding: 1rem 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;">
        <strong>Methodology:</strong> Each recommendation follows the structured Business Intelligence flow:<br>
        <strong>FACT</strong> → <strong>INSIGHT</strong> → <strong>RISK / OPPORTUNITY</strong> → <strong>RECOMMENDED ACTION</strong><br><br>
        All facts are derived from actual data analysis. Recommendations are actionable and specific.
    </div>
    """, unsafe_allow_html=True)
    
    actions = generate_recommended_actions(df, full_df, cols)
    
    for i, action in enumerate(actions, 1):
        icon = action.get("icon", "🎯")
        action_type = action.get("type", "OPPORTUNITY")
        type_color = "#2d6a4f" if action_type == "OPPORTUNITY" else "#e63946"
        
        st.markdown(
            f"""<div class="action-box">
                <h4>{icon} Action {i}: {action['title']}</h4>
                <strong>📌 FACT:</strong> {action['fact']}<br><br>
                <strong>💡 INSIGHT:</strong> {action['insight']}<br><br>
                <strong style="color: {type_color};">{'🌟' if action_type == 'OPPORTUNITY' else '⚠️'} {action_type}:</strong> {action['risk_or_opportunity']}<br><br>
                <strong>🎯 RECOMMENDED ACTION:</strong> {action['action']}
            </div>""",
            unsafe_allow_html=True
        )
    
    # Action Priority Matrix
    st.markdown("---")
    st.markdown('<div class="sub-header">📊 Action Priority Matrix</div>', unsafe_allow_html=True)
    
    priority_data = []
    for i, action in enumerate(actions, 1):
        priority_data.append({
            "Action": f"Action {i}",
            "Title": action["title"],
            "Impact": action.get("impact_score", 3),
            "Urgency": action.get("urgency_score", 3),
            "Type": action.get("type", "OPPORTUNITY")
        })
    
    priority_df = pd.DataFrame(priority_data)
    
    fig_priority = px.scatter(
        priority_df,
        x="Urgency",
        y="Impact",
        text="Action",
        color="Type",
        title="Action Priority Matrix (Impact vs Urgency)",
        template="plotly_white",        color_discrete_map={"OPPORTUNITY": "#2d6a4f", "RISK": "#e63946"},
        size_max=20
    )
    fig_priority.update_traces(textposition="top center", marker=dict(size=15))
    fig_priority.update_layout(
        height=400,
        xaxis=dict(title="Urgency →", range=[0.5, 5.5]),
        yaxis=dict(title="Impact →", range=[0.5, 5.5])
    )
    
    # Add quadrant labels
    fig_priority.add_annotation(x=1.5, y=4.5, text="Monitor", showarrow=False, font=dict(color="gray", size=12))
    fig_priority.add_annotation(x=4.5, y=4.5, text="Act Now", showarrow=False, font=dict(color="gray", size=12))
    fig_priority.add_annotation(x=1.5, y=1.5, text="Low Priority", showarrow=False, font=dict(color="gray", size=12))
    fig_priority.add_annotation(x=4.5, y=1.5, text="Quick Wins", showarrow=False, font=dict(color="gray", size=12))
    
    st.plotly_chart(fig_priority, use_container_width=True)
    
    # Summary Table
    st.markdown('<div class="sub-header">📋 Action Summary</div>', unsafe_allow_html=True)
    
    summary_data = []
    for i, action in enumerate(actions, 1):
        summary_data.append({
            "#": i,
            "Action": action["title"],
            "Type": action.get("type", "OPPORTUNITY"),
            "Priority": "High" if action.get("impact_score", 3) >= 4 else "Medium" if action.get("impact_score", 3) >= 3 else "Low"
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)


def generate_recommended_actions(df, full_df, cols):
    """Generate data-driven recommended actions."""
    actions = []
    total_revenue = df["Revenue"].sum()
    
    # Action 1: Market Diversification
    country_rev = df.groupby("Country")["Revenue"].sum().sort_values(ascending=False)
    top_country = country_rev.index[0]
    top_country_pct = country_rev.iloc[0] / total_revenue * 100
    
    non_uk = country_rev[country_rev.index != "United Kingdom"]
    top_intl = non_uk.head(3)
    
    actions.append({
        "title": "Diversify Geographic Revenue",
        "fact": f"{top_country} contributes {top_country_pct:.1f}% of total revenue ({fmt_currency(country_rev.iloc[0])}). International markets collectively contribute only {100-top_country_pct:.1f}%.",
        "insight": "The business is highly dependent on a single market, creating significant concentration risk.",
        "risk_or_opportunity": f"Top 3 international markets ({', '.join(top_intl.index[:3].tolist())}) already generate {fmt_currency(top_intl.sum())} combined, proving demand exists beyond the domestic market.",
        "action": f"Develop targeted market entry strategies for the top 3 international markets. Invest in localized marketing, consider local warehousing or fulfillment partnerships to reduce shipping costs, and set a target to increase international revenue share from {100-top_country_pct:.1f}% to at least {min(100-top_country_pct+10, 40):.0f}% within 12 months.",
        "type": "OPPORTUNITY",
        "icon": "🌍",
        "impact_score": 5,
        "urgency_score": 4
    })
    
    # Action 2: Product Portfolio Optimization
    product_rev = df.groupby("Description").agg(
        Revenue=("Revenue", "sum"),
        Orders=("Invoice", "nunique"),
        Quantity=("Quantity", "sum")
    ).sort_values("Revenue", ascending=False).reset_index()
    
    top_product = product_rev.iloc[0]
    top5_rev = product_rev.head(5)["Revenue"].sum()
    top5_pct = top5_rev / total_revenue * 100
    total_products = len(product_rev)
    bottom50_rev = product_rev.tail(total_products // 2)["Revenue"].sum()
    bottom50_pct = bottom50_rev / total_revenue * 100
    
    actions.append({
        "title": "Optimize Product Portfolio",
        "fact": f"Top 5 products generate {fmt_currency(top5_rev)} ({top5_pct:.1f}% of revenue), while the bottom {total_products // 2:,} products contribute only {bottom50_pct:.1f}% of revenue.",
        "insight": "A small number of products drive the majority of revenue, suggesting a long tail of underperforming products that may not justify inventory and management costs.",
        "risk_or_opportunity": "Focusing resources on proven top performers while evaluating the long tail can improve operational efficiency and profitability.",
        "action": f"Review the bottom 50% of products for potential discontinuation or price adjustments. Ensure top performers like \"{top_product['Description']}\" always have adequate stock. Consider cross-selling top products with complementary items to increase average order value.",
        "type": "OPPORTUNITY",
        "icon": "📦",
        "impact_score": 4,
        "urgency_score": 3
    })
    
    # Action 3: Customer Retention
    cust_df = df[df["HasCustomerID"]]
    if len(cust_df) > 0:
        cust_orders = cust_df.groupby("Customer ID")["Invoice"].nunique()
        one_time = (cust_orders == 1).sum()
        total_cust = len(cust_orders)
        one_time_pct = one_time / total_cust * 100
        
        repeat_cust = cust_orders[cust_orders > 1]
        repeat_avg_rev = cust_df[cust_df["Customer ID"].isin(repeat_cust.index)].groupby("Customer ID")["Revenue"].sum().mean()
        one_time_avg_rev = cust_df[cust_df["Customer ID"].isin(cust_orders[cust_orders == 1].index)].groupby("Customer ID")["Revenue"].sum().mean()
        
        actions.append({
            "title": "Implement Customer Retention Program",
            "fact": f"{one_time:,} customers ({one_time_pct:.1f}%) made only a single purchase. Repeat customers average {fmt_currency(repeat_avg_rev)} in lifetime revenue vs {fmt_currency(one_time_avg_rev)} for one-time buyers.",
            "insight": f"Repeat customers generate {repeat_avg_rev/one_time_avg_rev:.1f}x more revenue than one-time buyers, highlighting the significant value of customer retention.",
            "risk_or_opportunity": f"Converting even 10% of one-time buyers to repeat customers could add approximately {fmt_currency(one_time * 0.10 * (repeat_avg_rev - one_time_avg_rev))} in additional revenue.",
            "action": "Launch a customer retention program: (1) Implement post-purchase email follow-ups with product recommendations, (2) Create a loyalty rewards program for repeat purchases, (3) Offer targeted discounts to customers who haven't purchased in 60+ days, (4) Monitor customer churn rate monthly.",
            "type": "OPPORTUNITY",
            "icon": "👥",
            "impact_score": 5,
            "urgency_score": 4
        })
    
    # Action 4: Data Quality Improvement
    missing_cust_pct = (~df["HasCustomerID"]).sum() / len(df) * 100
    if missing_cust_pct > 10:
        missing_rev = df[~df["HasCustomerID"]]["Revenue"].sum()
        actions.append({
            "title": "Improve Customer Data Capture",
            "fact": f"{missing_cust_pct:.1f}% of transactions ({(~df['HasCustomerID']).sum():,} records) have no customer identification, representing {fmt_currency(missing_rev)} in untracked revenue.",
            "insight": "Without customer IDs, the business cannot perform accurate customer lifetime value analysis, personalize marketing, or effectively measure retention.",
            "risk_or_opportunity": "Incomplete data limits the ability to make data-driven customer decisions and may result in missed revenue opportunities.",
            "action": "Implement mandatory customer registration at checkout. Offer incentives (e.g., first-order discount, loyalty points) for account creation. Integrate CRM systems to ensure all transactions are linked to customer profiles. Target reducing unidentified transactions to below 5% within 6 months.",
            "type": "RISK",
            "icon": "📊",
            "impact_score": 4,
            "urgency_score": 5
        })
    
    # Action 5: Seasonal Planning
    monthly_rev = df.groupby("YearMonth")["Revenue"].sum().sort_index()
    if len(monthly_rev) >= 6:
        peak_month = monthly_rev.idxmax()
        peak_rev = monthly_rev.max()
        avg_rev = monthly_rev.mean()
        low_month = monthly_rev.idxmin()
        low_rev = monthly_rev.min()
        
        actions.append({
            "title": "Strategic Seasonal Planning",
            "fact": f"Revenue varies significantly by month: peak month ({peak_month}) generated {fmt_currency(peak_rev)} while the lowest month ({low_month}) generated only {fmt_currency(low_rev)}. Monthly average is {fmt_currency(avg_rev)}.",
            "insight": f"The {((peak_rev/low_rev)):.1f}x difference between peak and low months indicates strong seasonality that can be strategically managed.",
            "risk_or_opportunity": "Proper seasonal planning can maximize revenue during peaks and reduce losses during troughs.",
            "action": f"Develop a seasonal business calendar: (1) Pre-stock high-demand products 4-6 weeks before {peak_month}, (2) Plan promotional campaigns during historically low months to stimulate demand, (3) Adjust staffing levels to match seasonal patterns, (4) Create seasonal product bundles to increase average order value during peak periods.",
            "type": "OPPORTUNITY",
            "icon": "📅",
            "impact_score": 4,
            "urgency_score": 3
        })
    
    # Action 6: Operational Efficiency
    dow_rev = df.groupby("DayOfWeek")["Revenue"].sum()
    hour_rev = df.groupby("Hour")["Revenue"].sum()
    peak_day = dow_rev.idxmax()
    peak_hour = hour_rev.idxmax()
    
    actions.append({
        "title": "Optimize Operational Scheduling",
        "fact": f"Peak sales day is {peak_day} ({fmt_currency(dow_rev.max())} revenue), and peak sales hour is {int(peak_hour)}:00 ({fmt_currency(hour_rev.max())} revenue).",
        "insight": "Sales patterns show clear day-of-week and time-of-day preferences that should inform resource allocation.",
        "risk_or_opportunity": "Aligning operational resources with demand patterns can reduce costs and improve customer experience.",
        "action": f"Align staffing and customer support capacity to peak hours (around {int(peak_hour)}:00). Schedule marketing email campaigns and promotions for {peak_day} when purchase intent is highest. Consider special promotions on low-traffic days to balance demand. Ensure website infrastructure can handle peak-hour load.",
        "type": "OPPORTUNITY",
        "icon": "⚡",
        "impact_score": 3,
        "urgency_score": 2
    })
    
    return actions


# ============================================================
# PAGE 6: DATA QUALITY
# ============================================================
def page_data_quality(df, raw_stats, cols):
    st.markdown('<div class="main-header">🔍 Data Quality Report</div>', unsafe_allow_html=True)
    
    # Dataset Info
    st.markdown('<div class="sub-header">📋 Dataset Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        | Property | Value |
        |----------|-------|
        | **Dataset Name** | Online Retail II |
        | **Source** | UCI Machine Learning Repository |
        | **Source URL** | [archive.ics.uci.edu/dataset/502](https://archive.ics.uci.edu/dataset/502/online+retail+ii) |
        | **Total Raw Rows** | {raw_stats['total_rows']:,} |
        | **Total Columns** | {raw_stats['total_columns']} |
        | **Columns** | {', '.join(raw_stats['columns'])} |
        """)
    
    with col2:
        st.markdown(f"""
        | Property | Value |
        |----------|-------|
        | **Date Range** | {raw_stats.get('date_min', 'N/A')} to {raw_stats.get('date_max', 'N/A')} |
        | **Cleaned Rows** | {raw_stats.get('cleaned_rows', 'N/A'):,} |
        | **Duplicate Rows (Raw)** | {raw_stats['duplicate_rows']:,} |
        | **Rows Removed** | {raw_stats['total_rows'] - raw_stats.get('cleaned_rows', raw_stats['total_rows']):,} |
        | **Cleaning Ratio** | {raw_stats.get('cleaned_rows', 0) / raw_stats['total_rows'] * 100:.1f}% retained |
        """)    
    # Missing Values
    st.markdown('<div class="sub-header">❓ Missing Values (Raw Data)</div>', unsafe_allow_html=True)
    
    missing_data = pd.DataFrame({
        "Column": raw_stats["missing_values"].keys(),
        "Missing Count": raw_stats["missing_values"].values(),
        "Missing %": [v / raw_stats["total_rows"] * 100 for v in raw_stats["missing_values"].values()]
    })
    missing_data = missing_data.sort_values("Missing Count", ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(missing_data, use_container_width=True, hide_index=True)
    
    with col2:
        fig_missing = px.bar(
            missing_data[missing_data["Missing Count"] > 0],
            x="Column",
            y="Missing %",
            title="Missing Values by Column (%)",
            color_discrete_sequence=["#e63946"],
            template="plotly_white"
        )
        fig_missing.update_layout(height=350)
        st.plotly_chart(fig_missing, use_container_width=True)
    
    # Data Types
    st.markdown('<div class="sub-header">🔧 Data Types</div>', unsafe_allow_html=True)
    
    dtype_data = pd.DataFrame({
        "Column": raw_stats["dtypes"].keys(),
        "Data Type": raw_stats["dtypes"].values()
    })
    st.dataframe(dtype_data, use_container_width=True, hide_index=True)
    
    # Cleaning Log
    st.markdown('<div class="sub-header">🧹 Data Cleaning Steps</div>', unsafe_allow_html=True)
    
    for i, step in enumerate(raw_stats.get("cleaning_log", []), 1):
        st.markdown(f"**Step {i}:** {step}")
    
    # Cleaned Data Summary
    st.markdown('<div class="sub-header">✅ Cleaned Data Summary</div>', unsafe_allow_html=True)
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Cleaned Rows", f"{len(df):,}")
    with k2:
        st.metric("Total Columns", f"{len(df.columns)}")
    with k3:
        date_range = f"{df['InvoiceDate'].min().strftime('%Y-%m-%d')} to {df['InvoiceDate'].max().strftime('%Y-%m-%d')}"
        st.metric("Date Range", date_range)
    with k4:
        st.metric("Countries", f"{df['Country'].nunique()}")


# ============================================================
# RUN APPLICATION
# ============================================================
if __name__ == "__main__":
    main()