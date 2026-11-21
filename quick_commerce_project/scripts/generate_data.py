import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Seed fix kar rahe hain taaki har baar same pattern aaye
random.seed(42)
np.random.seed(42)

# 1. Dark stores banate hain
stores_data = [
    {"store_id": "DS01", "city": "Delhi", "pincode": "110001", "riders": 18},
    {"store_id": "DS02", "city": "Delhi", "pincode": "110024", "riders": 10},
    {"store_id": "DS03", "city": "Gurugram", "pincode": "122002", "riders": 16},
    {"store_id": "DS04", "city": "Noida", "pincode": "201301", "riders": 14},
    {"store_id": "DS05", "city": "Delhi", "pincode": "110085", "riders": 9},
]
stores_df = pd.DataFrame(stores_data)
stores_df.to_csv("../data/dark_stores.csv", index=False)

# 2. Products banate hain
products_data = [
    {"product_id": "P101", "name": "Full Cream Milk 1L", "category": "Dairy", "price": 66, "margin_pct": 12},
    {"product_id": "P102", "name": "Brown Bread", "category": "Bakery", "price": 45, "margin_pct": 22},
    {"product_id": "P103", "name": "Potato 1kg", "category": "Fresh", "price": 32, "margin_pct": 18},
    {"product_id": "P104", "name": "Salted Chips", "category": "Snacks", "price": 20, "margin_pct": 28},
    {"product_id": "P105", "name": "Greek Yogurt", "category": "Dairy", "price": 85, "margin_pct": 25},
    {"product_id": "P106", "name": "Dishwash Gel", "category": "Home", "price": 110, "margin_pct": 30},
]
products_df = pd.DataFrame(products_data)
products_df.to_csv("../data/products.csv", index=False)

# 3. 25,000 orders banate hain (shuruat ke liye kaafi hai, heavy bhi nahi hoga)
start_date = datetime(2026, 10, 1, 8, 0, 0)
orders = []
order_items = []

store_ids = stores_df["store_id"].tolist()
prod_ids = products_df["product_id"].tolist()
price_map = dict(zip(products_df["product_id"], products_df["price"]))

for i in range(1, 25001):
    order_id = f"ORD{100000 + i}"
    cust_id = f"CUST{random.randint(1, 4500)}"
    store_id = random.choice(store_ids)

    # Random timestamp pichle 30 din mein
    rand_mins = random.randint(0, 30 * 24 * 60)
    order_time = start_date + timedelta(minutes=rand_mins)
    hour = order_time.hour

    # Base delivery time
    base_time = random.normalvariate(13, 3)

    # Evening rush aur kam riders wale stores mein delay badhana
    if 19 <= hour <= 22:
        base_time += random.uniform(4, 9)
    if store_id in ["DS02", "DS05"] and 18 <= hour <= 22:
        base_time += random.uniform(5, 11)

    delivery_mins = round(max(4, base_time), 1)

    # Thoda messy / glitch data daal rahe hain
    r_glitch = random.random()
    if r_glitch < 0.015:
        delivery_mins = 0.0  # app/GPS glitch
    elif r_glitch < 0.025:
        delivery_mins = round(random.uniform(75, 130), 1)  # extreme delay

    # Status decide karna
    if delivery_mins > 28 or (store_id == "DS05" and random.random() < 0.08):
        status = "Cancelled"
        delivered_at = None
    else:
        status = "Delivered"
        delivered_at = order_time + timedelta(minutes=delivery_mins)

    # Items banana is order ke liye
    num_items = random.randint(1, 5)
    chosen_prods = random.sample(prod_ids, num_items)
    total_val = 0

    for pid in chosen_prods:
        qty = random.randint(1, 3)
        stockout = 1 if (status == "Cancelled" and random.random() < 0.35) else 0
        line_total = 0 if stockout == 1 else (price_map[pid] * qty)
        total_val += line_total

        order_items.append({
            "order_id": order_id,
            "product_id": pid,
            "quantity": qty,
            "is_stockout": stockout,
            "item_amount": line_total
        })

    # Kuch missing values jaan-boojh kar
    if random.random() < 0.01:
        cust_id = None
    if random.random() < 0.008:
        total_val = None

    orders.append({
        "order_id": order_id,
        "customer_id": cust_id,
        "store_id": store_id,
        "order_time": order_time,
        "delivered_at": delivered_at,
        "delivery_mins": delivery_mins,
        "status": status,
        "order_value": total_val
    })

pd.DataFrame(orders).to_csv("../data/orders.csv", index=False)
pd.DataFrame(order_items).to_csv("../data/order_items.csv", index=False)

print("Done! Files saved in data/ folder.")