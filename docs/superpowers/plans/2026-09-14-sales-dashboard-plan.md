# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase 1 Streamlit sales dashboard (KPIs, monthly trend, category/region breakdowns) reading from `data/sales-data.csv`.

**Architecture:** A flat two-file layout — `calculations.py` holds pure, pytest-tested data functions with no Streamlit dependency; `app.py` holds page config, small per-section render functions, and a `main()` that wires them together. Each dashboard feature is built calculations-first (TDD) then wired into the UI, one milestone at a time.

**Tech Stack:** Python 3.11+, Streamlit, Pandas, Plotly, pytest, plain `venv`.

**Spec:** `docs/superpowers/specs/2026-09-14-sales-dashboard-design.md`

## Milestone mapping

This plan's own task numbers (Task 1, Task 2, …) are independent of the milestone IDs in `TASKS.md` (TASK-1 … TASK-5). Each plan task below is labeled with the milestone it belongs to — don't confuse the two numbering schemes.

| Plan task | Milestone |
|---|---|
| Task 1 | TASK-1 |
| Task 2 | TASK-1 |
| Task 3 | TASK-1 |
| Task 4 | TASK-2 |
| Task 5 | TASK-2 |
| Task 6 | TASK-3 |
| Task 7 | TASK-3 |
| Task 8 | TASK-4 |
| Task 9 | TASK-4 |
| Task 10 | TASK-5 |
| Handoff (unnumbered, human-executed) | TASK-5 |

## Global Constraints

- Work on the current branch (`feature/sales-dashboard`); do not create a git worktree.
- Use a plain `venv/` virtual environment with `requirements.txt` for dependencies (no uv, no conda).
- Data calculations live in `calculations.py`, with zero Streamlit imports, tested via pytest with hand-crafted fixture DataFrames (not the real CSV).
- Flat file layout: `app.py` and `calculations.py` at the repo root; tests in `tests/test_calculations.py`.
- Wrap the CSV load in `@st.cache_data`.
- The sales trend chart is aggregated **monthly**, not daily.
- Missing-CSV handling: catch `FileNotFoundError`, show one `st.error(...)` message, call `st.stop()`. No other validation.
- Every commit message includes the relevant milestone ID (`TASK-1` … `TASK-5`), per `TASKS.md`'s Definition of Done.
- Deployment (the end of TASK-5) is executed by the user manually after merging to `main` — it is a handoff, not an executable task in this plan.

---

### Task 1: Environment setup and minimal app shell

**Milestone:** TASK-1

**Files:**
- Create: `requirements.txt`
- Create: `app.py`

**Interfaces:**
- Consumes: nothing (first task)
- Produces: a runnable `app.py` with a `main()` function that later tasks will extend; `venv/` and installed dependencies that every later task assumes are active

- [ ] **Step 1: Create the virtual environment**

Run: `python -m venv venv`

- [ ] **Step 2: Activate it and confirm**

On Windows Git Bash: `source venv/Scripts/activate`
On Windows PowerShell: `venv\Scripts\Activate.ps1`

Expected: the shell prompt is prefixed with `(venv)`.

- [ ] **Step 3: Create `requirements.txt`**

```
streamlit
pandas
plotly
pytest
```

- [ ] **Step 4: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: installs complete with no errors.

- [ ] **Step 5: Create the minimal `app.py`**

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


def main():
    st.title("ShopSmart Sales Dashboard")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Verify it runs**

Run: `streamlit run app.py`
Expected: browser opens showing the page titled "ShopSmart Sales Dashboard" with no errors in the terminal. Stop the server (Ctrl+C) once confirmed.

- [ ] **Step 7: Commit**

```bash
git add requirements.txt app.py
git commit -m "TASK-1: set up venv, dependencies, and minimal app shell"
```

---

### Task 2: `load_sales_data` with tests

**Milestone:** TASK-1

**Files:**
- Create: `calculations.py`
- Create: `tests/test_calculations.py`

**Interfaces:**
- Consumes: nothing
- Produces: `load_sales_data(path: str) -> pd.DataFrame` (columns include `date` as parsed datetime), raising `FileNotFoundError` for a missing path — consumed by Task 3's `app.py` wiring

- [ ] **Step 1: Write the failing tests**

