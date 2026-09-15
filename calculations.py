import pandas as pd


def load_sales_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["date"])


def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)


def monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.assign(month=df["date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .reset_index(drop=True)
    )
    return monthly.rename(columns={"total_amount": "sales"})


def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("category", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )
    return result.rename(columns={"total_amount": "sales"})


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("region", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )
    return result.rename(columns={"total_amount": "sales"})
