import plotly.express as px
import streamlit as st

from calculations import (
    load_sales_data,
    monthly_sales_trend,
    sales_by_category,
    sales_by_region,
    total_orders,
    total_sales,
)

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def load_data(path: str):
    return load_sales_data(path)


def render_kpis(df):
    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${total_sales(df):,.2f}")
    col2.metric("Total Orders", f"{total_orders(df):,}")


def render_trend_chart(df):
    st.subheader("Sales Trend Over Time")
    monthly = monthly_sales_trend(df)
    fig = px.line(monthly, x="month", y="sales", markers=True)
    fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
    st.plotly_chart(fig, width="stretch")


def render_category_chart(df):
    st.subheader("Sales by Category")
    data = sales_by_category(df)
    fig = px.bar(data, x="category", y="sales")
    fig.update_layout(xaxis_title="Category", yaxis_title="Sales ($)")
    st.plotly_chart(fig, width="stretch")


def render_region_chart(df):
    st.subheader("Sales by Region")
    data = sales_by_region(df)
    fig = px.bar(data, x="region", y="sales")
    fig.update_layout(xaxis_title="Region", yaxis_title="Sales ($)")
    st.plotly_chart(fig, width="stretch")


def main():
    st.title("ShopSmart Sales Dashboard")

    try:
        df = load_data(DATA_PATH)
    except FileNotFoundError:
        st.error(
            "Could not find data/sales-data.csv — make sure the file exists "
            "before running the dashboard."
        )
        st.stop()

    render_kpis(df)
    render_trend_chart(df)

    col1, col2 = st.columns(2)
    with col1:
        render_category_chart(df)
    with col2:
        render_region_chart(df)


if __name__ == "__main__":
    main()
