-- query.sql
-- Total spent per user (only paid) + number of distinct brands they bought from
SELECT u.user_id, u.name, u.email,
       COUNT(DISTINCT pr.brand) AS distinct_brands,
       SUM(p.amount) AS total_spent
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN payments p ON o.order_id = p.order_id AND p.status = 'paid'
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products pr ON oi.product_id = pr.product_id
GROUP BY u.user_id
ORDER BY total_spent DESC
LIMIT 50;
