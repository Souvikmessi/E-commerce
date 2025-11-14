-- analytics.sql

-- 1) RFM-like summary per user (recency: days since last order, frequency: order count, monetary: sum payments)
WITH last_order AS (
  SELECT user_id, MAX(order_date) AS last_order_date
  FROM orders
  GROUP BY user_id
),
freq AS (
  SELECT user_id, COUNT(*) AS order_count
  FROM orders
  GROUP BY user_id
),
monetary AS (
  SELECT o.user_id, SUM(p.amount) AS total_spent
  FROM orders o
  JOIN payments p ON o.order_id = p.order_id
  WHERE p.status = 'paid'
  GROUP BY o.user_id
)
SELECT 
  u.user_id,
  u.name,
  u.email,
  julianday('now') - julianday(last_order.last_order_date) AS recency_days,
  freq.order_count,
  COALESCE(monetary.total_spent,0) AS total_spent
FROM users u
LEFT JOIN last_order ON u.user_id = last_order.user_id
LEFT JOIN freq ON u.user_id = freq.user_id
LEFT JOIN monetary ON u.user_id = monetary.user_id
ORDER BY total_spent DESC
LIMIT 20;

-- 2) Revenue share from high-sustainability products (sustainability_score >= 0.7)
SELECT 
  SUM(p.amount) AS total_paid,
  SUM(p.amount * (pr.sustainability_score >= 0.7)) AS high_sustainability_revenue,
  ROUND(100.0 * SUM(p.amount * (pr.sustainability_score >= 0.7)) / SUM(p.amount), 2) AS pct_high_sustainability
FROM payments p
JOIN orders o ON p.order_id = o.order_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products pr ON pr.product_id = oi.product_id
WHERE p.status = 'paid';

-- 3) Cohort: monthly new-user cohort and purchases in following months (simple)
WITH user_cohort AS (
  SELECT user_id, substr(first_order_date,1,7) AS cohort_month
  FROM users
  WHERE first_order_date IS NOT NULL
),
orders_month AS (
  SELECT user_id, substr(order_date,1,7) AS order_month, SUM(order_value - COALESCE(discount_amount,0)) AS revenue
  FROM orders
  GROUP BY user_id, order_month
)
SELECT c.cohort_month, o.order_month, COUNT(DISTINCT o.user_id) AS active_users, SUM(o.revenue) AS revenue
FROM user_cohort c
JOIN orders_month o ON c.user_id = o.user_id
GROUP BY c.cohort_month, o.order_month
ORDER BY c.cohort_month, o.order_month
LIMIT 50;
