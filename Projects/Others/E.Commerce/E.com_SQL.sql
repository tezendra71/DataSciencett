-- Active: 1756819717541@@127.0.0.1@5432@ecommerce_db@public
-- Before creating tables, Database and selecting it was done through interface.

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    gender VARCHAR(10),
    age INTEGER,
    city VARCHAR(50),
    registration_date DATE
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    cost_price DECIMAL(10,2),
    selling_price DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    payment_method VARCHAR(20),
    order_status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    discount DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE returns (
    return_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    return_reason VARCHAR(50),
    return_date DATE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- To load the data file were converted to csv and imported through pgadmin feature.

Select * From customers;
Select * From order_items;
Select * From orders;
Select * From products;
Select * From returns ;

-- Total revenue and total orders
SELECT 
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(oi.quantity * p.selling_price - oi.discount) as total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'Delivered';

-- Revenue by product category
SELECT 
    p.category,
    SUM(oi.quantity * p.selling_price - oi.discount) as revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY p.category
ORDER BY revenue DESC;

--  Top 5 customers by spending
SELECT 
    c.customer_name,
    SUM(oi.quantity * p.selling_price - oi.discount) as total_spent,
    COUNT(DISTINCT o.order_id) as orders_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_name
ORDER BY total_spent DESC
LIMIT 5;

--  Monthly sales trend
SELECT 
    TO_CHAR(o.order_date, 'YYYY-MM') as month,
    SUM(oi.quantity * p.selling_price - oi.discount) as revenue,
    COUNT(DISTINCT o.order_id) as orders_count
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'Delivered'
GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')
ORDER BY month;

--  Return rate by category
SELECT 
    p.category,
    COUNT(DISTINCT o.order_id) as total_orders,
    COUNT(DISTINCT r.order_id) as returned_orders,
    ROUND(COUNT(DISTINCT r.order_id) * 100.0 / COUNT(DISTINCT o.order_id), 1) as return_rate
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN returns r ON o.order_id = r.order_id
WHERE o.order_status = 'Delivered'
GROUP BY p.category
ORDER BY return_rate DESC;


