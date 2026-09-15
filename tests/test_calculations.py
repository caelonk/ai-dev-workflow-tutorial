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
