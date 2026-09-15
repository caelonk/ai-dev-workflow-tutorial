# Sales Dashboard Design

Design for the Phase 1 e-commerce sales dashboard described in `prd/ecommerce-analytics.md`. Milestones are tracked in `TASKS.md` (TASK-1 through TASK-5).

## Scope

Phase 1 only: KPI cards (Total Sales, Total Orders), a monthly sales trend line chart, and bar charts for sales by category and by region, all reading from the static `data/sales-data.csv`. No filtering, auth, database integration, or export — those are explicitly out of scope per the PRD's Phase 2 list.

## Ground rules

- Work on the current branch (`feature/sales-dashboard`); no git worktree.
- Plain `venv/` virtual environment with `requirements.txt` (no uv/conda).
- Data calculations live in their own module with pytest tests.
- Code stays simple and readable over clever or heavily abstracted.

## Architecture / file layout

```
ai-dev-workflow-tutorial/
├── app.py                  # Streamlit UI: page config + render functions + main()
├── calculations.py         # Pure data functions: load, aggregate
├── requirements.txt        # streamlit, pandas, plotly, pytest
├── venv/                   # local virtual environment (gitignored)
├── tests/
│   └── test_calculations.py
├── data/
│   └── sales-data.csv      # already present
└── TASKS.md
```

Flat layout: `app.py` and `calculations.py` sit at the repo root. `calculations.py` has no Streamlit imports, so it's testable with plain pytest independent of the UI.

## Components

**`calculations.py`** (pure functions, no Streamlit, no side effects beyond one CSV read):

- `load_sales_data(path)` — reads the CSV, parses `date` as datetime, returns a DataFrame. Raises `FileNotFoundError` naturally if the path doesn't exist; the caller decides how to present that.
- `total_sales(df)` — sum of `total_amount`.
- `total_orders(df)` — row count.
- `monthly_sales_trend(df)` — groups by month, returns (month, sales) sorted chronologically.
- `sales_by_category(df)` — groups by category, sums `total_amount`, sorted descending.
- `sales_by_region(df)` — groups by region, sums `total_amount`, sorted descending.

**`app.py`**:

- Page config (`st.set_page_config(layout="wide")`, title "ShopSmart Sales Dashboard").
- `load_data()` — `@st.cache_data`-wrapped call into `calculations.load_sales_data`, catching `FileNotFoundError` and showing an error message on failure.
- `render_kpis(df)`, `render_trend_chart(df)`, `render_category_chart(df)`, `render_region_chart(df)` — each builds one Plotly figure or metric row.
- `main()` — calls `load_data()` then the four render functions in order.

Each `calculations.py` function takes a DataFrame in and returns a DataFrame/scalar out, with no hidden state, so each is independently unit-testable.

## Data flow

```
data/sales-data.csv
      |
      v
load_sales_data()          (calculations.py -- parses dates, returns raw DataFrame)
      |
      v
load_data()                (app.py -- @st.cache_data wraps the call above; cached across reruns)
      |
      +--> total_sales(df) -----------+
      +--> total_orders(df) ----------+--> render_kpis()           -> st.metric x2
      +--> monthly_sales_trend(df) ---+--> render_trend_chart()    -> Plotly line chart
      +--> sales_by_category(df) -----+--> render_category_chart() -> Plotly bar chart
      +--> sales_by_region(df) -------+--> render_region_chart()   -> Plotly bar chart
```

The raw DataFrame is loaded once (cached). Aggregation functions re-run on each script rerun, which is cheap at 482 rows and requires no per-function caching. Phase 1 has no filter widgets, so in practice `main()` only re-executes on manual refresh or first load.

## Error handling

- `load_sales_data()` lets pandas raise its natural `FileNotFoundError` if the CSV is missing.
- `load_data()` in `app.py` catches that exception, shows `st.error("Could not find data/sales-data.csv — make sure the file exists before running the dashboard.")`, and calls `st.stop()` so the rest of the page doesn't render against missing data.
- No column/type validation beyond that. If the CSV exists but is malformed, pandas/Streamlit's own error surfaces naturally rather than being caught and re-wrapped. This keeps the code short; more defensive validation can be added later if needed, but isn't built in speculatively now.

## Testing

`tests/test_calculations.py`, using hand-crafted fixture DataFrames (~5-6 rows spanning 2 months, 2+ categories, 2+ regions, with amounts chosen so expected sums are easy to verify by hand):

- `test_total_sales` — sum matches expected.
- `test_total_orders` — count matches expected.
- `test_monthly_sales_trend` — correct grouping and chronological sort order.
- `test_sales_by_category` — correct grouping and descending sort order.
- `test_sales_by_region` — correct grouping and descending sort order.
- `test_load_sales_data_reads_csv` — writes a tiny CSV to `tmp_path`, confirms it loads with parsed dates.
- `test_load_sales_data_missing_file_raises` — confirms `FileNotFoundError` propagates for a nonexistent path.

No tests for `app.py` itself — Streamlit UI code is verified by hand via `streamlit run app.py`, per the Definition of Done in `TASKS.md`.

## Key decisions (from clarifying questions)

| Decision | Choice | Rationale |
|---|---|---|
| File structure | Flat (`app.py` + `calculations.py` at root) | Matches "simple and readable" ground rule; PRD is Phase-1-scoped |
| Caching | `@st.cache_data` on the load function | Avoids re-reading CSV on every Streamlit rerun; idiomatic |
| Trend granularity | Monthly | Daily would be noisy at ~1-2 orders/day; monthly better answers "is the business growing" |
| Missing-file handling | Simple: `st.error` + `st.stop()` | No auth/multi-user complexity in Phase 1; friendly message is enough |
| Test data | Hand-crafted fixtures | Fast, expected values obvious by inspection, independent of real CSV changing |
| App.py internal structure | Small render functions per section, one file | Readable top-to-bottom without splitting into more files |

## Out of scope (explicit)

Everything in the PRD's Phase 2 list: auth, real-time DB integration, export, email alerts, filtering/date range, drill-down, mobile-responsive design. Also out of scope for this design: automated UI tests for `app.py`, and deployment (handled manually by the user after merge, per the plan's final step).
