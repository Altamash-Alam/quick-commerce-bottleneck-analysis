import pandas as pd

orders = pd.read_csv("../data/clean_orders.csv")
stores = pd.read_csv("../data/dark_stores.csv")

# Store-wise peak vs non-peak summary
orders["is_peak"] = orders["order_hour"].between(19, 22)

summary = []
for sid in stores["store_id"]:
  s_row = stores[stores["store_id"] == sid].iloc[0]
  sub = orders[orders["store_id"] == sid]
  peak = sub[sub["is_peak"]]

  total_ord = len(sub)
  cancelled_ord = (sub["status"] == "Cancelled").sum()
  peak_ord = len(peak)
  peak_cancel = (peak["status"] == "Cancelled").sum()
  avg_del = sub[
      (sub["status"] == "Delivered") & (sub["is_glitch_delivery"] == 0)
  ]["delivery_mins"].mean()

  summary.append({
      "store_id": sid,
      "city": s_row["city"],
      "pincode": s_row["pincode"],
      "current_riders": s_row["riders"],
      "total_orders_30d": total_ord,
      "cancelled_orders_30d": cancelled_ord,
      "peak_orders_30d": peak_ord,
      "peak_cancelled_30d": peak_cancel,
      "avg_delivery_mins": round(avg_del, 1),
  })

df_sum = pd.DataFrame(summary)
df_sum.to_csv("../data/store_summary_for_excel.csv", index=False)
print("Saved ../data/store_summary_for_excel.csv")