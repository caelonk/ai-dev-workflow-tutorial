# Sales Dashboard: Tasks

This file tracks all work for the e-commerce sales dashboard.
Each milestone moves through To Do -> In Progress -> Done.

**Live dashboard:** https://ai-dev-workflow-tutorial-v6fzstakicuhqnfk5zdwy3.streamlit.app/

## Definition of Done (must hold before any milestone moves to Done)
- Acceptance criteria met
- App runs locally with `streamlit run app.py`
- Changes committed with the milestone ID in the message

## To Do

## In Progress

## Done
- [x] **TASK-1: Project setup and data loading**
  - [x] App runs with `streamlit run app.py` and shows a title
  - [x] Loads `data/sales-data.csv`; handles a missing file cleanly
  - Commit: ec30f0c a967431 c4b1f05
  - Notes: no browser available, so the missing-file error path was verified with Streamlit's AppTest harness instead of by eye
- [x] **TASK-2: KPI scorecards**
  - [x] Total Sales and Total Orders shown as formatted metrics
  - Commit: a758577 c787873
  - Notes: first implementer stalled 10 min because bare `pytest` couldn't import `calculations`; worked around with `python -m pytest`, then fixed properly with a `pyproject.toml` pythonpath setting (0268bfe)
- [x] **TASK-3: Sales trend chart**
  - [x] Line chart of sales over time renders from the data
  - Commit: cfb3f31 cc2c687
  - Notes: the plan's chart code used the deprecated `use_container_width`, a deploy risk on unpinned Streamlit, replaced with `width="stretch"` (0268bfe); `/code-review` found a redundant sort after groupby, removed (28a57dd)
- [x] **TASK-4: Category and region breakdowns**
  - [x] Bar charts for sales by category and by region, sorted by value
  - Commit: cf0e57c 98c239d
  - Notes: first report only tested the calculation functions, not the rendered charts; review bounced it and the charts were re-verified with AppTest. Category/region near-duplication left as-is (YAGNI)
- [x] **TASK-5: Test and deploy**
  - [x] Dashboard runs without errors and is deployed to a public URL: https://ai-dev-workflow-tutorial-v6fzstakicuhqnfk5zdwy3.streamlit.app/
  - Commit: 291692e (merge deployed from main)
  - Notes: TASKS.md wasn't updated during the build; the final review caught it and it was synced (0268bfe). `/code-review` flagged that groupby drops rows with blank category/region/date, left as-is since the data has no nulls and validation is out of Phase 1 scope
