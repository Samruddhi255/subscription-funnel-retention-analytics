-- Import orders.csv and suppliers.csv as tables named orders and suppliers.
SELECT COUNT(*) total_orders,
 ROUND(100.0*SUM(CASE WHEN order_status='Delivered' AND actual_delivery_days<=promised_delivery_days THEN 1 ELSE 0 END)/NULLIF(SUM(CASE WHEN order_status='Delivered' THEN 1 ELSE 0 END),0),2) on_time_delivery_rate_pct,
 ROUND(SUM(revenue_inr),2) revenue_inr,
 ROUND(SUM(gross_profit_before_shipping_inr),2) gross_profit_before_shipping_inr
FROM orders;

SELECT region,COUNT(*) orders,SUM(late_delivery) late_orders,
 ROUND(100.0*SUM(late_delivery)/COUNT(*),2) late_rate_pct
FROM orders WHERE order_status='Delivered'
GROUP BY region ORDER BY late_rate_pct DESC;

SELECT shipping_mode,COUNT(*) orders,ROUND(AVG(shipping_cost_inr),2) avg_shipping_cost,
 ROUND(100.0*AVG(late_delivery),2) late_rate_pct
FROM orders GROUP BY shipping_mode;

WITH k AS (
 SELECT supplier_id,COUNT(*) orders,
 ROUND(100.0*AVG(CASE WHEN late_delivery=0 THEN 1.0 ELSE 0.0 END),2) on_time_rate_pct
 FROM orders WHERE order_status='Delivered' GROUP BY supplier_id
)
SELECT k.supplier_id,s.supplier_tier,s.on_time_target_pct,k.orders,k.on_time_rate_pct,
 ROUND(k.on_time_rate_pct-s.on_time_target_pct,2) target_gap_pp
FROM k JOIN suppliers s ON s.supplier_id=k.supplier_id ORDER BY target_gap_pp;

SELECT strftime('%Y-%m',order_date) order_month,COUNT(*) orders,
 ROUND(SUM(revenue_inr),2) revenue_inr,ROUND(100.0*AVG(late_delivery),2) late_rate_pct
FROM orders GROUP BY strftime('%Y-%m',order_date) ORDER BY order_month;
