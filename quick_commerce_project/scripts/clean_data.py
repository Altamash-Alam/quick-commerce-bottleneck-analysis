import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Raw files load kar rahe hain
orders = pd.read_csv("../data/orders.csv")
stores = pd.read_csv("../data/dark_stores.csv")
products = pd.read_csv("../data/products.csv")
items = pd.read_csv("../data/order_items.csv")

print("--- ORDERS RAW INFO ---")
print("Rows & Columns:", orders.shape)
print("\nMissing values in orders:\n", orders.isnull().sum())
print("\nDelivery mins summary:\n", orders["delivery_mins"].describe())
print("\nStatus counts:\n", orders["status"].value_counts())

# Ab cleaning shuru karte hain
clean_orders = orders.copy()

# 1. Agar order_value missing hai toh us order ke items ka sum nikal kar bhar denge
item_totals = items.groupby("order_id")["item_amount"].sum()
missing_val_mask = clean_orders["order_value"].isnull()
clean_orders.loc[missing_val_mask, "order_value"] = clean_orders.loc[
    missing_val_mask, "order_id"
].map(item_totals)

# Agar ab bhi koi order_value missing hai toh 0 kar dete hain
clean_orders["order_value"] = clean_orders["order_value"].fillna(0)

# 2. Missing customer_id ko 'UNKNOWN_CUST' mark kar dete hain (drop karne ke bajaye)
clean_orders["customer_id"] = clean_orders["customer_id"].fillna("UNKNOWN_CUST")

# 3. Glitch delivery times ko flag kar rahe hain (0 min ya > 60 min abnormal hai)
# Delivered orders mein 0 min aana matlab tracking glitch tha
clean_orders["is_glitch_delivery"] = np.where(
    (clean_orders["status"] == "Delivered")
    & ((clean_orders["delivery_mins"] <= 1) | (clean_orders["delivery_mins"] > 60)),
    1,
    0,
)

# 4. Date & Time features nikal rahe hain
clean_orders["order_dt"] = pd.to_datetime(clean_orders["order_time"])
clean_orders["order_hour"] = clean_orders["order_dt"].dt.hour
clean_orders["order_date"] = clean_orders["order_dt"].dt.date

# 15 minute SLA (Service Level Agreement) check
clean_orders["sla_breached"] = np.where(clean_orders["delivery_mins"] > 15, 1, 0)

# 5. Ek chhota sa Matplotlib chart banate hain taaki delivery time distribution dikhe
valid_del = clean_orders[
    (clean_orders["status"] == "Delivered")
    & (clean_orders["is_glitch_delivery"] == 0)
]["delivery_mins"]

plt.figure(figsize=(8, 4))
plt.hist(valid_del, bins=25, edgecolor="black")
plt.axvline(15, color="red", linestyle="--", label="15-Min SLA")
plt.title("Normal Delivered Orders - Delivery Time Distribution")
plt.xlabel("Delivery Minutes")
plt.ylabel("Number of Orders")
plt.legend()
plt.tight_layout()
plt.savefig("../dashboard/delivery_distribution.png")
plt.close()

# Cleaned file save kar rahe hain
clean_orders.to_csv("../data/clean_orders.csv", index=False)
print("\nSaved ../data/clean_orders.csv and ../dashboard/delivery_distribution.png")