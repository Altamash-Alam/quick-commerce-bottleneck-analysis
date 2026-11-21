import sqlite3
import pandas as pd

# Memory mein SQLite database banate hain aur CSVs load karte hain
conn = sqlite3.connect(":memory:")

pd.read_csv("../data/clean_orders.csv").to_sql("orders", conn, index=False, if_exists="replace")
pd.read_csv("../data/dark_stores.csv").to_sql("dark_stores", conn, index=False, if_exists="replace")
pd.read_csv("../data/products.csv").to_sql("products", conn, index=False, if_exists="replace")
pd.read_csv("../data/order_items.csv").to_sql("order_items", conn, index=False, if_exists="replace")

with open("../sql/business_analysis.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# Har query ko ';' se alag karke chalate hain
queries = [q.strip() for q in sql_script.split(";") if q.strip()]

for idx, q in enumerate(queries, start=1):
    print(f"\n==================== QUERY {idx} RESULT ====================")
    df_res = pd.read_sql_query(q, conn)
    print(df_res.to_string(index=False))

conn.close()