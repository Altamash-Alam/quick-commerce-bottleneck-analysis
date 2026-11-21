-- Query 1: Peak hours (19:00 - 22:00) mein har store ka performance aur cancellation rate
SELECT
    o.store_id,
    s.city,
    s.pincode,
    s.riders,
    COUNT(*) AS peak_total_orders,
    SUM(CASE WHEN o.status = 'Cancelled' THEN 1 ELSE 0 END) AS peak_cancelled,
    ROUND(100.0 * SUM(CASE WHEN o.status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 1) AS peak_cancel_pct,
    ROUND(AVG(CASE WHEN o.status = 'Delivered' AND o.is_glitch_delivery = 0 THEN o.delivery_mins END), 1) AS peak_avg_mins
FROM orders o
JOIN dark_stores s ON o.store_id = s.store_id
WHERE o.order_hour BETWEEN 19 AND 22
GROUP BY o.store_id, s.city, s.pincode, s.riders
ORDER BY peak_avg_mins DESC;

-- Query 2: Kis product category mein stockout ki wajah se kitna order value loss hua
SELECT
    p.category,
    COUNT(*) AS total_item_lines,
    SUM(oi.is_stockout) AS stockout_count,
    ROUND(100.0 * SUM(oi.is_stockout) / COUNT(*), 2) AS stockout_rate_pct,
    SUM(CASE WHEN oi.is_stockout = 1 THEN oi.quantity * p.price ELSE 0 END) AS estimated_stockout_loss
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY estimated_stockout_loss DESC;

-- Query 3: Har store ke andar peak-hour delivery time ki ranking (Window Function)
SELECT
    store_id,
    order_hour,
    ROUND(AVG(delivery_mins), 1) AS avg_mins,
    RANK() OVER (PARTITION BY store_id ORDER BY AVG(delivery_mins) DESC) AS delay_rank_in_store
FROM orders
WHERE status = 'Delivered' AND is_glitch_delivery = 0
GROUP BY store_id, order_hour
HAVING COUNT(*) >= 10
ORDER BY store_id, delay_rank_in_store
LIMIT 15;