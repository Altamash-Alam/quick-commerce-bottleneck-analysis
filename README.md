# Quick-Commerce Dark-Store & Delivery Bottleneck Analysis

## What This Project Is About
I built a 25,000-order quick-commerce dataset across 5 dark stores (`DS01`–`DS05`) to find why evening deliveries run slow, why orders get cancelled during peak hours, and where stockouts hurt revenue.

## Tools Used
- **Python (Pandas, NumPy, Matplotlib):** Raw data generation, missing value / glitch handling, hourly & store analysis, and charts.
- **SQL (SQLite):** Peak-hour store cancellation & delay checks, category stockout loss, and window-function hour ranking.
- **Excel:** What-if rider hiring cost vs. recovered peak orders & revenue model (`excel/rider_roi_model.xlsx`).
- **Power BI:** Interactive dashboard (`dashboard/quick_commerce_dashboard.pbix`) showing hourly delivery spikes and store-wise cancellation rates.

## Key Findings
- **Evening peak bottleneck:** Overall average delivery looks fine (~14–15 mins across stores), but between **19:00 and 22:00** average delivery jumps to **~21 mins**.
- **Low-rider stores struggle most:** `DS05` (9 riders) and `DS02` (10 riders) see high peak cancellation rates (~47.3% and ~43.1%) and ~24.7–24.9 min peak averages, compared to `DS01` (18 riders) at ~2.4% peak cancellation.
- **Category stockouts:** `Dairy` had the highest estimated stockout loss in my sample run, followed by `Home` and `Bakery`.
- **Rider cost reality check:** Adding 9 riders at ₹18,000/month costs ₹1,62,000/month, which can be larger than recovered order revenue if cancel reduction stays modest—so hiring should be tested carefully alongside stockout and peak routing fixes.

## Challenges I Ran Into
- `order_hour` was initially treated as a numeric summary in Power BI, so I switched its summarization to **Don't summarize** to plot hours `0` to `23` properly.
- Some orders had missing `order_value` or `customer_id`, and a few delivered rows had `0` or extreme minutes (`is_glitch_delivery`), so I flagged glitches instead of blindly averaging everything.
