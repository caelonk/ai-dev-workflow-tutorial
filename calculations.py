import pandas as pd


def load_sales_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["date"])
