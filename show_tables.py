# show_tables.py
import sqlite3
conn = sqlite3.connect("ecom.db")
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cur.fetchall()
print("Tables in ecom.db:")
for t in tables:
    print(" -", t[0])
conn.close()
