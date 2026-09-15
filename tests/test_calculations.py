import pandas as pd
import pytest

from calculations import load_sales_data


def test_load_sales_data_reads_csv(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-001,Widget,Electronics,North,2,10.00,20.00\n"
    )

    df = load_sales_data(str(csv_path))

    assert len(df) == 1
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_load_sales_data_missing_file_raises(tmp_path):
    missing_path = tmp_path / "does_not_exist.csv"

    with pytest.raises(FileNotFoundError):
        load_sales_data(str(missing_path))


from calculations import total_orders, total_sales


def _sample_sales_df():
    return pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-03", "2024-01-04", "2024-02-01"]),
            "category": ["Electronics", "Audio", "Electronics"],
            "region": ["North", "South", "East"],
            "total_amount": [100.0, 50.0, 25.0],
        }
    )


def test_total_sales():
    df = _sample_sales_df()
    assert total_sales(df) == 175.0


def test_total_orders():
    df = _sample_sales_df()
    assert total_orders(df) == 3


from calculations import monthly_sales_trend


def test_monthly_sales_trend():
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-02-01", "2024-01-03", "2024-01-04"]),
            "total_amount": [25.0, 100.0, 50.0],
        }
    )

    result = monthly_sales_trend(df)

    assert list(result["month"]) == [
        pd.Timestamp("2024-01-01"),
        pd.Timestamp("2024-02-01"),
    ]
    assert list(result["sales"]) == [150.0, 25.0]