Create `tests/test_calculations.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_calculations.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'calculations'` (the file doesn't exist yet).

- [ ] **Step 3: Write the minimal implementation**

Create `calculations.py`:

```python
import pandas as pd


def load_sales_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["date"])
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_calculations.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-1: add load_sales_data with tests"
```

---

### Task 3: Wire CSV loading and error handling into the app

**Milestone:** TASK-1 (completes this milestone's acceptance criteria)

**Files:**
- Modify: `app.py` (replace entire file)

**Interfaces:**
- Consumes: `load_sales_data(path: str) -> pd.DataFrame` from Task 2
- Produces: `load_data(path: str) -> pd.DataFrame` (the `@st.cache_data`-wrapped loader), `DATA_PATH` constant, and a `main()` shape — `try: df = load_data(DATA_PATH) except FileNotFoundError: ...` — that Tasks 5, 7, and 9 will extend

- [ ] **Step 1: Replace `app.py`**

```python
import streamlit as st

from calculations import load_sales_data

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def load_data(path: str):
    return load_sales_data(path)


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


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify the happy path**

Run: `streamlit run app.py`
Expected: title renders, no errors in terminal or browser. Stop the server once confirmed.

- [ ] **Step 3: Verify the missing-file path (manual, reversible)**

Temporarily change `DATA_PATH = "data/sales-data.csv"` to `DATA_PATH = "data/does-not-exist.csv"`, run `streamlit run app.py`, and confirm the red error message appears and the page stops there with no traceback. Then change `DATA_PATH` back to `"data/sales-data.csv"` before continuing. Do not rename or move the real CSV file.

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "TASK-1: load CSV into the app with cached, handled loading"
```

---

### Task 4: KPI calculations with tests

**Milestone:** TASK-2

**Files:**
- Modify: `calculations.py` (append)
- Modify: `tests/test_calculations.py` (append)

**Interfaces:**
- Consumes: nothing new (operates on any DataFrame with a `total_amount` column)
- Produces: `total_sales(df) -> float`, `total_orders(df) -> int` — consumed by Task 5's `render_kpis`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_calculations.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_calculations.py -v`
Expected: FAIL with `ImportError: cannot import name 'total_orders'`.

- [ ] **Step 3: Write the minimal implementation**

Append to `calculations.py`:

```python
def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_calculations.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-2: add total_sales and total_orders with tests"
```

---

### Task 5: Render KPI cards

**Milestone:** TASK-2 (completes this milestone's acceptance criteria)

**Files:**
- Modify: `app.py` (replace entire file)

**Interfaces:**
- Consumes: `total_sales(df) -> float`, `total_orders(df) -> int` from Task 4
- Produces: `render_kpis(df) -> None`, and a `main()` that calls it after the load block — consumed by Tasks 7 and 9, which append further render calls after this one

- [ ] **Step 1: Replace `app.py`**

```python
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
```

- [ ] **Step 2: Verify manually**

Run: `streamlit run app.py`
Expected: two metric cards show "Total Sales" (formatted as currency, approximately $116,500) and "Total Orders" (482). Stop the server once confirmed.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-2: render KPI scorecards"
```

---

### Task 6: Monthly trend calculation with tests

**Milestone:** TASK-3

**Files:**
- Modify: `calculations.py` (append)
- Modify: `tests/test_calculations.py` (append)

**Interfaces:**
- Consumes: nothing new
- Produces: `monthly_sales_trend(df) -> pd.DataFrame` with columns `month` (Timestamp, chronologically sorted) and `sales` (float) — consumed by Task 7's `render_trend_chart`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_calculations.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_calculations.py -v`
Expected: FAIL with `ImportError: cannot import name 'monthly_sales_trend'`.

- [ ] **Step 3: Write the minimal implementation**

Append to `calculations.py`:

```python
def monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.assign(month=df["date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .sort_values("month")
        .reset_index(drop=True)
    )
    return monthly.rename(columns={"total_amount": "sales"})
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_calculations.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-3: add monthly_sales_trend with tests"
```

---

### Task 7: Render sales trend chart

**Milestone:** TASK-3 (completes this milestone's acceptance criteria)

**Files:**
- Modify: `app.py` (replace entire file)

**Interfaces:**
- Consumes: `monthly_sales_trend(df) -> pd.DataFrame` from Task 6
- Produces: `render_trend_chart(df) -> None`, appended in `main()` after `render_kpis(df)` — consumed by Task 9, which appends further render calls after this one

- [ ] **Step 1: Replace `app.py`**

```python
import plotly.express as px
import streamlit as st

from calculations import load_sales_data, monthly_sales_trend, total_orders, total_sales

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
    st.plotly_chart(fig, use_container_width=True)


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


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify manually**

Run: `streamlit run app.py`
Expected: a line chart titled "Sales Trend Over Time" renders below the KPIs, showing 12 monthly points with hover tooltips showing exact values. Stop the server once confirmed.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-3: render monthly sales trend chart"
```

---

### Task 8: Category and region calculations with tests

**Milestone:** TASK-4

**Files:**
- Modify: `calculations.py` (append)
- Modify: `tests/test_calculations.py` (append)

**Interfaces:**
- Consumes: nothing new
- Produces: `sales_by_category(df) -> pd.DataFrame` and `sales_by_region(df) -> pd.DataFrame`, each with columns matching the groupby key (`category` or `region`) and `sales`, sorted descending — consumed by Task 9's `render_category_chart` and `render_region_chart`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_calculations.py`:

```python
from calculations import sales_by_category, sales_by_region


def _sample_breakdown_df():
    return pd.DataFrame(
        {
            "category": ["Electronics", "Audio", "Electronics", "Wearables"],
            "region": ["North", "South", "North", "East"],
            "total_amount": [100.0, 50.0, 25.0, 75.0],
        }
    )


def test_sales_by_category():
    df = _sample_breakdown_df()
    result = sales_by_category(df)
    assert list(result["category"]) == ["Electronics", "Wearables", "Audio"]
    assert list(result["sales"]) == [125.0, 75.0, 50.0]


def test_sales_by_region():
    df = _sample_breakdown_df()
    result = sales_by_region(df)
    assert list(result["region"]) == ["North", "East", "South"]
    assert list(result["sales"]) == [125.0, 75.0, 50.0]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_calculations.py -v`
Expected: FAIL with `ImportError: cannot import name 'sales_by_category'`.

- [ ] **Step 3: Write the minimal implementation**

Append to `calculations.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_calculations.py -v`
Expected: 7 passed.

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-4: add sales_by_category and sales_by_region with tests"
```

---

### Task 9: Render category and region charts

**Milestone:** TASK-4 (completes this milestone's acceptance criteria)

**Files:**
- Modify: `app.py` (replace entire file)

**Interfaces:**
- Consumes: `sales_by_category(df)`, `sales_by_region(df)` from Task 8
- Produces: `render_category_chart(df) -> None`, `render_region_chart(df) -> None`, and the final `main()` shape used by Task 10's verification pass

- [ ] **Step 1: Replace `app.py`**

```python
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
    st.plotly_chart(fig, use_container_width=True)


def render_category_chart(df):
    st.subheader("Sales by Category")
    data = sales_by_category(df)
    fig = px.bar(data, x="category", y="sales")
    fig.update_layout(xaxis_title="Category", yaxis_title="Sales ($)")
    st.plotly_chart(fig, use_container_width=True)


def render_region_chart(df):
    st.subheader("Sales by Region")
    data = sales_by_region(df)
    fig = px.bar(data, x="region", y="sales")
    fig.update_layout(xaxis_title="Region", yaxis_title="Sales ($)")
    st.plotly_chart(fig, use_container_width=True)


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
```

- [ ] **Step 2: Verify manually**

Run: `streamlit run app.py`
Expected: two bar charts render side by side below the trend chart — "Sales by Category" (5 bars, Electronics tallest) on the left, "Sales by Region" (4 bars) on the right, both sorted highest to lowest with hover tooltips. Stop the server once confirmed.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-4: render category and region breakdown charts"
```

---

### Task 10: Full verification pass

**Milestone:** TASK-5 (test portion)

**Files:** none created or modified, unless a discrepancy is found (see Step 3)

**Interfaces:**
- Consumes: the complete `app.py` and `calculations.py` from Tasks 1-9
- Produces: nothing new — this task validates the existing surface

- [ ] **Step 1: Run the full test suite**

Run: `pytest tests/ -v`
Expected: 7 passed, 0 failed, no warnings.

- [ ] **Step 2: Run the app and compare against the PRD's expected output**

Run: `streamlit run app.py` and check in the browser:
- Total Sales ≈ $116,500
- Total Orders = 482
- Tallest category bar is Electronics
- Four regions shown: North, South, East, West
- No error banners or tracebacks in the browser or the terminal running Streamlit

Stop the server once confirmed.

- [ ] **Step 3: Fix any discrepancy found**

If any value in Step 2 doesn't match, the bug is in `calculations.py` (most likely the `groupby`/date-parsing logic). Add a regression test to `tests/test_calculations.py` that captures the exact discrepancy, fix the function in `calculations.py`, re-run Step 1 to confirm all tests pass, then commit:

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-5: fix <short description of the discrepancy>"
```

If Step 2 matched on the first try, no code changed and no commit is needed for this task — proceed to the handoff below.

---

## Handoff: Deployment (TASK-5)

**Do not execute this section.** Deployment is performed by the user, manually, after the feature branch is merged. No subagent or automated executor should attempt these steps.

Once Task 10 is complete and this plan's implementation tasks are merged into `main`:

1. Merge `feature/sales-dashboard` into `main` (e.g., via a reviewed pull request).
2. From `main`, go to Streamlit Community Cloud and deploy the app, pointing it at `app.py` in this repository.
3. Open the resulting public URL and confirm it shows the same KPIs and charts as the local run in Task 10.
4. Check off TASK-5 in `TASKS.md` and fill in its `Commit:` line once satisfied.
