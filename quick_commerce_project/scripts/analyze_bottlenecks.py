import matplotlib.pyplot as plt
import pandas as pd

# Cleaned orders aur stores load karte hain
orders = pd.read_csv("../data/clean_orders.csv")
stores = pd.read_csv("../data/dark_stores.csv")

# Glitch deliveries ko exclude karke normal delivered orders lete hain
normal_del = orders[
    (orders["status"] == "Delivered") & (orders["is_glitch_delivery"] == 0)
].copy()

# Store-wise summary banate hain
store_summary = (
    normal_del.groupby("store_id")
    .agg(
        delivered_orders=("order_id", "count"),
        avg_delivery_mins=("delivery_mins", "mean"),
        sla_breach_pct=("sla_breached", lambda x: round(x.mean() * 100, 1)),
    )
    .reset_index()
)

# Cancellation rate bhi nikalte hain (total orders ke hisab se)
cancel_rate = (
    orders.groupby("store_id")["status"]
    .apply(lambda x: round((x == "Cancelled").mean() * 100, 1))
    .reset_index(name="cancel_rate_pct")
)

store_report = store_summary.merge(cancel_rate, on="store_id").merge(
    stores, on="store_id"
)
store_report = store_report.sort_values("avg_delivery_mins", ascending=False)

print("--- STORE PERFORMANCE REPORT ---")
print(store_report.to_string(index=False))

# Hourly trend nikalte hain
hourly = (
    normal_del.groupby("order_hour")
    .agg(
        orders_cnt=("order_id", "count"),
        avg_mins=("delivery_mins", "mean"),
    )
    .reset_index()
)

# 2 charts side-by-side banate hain
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

# Chart 1: Store-wise Avg Delivery Time
ax1.bar(
    store_report["store_id"],
    store_report["avg_delivery_mins"],
    color="steelblue",
    edgecolor="black",
)
ax1.axhline(15, color="red", linestyle="--", label="15-Min SLA")
ax1.set_title("Avg Delivery Time by Store")
ax1.set_xlabel("Store ID")
ax1.set_ylabel("Avg Minutes")
ax1.legend()

# Chart 2: Hour-wise Avg Delivery Time
ax2.plot(hourly["order_hour"], hourly["avg_mins"], marker="o", color="darkorange")
ax2.axhline(15, color="red", linestyle="--", label="15-Min SLA")
ax2.set_title("Avg Delivery Time by Hour of Day")
ax2.set_xlabel("Hour (0 - 23)")
ax2.set_ylabel("Avg Minutes")
ax2.set_xticks(range(0, 24, 2))
ax2.legend()

plt.tight_layout()
plt.savefig("../dashboard/store_and_hourly_bottlenecks.png")
plt.close()

print("\nSaved ../dashboard/store_and_hourly_bottlenecks.png")