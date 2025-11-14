# run_sql_file.py
import sqlite3
import sys

if len(sys.argv) < 2:
    print("Usage: python run_sql_file.py <sql-file> [limit]")
    sys.exit(1)

sql_file = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else None

with open(sql_file, "r", encoding="utf8") as f:
    sql = f.read()

conn = sqlite3.connect("ecom.db")
cur = conn.cursor()

try:
    cur.execute(sql)
    rows = cur.fetchmany(limit) if limit else cur.fetchall()
    cols = [d[0] for d in cur.description] if cur.description else []
    if cols:
        print("\t".join(cols))
        for r in rows:
            print("\t".join(str(x) for x in r))
    else:
        print("Query executed (no results to show).")
except Exception as e:
    print("Error running SQL:", e)
finally:
    conn.close()
