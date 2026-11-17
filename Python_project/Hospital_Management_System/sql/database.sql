-- ==========================================
-- HOSPITAL MANAGEMENT SYSTEM
-- DATABASE
-- ==========================================


-- Create Database
CREATE DATABASE IF NOT EXISTS hospital_management;

USE hospital_management;


-- ==========================================
-- USERS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS users (

    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) NOT NULL UNIQUE,

    password_hash VARCHAR(300) NOT NULL,

    full_name VARCHAR(100) NOT NULL,

    role VARCHAR(30) NOT NULL DEFAULT 'receptionist',

    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- ==========================================
-- CUSTOMERS / PATIENTS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS customers (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    phone VARCHAR(30),

    email VARCHAR(100),

    address VARCHAR(255),

    age INT,

    gender VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- ==========================================
-- SUPPLIERS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS suppliers (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    phone VARCHAR(30),

    email VARCHAR(100),

    address VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- ==========================================
-- PRODUCTS / MEDICINES TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS products (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    category VARCHAR(100),

    price DECIMAL(12,2) NOT NULL DEFAULT 0,

    quantity INT NOT NULL DEFAULT 0,

    supplier_id INT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (supplier_id)

        REFERENCES suppliers(id)

        ON DELETE SET NULL

        ON UPDATE CASCADE

);


-- ==========================================
-- SALES / BILLING TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS sales (

    id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NULL,

    total DECIMAL(12,2) NOT NULL DEFAULT 0,

    payment_method VARCHAR(30)
        NOT NULL DEFAULT 'Cash',

    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)

        REFERENCES customers(id)

        ON DELETE SET NULL

        ON UPDATE CASCADE

);


-- ==========================================
-- PURCHASES TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS purchases (

    id INT AUTO_INCREMENT PRIMARY KEY,

    supplier_id INT NULL,

    total DECIMAL(12,2) NOT NULL DEFAULT 0,

    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (supplier_id)

        REFERENCES suppliers(id)

        ON DELETE SET NULL

        ON UPDATE CASCADE

);


-- ==========================================
-- EMPLOYEES TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS employees (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    phone VARCHAR(30),

    email VARCHAR(100),

    department VARCHAR(100),

    salary DECIMAL(12,2) DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- ==========================================
-- DEFAULT SUPPLIER
-- ==========================================

INSERT INTO suppliers
(
    name,
    phone,
    email,
    address
)

SELECT
    'Default Medical Supplier',
    '0000000000',
    'supplier@example.com',
    'Hospital Area'

WHERE NOT EXISTS
(
    SELECT 1

    FROM suppliers

    WHERE name = 'Default Medical Supplier'
);


-- ==========================================
-- SALE ITEMS
-- ==========================================

CREATE TABLE IF NOT EXISTS sale_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,

    FOREIGN KEY (sale_id)
        REFERENCES sales(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


-- ==========================================
-- PURCHASE ITEMS
-- ==========================================

USE hospital_management;

CREATE TABLE IF NOT EXISTS purchase_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,

    FOREIGN KEY (purchase_id)
        REFERENCES purchases(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

USE hospital_management;

ALTER TABLE products
ADD COLUMN purchase_price DECIMAL(12,2) NOT NULL DEFAULT 0
AFTER price;

DESCRIBE products;


USE hospital_management;

ALTER TABLE products
ADD COLUMN expiry_date DATE NULL;


USE hospital_management;

SHOW COLUMNS FROM products;

show tables;
DESCRIBE sales;
DESCRIBE sale_items;


USE hospital_management;

ALTER TABLE products
ADD COLUMN is_active TINYINT(1) NOT NULL DEFAULT 1;

DESCRIBE products;
SHOW COLUMNS FROM products LIKE 'is_active';
