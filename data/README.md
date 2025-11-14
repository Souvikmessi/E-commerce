# E-commerce Synthetic Dataset + Analytics (Unique Variant)

This project generates synthetic e-commerce data, ingests it to SQLite, and runs analytics.

**Unique features**
- Behavioral user fields: `device_type`, `signup_channel`, `last_login`
- Product sustainability score & limited-edition flag
- Events file for funnel analysis (`events.csv`)
- RFM and cohort analytics included

## Files
- `generate_data.py` — generate CSVs (requires `faker`)
- `data/*.csv` — generated datasets
- `ingest.py` — create `ecom.db` and load CSVs
- `analytics.sql` — example advanced SQL queries (RFM, sustainability share, cohort)
- `query.sql` — lightweight single query for the assignment

## Quick run
1. Create `data/` folder.
2. `pip install pandas faker`
3. `python generate_data.py`
4. `python ingest.py`
5. Use `sqlite3 ecom.db` and run `.read analytics.sql` or open in DB browser.

## Why this is unique
Adds behavioral & sustainability dimensions + events funnel — helps show product thinking, domain knowledge, and SQL skills beyond a simple join.

