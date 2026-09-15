import streamlit as st

from calculations import load_sales_data, total_orders, total_sales

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def load_data(path: str):
    return load_sales_data(path)


def render_kpis(df):
    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${total_sales(df):,.2f}")
    col2.metric("Total Orders", f"{total_orders(df):,}")


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


if __name__ == "__main__":
    main()
