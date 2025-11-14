# ingest.py
import pandas as pd
import sqlite3

conn = sqlite3.connect("ecom.db")
cur = conn.cursor()

# Create typed tables
cur.executescript("""
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT,
  city TEXT,
  signup_channel TEXT,
  device_type TEXT,
  first_order_date TEXT,
  last_login TEXT
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  product_name TEXT,
  brand TEXT,
  category TEXT,
  price REAL,
  cost_price REAL,
  rating REAL,
  is_limited_edition INTEGER,
  sustainability_score REAL
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  user_id INTEGER,
  order_date TEXT,
  discount_code TEXT,
  discount_amount REAL,
  shipping_type TEXT,
  order_value REAL
);

DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
  order_item_id INTEGER PRIMARY KEY,
  order_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  unit_price REAL,
  is_returned INTEGER
);

DROP TABLE IF EXISTS payments;
CREATE TABLE payments (
  payment_id INTEGER PRIMARY KEY,
  order_id INTEGER,
  amount REAL,
  payment_method TEXT,
  status TEXT
);

DROP TABLE IF EXISTS events;
CREATE TABLE events (
  event_id INTEGER PRIMARY KEY,
  user_id INTEGER,
  event_type TEXT,
  event_time TEXT,
  page_url TEXT
);
""")

conn.commit()

# Load CSVs using pandas
files = {
    "users": "data/users.csv",
    "products": "data/products.csv",
    "orders": "data/orders.csv",
    "order_items": "data/order_items.csv",
    "payments": "data/payments.csv",
    "events": "data/events.csv"
}

for table, path in files.items():
    df = pd.read_csv(path)
    df.to_sql(table, conn, if_exists="replace", index=False)

conn.close()
print("Ingested CSVs to ecom.db")
