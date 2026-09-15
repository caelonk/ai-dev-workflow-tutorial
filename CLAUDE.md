# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Streamlit e-commerce sales dashboard built from `prd/ecommerce-analytics.md`, as the hands-on project for the tutorial in `workshop-build-deploy.md`. Work is tracked in `TASKS.md` (milestones TASK-1 through TASK-5), and the design/implementation history lives in `docs/superpowers/specs/2026-09-14-sales-dashboard-design.md` and `docs/superpowers/plans/2026-09-14-sales-dashboard-plan.md`.

## Commands

```bash
# Activate the virtual environment first (every command below assumes this)
source venv/Scripts/activate      # Git Bash on Windows
# venv\Scripts\Activate.ps1       # PowerShell
# source venv/bin/activate        # macOS/Linux

pip install -r requirements.txt   # install dependencies

streamlit run app.py              # run the dashboard locally

pytest tests/ -v                  # run the full test suite
pytest tests/test_calculations.py::test_total_sales -v   # run a single test
```

`pyproject.toml` sets `pythonpath = ["."]` so bare `pytest` resolves `from calculations import ...` correctly — don't remove it.

## Architecture

Two-file split, enforced deliberately (see the design doc for the rationale):

- **`calculations.py`** — pure data functions only. No Streamlit import. Takes a DataFrame in, returns a DataFrame/scalar out, no side effects beyond `load_sales_data`'s one CSV read. This is what makes it testable with plain pytest.
- **`app.py`** — all Streamlit UI: page config, a `load_data()` wrapper (`@st.cache_data`) around `calculations.load_sales_data`, one `render_*(df)` function per dashboard section, and a `main()` that calls them in order. Each `render_*` function is self-contained and independently readable — that's the file's whole organizing idea.

Data flow: `data/sales-data.csv` → `load_sales_data` (parses `date`) → `load_data` (cached) → `main()` fans the same DataFrame out to `total_sales`/`total_orders` (KPIs), `monthly_sales_trend` (line chart), `sales_by_category`/`sales_by_region` (bar charts). Aggregation re-runs on every rerun; only the raw load is cached, since 482 rows makes the aggregations cheap.

Missing-CSV handling is intentionally minimal: `load_sales_data` lets `FileNotFoundError` propagate naturally, and `app.py`'s `main()` catches it once, shows `st.error(...)`, calls `st.stop()`. No other validation — malformed-but-present CSVs surface pandas' own errors rather than being caught and re-wrapped.

Tests (`tests/test_calculations.py`) use hand-crafted fixture DataFrames or a `tmp_path` CSV — never `data/sales-data.csv` — so expected values are verifiable by inspection and independent of the real dataset changing.

## Scope

This is Phase 1 only (see the PRD's Phase 2 list for what's explicitly excluded): no auth, no filtering/date-range, no DB integration, no export. Don't add these without checking the PRD first — it's a deliberate boundary, not an oversight.

## Lessons

- Bare `pytest` does not resolve `from calculations import ...` on its own — this repo has no `tests/__init__.py`, so pytest's default import mode inserts `tests/` onto `sys.path`, not the repo root. `pyproject.toml`'s `pythonpath = ["."]` fixes this; don't remove it, and don't reach for `PYTHONPATH=.` or `python -m pytest` workarounds instead.
- Streamlit's `use_container_width` parameter is deprecated (removal deadline already passed); use `width="stretch"` on `st.plotly_chart` calls instead. `requirements.txt` is unpinned, so a fresh install can resolve a Streamlit version that drops the old parameter entirely.
- No browser is available in this environment for manual UI verification. Use `streamlit.testing.v1.AppTest` (`AppTest.from_file("app.py")`, `at.run(timeout=30)`) to inspect rendered metrics, chart data, and exceptions in-process — it's the reliable substitute used throughout this project's build.
