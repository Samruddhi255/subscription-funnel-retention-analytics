# Supply Chain Delivery & Cost Performance Analytics
**Operations analytics portfolio project | Python, SQL, Power BI-ready CSVs**

## Business problem
An online retailer needs to understand late deliveries, shipping cost, supplier service levels, and regional/category performance.

## Questions
- What is the on-time delivery rate?
- Which regions, categories, shipping modes, and suppliers have elevated delay rates?
- How do revenue and gross profit vary by region/category?
- Which suppliers fall below their on-time target?

## Run
```bash
python -m pip install -r requirements.txt
python src/analyze.py
```
Data is in `data/`; SQL examples in `sql/`; generated KPI tables and recommendations in `reports/`; chart previews in `images/`.

## KPI definitions
- On-time delivery rate = delivered orders delivered within promised days / delivered orders.
- Late rate = delivered orders exceeding promised days / delivered orders.
- Gross profit before shipping = revenue minus product cost; shipping cost is tracked separately.
- Supplier target gap = observed on-time rate minus target, in percentage points.

## Power BI dashboard
Import `orders.csv` and `suppliers.csv`, relate by `supplier_id`, and build pages for executive KPIs, delivery operations, supplier scorecards, and profitability. Add date, region, category, shipping mode, and supplier slicers. Chart previews are included; create the actual `.pbix` in Power BI Desktop.

## Data note
All records are **synthetic portfolio data**, not real supplier, retailer, or delivery records. Findings are descriptive and do not prove causation.
