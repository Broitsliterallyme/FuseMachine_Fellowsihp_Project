-- 1
SELECT * 
FROM customers
WHERE creditLimit > 20000;

-- 2
SELECT * 
FROM employees
WHERE reportsTo = (
    SELECT employeeNumber 
    FROM employees 
    WHERE jobTitle = 'VP Sales'
);

-- 3
SELECT * 
FROM customers
WHERE country = 'USA'
AND state IS NOT NULL
AND creditLimit BETWEEN 100000 AND 200000;

-- 4
SELECT * 
FROM employees
WHERE reportsTo IN (
    SELECT employeeNumber 
    FROM employees 
    WHERE jobTitle LIKE '%Sales Manager%'
);

-- 5
SELECT country, AVG(creditLimit) AS avg_credit
FROM customers
GROUP BY country;

-- 6
SELECT orderDate, customerNumber, COUNT(*) AS total_orders
FROM orders
GROUP BY orderDate, customerNumber
HAVING COUNT(*) > 10;

-- 7
SELECT 
    firstName, lastName, jobTitle,
    (SELECT COUNT(*) 
     FROM employees e2 
     WHERE e2.reportsTo = e1.employeeNumber) AS total_supervisee
FROM employees e1;

-- 8
SELECT 
    e1.firstName, e1.lastName, e1.jobTitle,
    COUNT(e2.employeeNumber) AS total_supervisee
FROM employees e1
LEFT JOIN employees e2 
ON e1.employeeNumber = e2.reportsTo
GROUP BY e1.employeeNumber;

-- 9
WITH avg_cte AS (
    SELECT AVG(creditLimit) AS avg_credit FROM customers
)
SELECT * 
FROM customers, avg_cte
WHERE customers.creditLimit > avg_cte.avg_credit;

-- 10
SELECT customerName, creditLimit,
RANK() OVER (ORDER BY creditLimit DESC) AS rnk
FROM customers;

SELECT * FROM (
    SELECT customerName, creditLimit,
    RANK() OVER (ORDER BY creditLimit DESC) AS rnk
    FROM customers
) t
WHERE rnk = 3;

-- 11
SELECT officeCode, COUNT(*) AS total_employees
FROM employees
GROUP BY officeCode;

-- 12
SELECT salesRepEmployeeNumber, COUNT(*) AS total_customers
FROM customers
GROUP BY salesRepEmployeeNumber;

-- 13
SELECT o.city, o.state, o.country, SUM(p.amount) AS total_payment
FROM payments p
JOIN customers c ON p.customerNumber = c.customerNumber
JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber
JOIN offices o ON e.officeCode = o.officeCode
GROUP BY o.officeCode;

-- 14
SELECT o.officeCode, SUM(od.quantityOrdered * od.priceEach) AS total_sales
FROM orderdetails od
JOIN orders o2 ON od.orderNumber = o2.orderNumber
JOIN customers c ON o2.customerNumber = c.customerNumber
JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber
JOIN offices o ON e.officeCode = o.officeCode
GROUP BY o.officeCode;

-- 15
SELECT o.officeCode, 
SUM(od.quantityOrdered * od.priceEach) - IFNULL(SUM(p.amount),0) AS pending
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o2 ON c.customerNumber = o2.customerNumber
JOIN orderdetails od ON o2.orderNumber = od.orderNumber
LEFT JOIN payments p ON c.customerNumber = p.customerNumber
GROUP BY o.officeCode;

-- 16
SELECT 
    customerName,
    country,
    creditLimit,
    creditLimit / SUM(creditLimit) OVER (PARTITION BY country) AS proportion
FROM customers;

-- 17
CREATE VIEW customer_order_summary AS
SELECT 
    c.customerName,
    CONCAT(c.addressLine1, ', ', c.city, ', ', c.country) AS address,
    COUNT(o.orderNumber) AS total_orders
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
GROUP BY c.customerNumber;

-- 18
UPDATE customers
SET country = 'Nepal'
WHERE customerNumber = 103;

-- 19
DELETE FROM payments
WHERE amount < 20000;

-- 20
INSERT INTO payments (customerNumber, checkNumber, paymentDate, amount)
VALUES (103, 'CHK999', '2026-05-04', 50000);