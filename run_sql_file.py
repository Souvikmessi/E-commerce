
import sqlite3
import sys
import re

if len(sys.argv) < 2:
    print("Usage: python run_sql_file.py <sql-file> [max_rows_per_select]")
    sys.exit(1)

sql_file = sys.argv[1]
max_rows = int(sys.argv[2]) if len(sys.argv) > 2 else 50

with open(sql_file, "r", encoding="utf8") as f:
    sql_text = f.read()

# Remove SQL comments that start with -- (single-line)
sql_text = re.sub(r'--.*', '', sql_text)

# Split on semicolons but keep things robust for whitespace
# This is a simple split — it works for the typical SQL files you'll use here.
statements = [s.strip() for s in sql_text.split(';') if s.strip()]

conn = sqlite3.connect("ecom.db")
cur = conn.cursor()

select_counter = 0
other_counter = 0

for stmt in statements:
    # Lowercase first token to decide type
    first = stmt.lstrip().split(None, 1)[0].lower() if stmt else ''
    try:
        if first == 'select' or first.startswith('with'):  # treat WITH ... SELECT as SELECT
            select_counter += 1
            cur.execute(stmt)
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchmany(max_rows)
            print("\n--- SELECT result (#{}): ---".format(select_counter))
            if cols:
                print("\t".join(cols))
                for r in rows:
                    print("\t".join(str(x) if x is not None else 'NULL' for x in r))
                # if there are more rows, indicate so
                if len(rows) == max_rows:
                    print(f"... (showing first {max_rows} rows only)")
            else:
                print("No columns returned.")
        else:
            # Non-select statement (CREATE, DROP, INSERT, etc.)
            other_counter += 1
            cur.execute(stmt)
            conn.commit()
            print(f"[OK] Executed statement #{other_counter}: starts with '{first.upper()}'")
    except Exception as e:
        print(f"[ERROR] while executing statement starting with '{first}': {e}")

conn.close()
print(f"\nDone. Executed {other_counter} non-SELECT statements and displayed {select_counter} SELECT results.")
