# Sales Dashboard: Tasks

This file tracks all work for the e-commerce sales dashboard.
Each milestone moves through To Do -> In Progress -> Done.

## Definition of Done (must hold before any milestone moves to Done)
- Acceptance criteria met
- App runs locally with `streamlit run app.py`
- Changes committed with the milestone ID in the message

## To Do
- [ ] **TASK-5: Test and deploy** (test portion complete; deployment pending)
  - [ ] Dashboard runs without errors and is deployed to a public URL
  - Commit:

## In Progress

## Done
- [x] **TASK-1: Project setup and data loading**
  - [x] App runs with `streamlit run app.py` and shows a title
  - [x] Loads `data/sales-data.csv`; handles a missing file cleanly
  - Commit: ec30f0c a967431 c4b1f05
- [x] **TASK-2: KPI scorecards**
  - [x] Total Sales and Total Orders shown as formatted metrics
  - Commit: a758577 c787873
- [x] **TASK-3: Sales trend chart**
  - [x] Line chart of sales over time renders from the data
  - Commit: cfb3f31 cc2c687
- [x] **TASK-4: Category and region breakdowns**
  - [x] Bar charts for sales by category and by region, sorted by value
  - Commit: cf0e57c 98c239d
