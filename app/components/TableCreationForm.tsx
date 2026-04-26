'use client';

import { useState } from 'react';
import { DatabaseConnection } from '@/app/types';
import { useToast } from './ToastContext';
import { createTable } from '@/app/lib/api';

interface TableCreationFormProps {
  connection: DatabaseConnection | null;
  onTableCreated?: () => void;
}

// 10 diverse SQL templates for each database type
const TABLE_TEMPLATES = {
  postgresql: [
    {
      name: 'users',
      title: '👤 Users (4 cols)',
      sql: `CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email) VALUES
  ('john_doe', 'john@example.com'),
  ('jane_smith', 'jane@example.com'),
  ('alex_wilson', 'alex@example.com');`,
    },
    {
      name: 'products',
      title: '🛍️ Products (6 cols)',
      sql: `CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL,
  stock INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO products (name, description, price, stock) VALUES
  ('Laptop Pro', 'High-performance laptop', 1299.99, 45),
  ('Wireless Mouse', 'Ergonomic wireless mouse', 29.99, 150),
  ('USB-C Cable', '6ft charging cable', 12.99, 500);`,
    },
    {
      name: 'orders',
      title: '📦 Orders (5 cols)',
      sql: `CREATE TABLE IF NOT EXISTS orders (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total_amount DECIMAL(10, 2) NOT NULL,
  status VARCHAR(50) DEFAULT 'pending'
);

INSERT INTO orders (user_id, order_date, total_amount, status) VALUES
  (1, CURRENT_TIMESTAMP, 1329.97, 'completed'),
  (2, CURRENT_TIMESTAMP, 89.98, 'pending'),
  (1, CURRENT_TIMESTAMP, 299.99, 'shipped');`,
    },
    {
      name: 'employees',
      title: '👔 Employees (10 cols)',
      sql: `CREATE TABLE IF NOT EXISTS employees (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE,
  salary DECIMAL(10, 2),
  department VARCHAR(100),
  job_title VARCHAR(100),
  hire_date DATE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO employees (first_name, last_name, email, salary, department, job_title, hire_date, is_active) VALUES
  ('John', 'Smith', 'john.smith@company.com', 75000.00, 'Engineering', 'Software Engineer', '2024-01-10', TRUE),
  ('Sarah', 'Johnson', 'sarah.johnson@company.com', 85000.00, 'Management', 'Team Lead', '2023-08-15', TRUE),
  ('Mike', 'Davis', 'mike.davis@company.com', 65000.00, 'Support', 'Support Specialist', '2024-03-01', TRUE),
  ('Lisa', 'Anderson', 'lisa.anderson@company.com', 95000.00, 'Engineering', 'Architect', '2022-11-20', TRUE),
  ('Tom', 'Brown', 'tom.brown@company.com', 72000.00, 'Sales', 'Account Executive', '2025-02-12', FALSE);`,
    },
    {
      name: 'transactions',
      title: '💰 Transactions (9 cols)',
      sql: `CREATE TABLE IF NOT EXISTS transactions (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  transaction_type VARCHAR(50),
  payment_method VARCHAR(50),
  status VARCHAR(50) DEFAULT 'completed',
  reference_code VARCHAR(100),
  description TEXT,
  transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO transactions (user_id, amount, transaction_type, payment_method, status, reference_code, description, transaction_date) VALUES
  (1, 500.00, 'credit', 'bank_transfer', 'completed', 'TXN-1001', 'Account deposit', CURRENT_TIMESTAMP),
  (2, 150.00, 'debit', 'card', 'completed', 'TXN-1002', 'Purchase order #123', CURRENT_TIMESTAMP),
  (1, 1000.00, 'transfer', 'wire', 'pending', 'TXN-1003', 'Wire transfer', CURRENT_TIMESTAMP),
  (3, 49.99, 'subscription', 'card', 'completed', 'TXN-1004', 'Monthly plan', CURRENT_TIMESTAMP),
  (2, 200.00, 'refund', 'wallet', 'completed', 'TXN-1005', 'Refund issued', CURRENT_TIMESTAMP);`,
    },
    {
      name: 'categories',
      title: '📂 Categories (5 cols)',
      sql: `CREATE TABLE IF NOT EXISTS categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  parent_category VARCHAR(100),
  is_featured BOOLEAN DEFAULT FALSE
);

INSERT INTO categories (name, description, parent_category, is_featured) VALUES
  ('Electronics', 'Electronic devices and gadgets', NULL, TRUE),
  ('Computers', 'Laptops and desktop systems', 'Electronics', TRUE),
  ('Accessories', 'Cables, adapters, and peripherals', 'Electronics', FALSE),
  ('Books', 'Physical and digital books', NULL, FALSE),
  ('Home & Garden', 'Home improvement and garden supplies', NULL, FALSE);`,
    },
    {
      name: 'customers',
      title: '🏪 Customers (8 cols)',
      sql: `CREATE TABLE IF NOT EXISTS customers (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  phone VARCHAR(20),
  address TEXT,
  city VARCHAR(100),
  loyalty_points INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO customers (first_name, last_name, phone, address, city, loyalty_points) VALUES
  ('Robert', 'Wilson', '+1-555-0101', '123 Main St, NYC, NY 10001', 'New York', 120),
  ('Emily', 'Martinez', '+1-555-0102', '456 Oak Ave, LA, CA 90001', 'Los Angeles', 80),
  ('James', 'Taylor', '+1-555-0103', '789 Pine Rd, Chicago, IL 60601', 'Chicago', 45),
  ('Victoria', 'Garcia', '+1-555-0104', '321 Elm St, Houston, TX 77001', 'Houston', 210),
  ('Daniel', 'Lopez', '+1-555-0105', '654 Cedar Ln, Phoenix, AZ 85001', 'Phoenix', 60);`,
    },
    {
      name: 'inventory',
      title: '📊 Inventory (10 cols)',
      sql: `CREATE TABLE IF NOT EXISTS inventory (
  id SERIAL PRIMARY KEY,
  product_id INT NOT NULL,
  warehouse_id INT,
  location_code VARCHAR(50),
  quantity INT DEFAULT 0,
  reorder_level INT,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_audit_date DATE,
  supplier_id INT,
  cost DECIMAL(10, 2)
);

INSERT INTO inventory (product_id, warehouse_id, location_code, quantity, reorder_level, last_updated, last_audit_date, supplier_id, cost) VALUES
  (1, 1, 'A-01-01', 100, 20, CURRENT_TIMESTAMP, '2026-04-01', 5, 899.99),
  (2, 2, 'B-02-04', 45, 10, CURRENT_TIMESTAMP, '2026-04-03', 3, 199.99),
  (3, 1, 'A-03-02', 200, 50, CURRENT_TIMESTAMP, '2026-04-05', 7, 20.00),
  (4, 3, 'C-01-05', 75, 15, CURRENT_TIMESTAMP, '2026-04-06', 2, 499.99),
  (5, 2, 'B-04-01', 30, 8, CURRENT_TIMESTAMP, '2026-04-07', 4, 129.50);`,
    },
    {
      name: 'reviews',
      title: '⭐ Reviews (7 cols)',
      sql: `CREATE TABLE IF NOT EXISTS reviews (
  id SERIAL PRIMARY KEY,
  product_id INT NOT NULL,
  user_id INT NOT NULL,
  rating INT CHECK (rating >= 1 AND rating <= 5),
  title VARCHAR(255),
  comment TEXT,
  verified_purchase BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO reviews (product_id, user_id, rating, title, comment, verified_purchase) VALUES
  (1, 1, 5, 'Excellent product', 'Excellent quality and fast shipping!', TRUE),
  (2, 2, 4, 'Great value', 'Good product with great value', TRUE),
  (3, 1, 5, 'Highly recommended', 'Exceeded expectations.', TRUE),
  (1, 3, 3, 'Decent', 'Works as expected but packaging was damaged.', FALSE),
  (2, 4, 4, 'Solid purchase', 'Reliable and easy to use.', TRUE);`,
    },
    {
      name: 'analytics',
      title: '📈 Analytics (12 cols)',
      sql: `CREATE TABLE IF NOT EXISTS analytics (
  id SERIAL PRIMARY KEY,
  date DATE NOT NULL,
  user_count INT,
  new_users INT,
  sessions INT,
  page_views INT,
  bounce_rate DECIMAL(5, 2),
  avg_session_duration INT,
  conversion_rate DECIMAL(5, 2),
  revenue DECIMAL(10, 2),
  traffic_source VARCHAR(100),
  top_page VARCHAR(255),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO analytics (date, user_count, new_users, sessions, page_views, bounce_rate, avg_session_duration, conversion_rate, revenue, traffic_source, top_page) VALUES
  ('2026-04-10', 1250, 220, 3450, 12300, 32.5, 145, 2.8, 8750.50, 'organic', '/products'),
  ('2026-04-11', 1340, 245, 3680, 13200, 30.2, 152, 3.1, 9250.75, 'paid_search', '/checkout'),
  ('2026-04-12', 1450, 280, 4120, 14500, 28.1, 168, 3.5, 10300.25, 'organic', '/products'),
  ('2026-04-13', 1380, 210, 3950, 13800, 31.3, 158, 3.2, 9800.00, 'email', '/sale'),
  ('2026-04-14', 1520, 300, 4300, 15100, 27.9, 172, 3.7, 11120.00, 'referral', '/pricing');`,
    },
  ],
  mysql: [
    {
      name: 'users',
      title: '👤 Users (4 cols)',
      sql: `CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email) VALUES
  ('john_doe', 'john@example.com'),
  ('jane_smith', 'jane@example.com'),
  ('alex_wilson', 'alex@example.com');`,
    },
    {
      name: 'products',
      title: '🛍️ Products (6 cols)',
      sql: `CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description LONGTEXT,
  price DECIMAL(10, 2) NOT NULL,
  stock INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO products (name, description, price, stock) VALUES
  ('Laptop Pro', 'High-performance laptop', 1299.99, 45),
  ('Wireless Mouse', 'Ergonomic wireless mouse', 29.99, 150),
  ('USB-C Cable', '6ft charging cable', 12.99, 500);`,
    },
    {
      name: 'orders',
      title: '📦 Orders (5 cols)',
      sql: `CREATE TABLE IF NOT EXISTS orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total_amount DECIMAL(10, 2) NOT NULL,
  status VARCHAR(50) DEFAULT 'pending'
);

INSERT INTO orders (user_id, order_date, total_amount, status) VALUES
  (1, CURRENT_TIMESTAMP, 1329.97, 'completed'),
  (2, CURRENT_TIMESTAMP, 89.98, 'pending'),
  (1, CURRENT_TIMESTAMP, 299.99, 'shipped');`,
    },
    {
      name: 'employees',
      title: '👔 Employees (8 cols)',
      sql: `CREATE TABLE IF NOT EXISTS employees (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE,
  salary DECIMAL(10, 2),
  department VARCHAR(100),
  hire_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`,
    },
    {
      name: 'transactions',
      title: '💰 Transactions (7 cols)',
      sql: `CREATE TABLE IF NOT EXISTS transactions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  transaction_type VARCHAR(50),
  status VARCHAR(50) DEFAULT 'completed',
  description LONGTEXT,
  transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`,
    },
    {
      name: 'categories',
      title: '📂 Categories (3 cols)',
      sql: `CREATE TABLE IF NOT EXISTS categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  description LONGTEXT
);`,
    },
    {
      name: 'customers',
      title: '🏪 Customers (6 cols)',
      sql: `CREATE TABLE IF NOT EXISTS customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  phone VARCHAR(20),
  address LONGTEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`,
    },
    {
      name: 'inventory',
      title: '📊 Inventory (8 cols)',
      sql: `CREATE TABLE IF NOT EXISTS inventory (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  warehouse_id INT,
  quantity INT DEFAULT 0,
  reorder_level INT,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  supplier_id INT,
  cost DECIMAL(10, 2)
);`,
    },
    {
      name: 'reviews',
      title: '⭐ Reviews (5 cols)',
      sql: `CREATE TABLE IF NOT EXISTS reviews (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  user_id INT NOT NULL,
  rating INT CHECK (rating >= 1 AND rating <= 5),
  comment LONGTEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`,
    },
    {
      name: 'analytics',
      title: '📈 Analytics (10 cols)',
      sql: `CREATE TABLE IF NOT EXISTS analytics (
  id INT AUTO_INCREMENT PRIMARY KEY,
  date DATE NOT NULL,
  user_count INT,
  sessions INT,
  page_views INT,
  bounce_rate DECIMAL(5, 2),
  avg_session_duration INT,
  conversion_rate DECIMAL(5, 2),
  revenue DECIMAL(10, 2),
  top_page VARCHAR(255),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`,
    },
  ],
  mongodb: [
    {
      name: 'users',
      title: '👤 Users (4 fields)',
      sql: `// MongoDB Collection: users
// Sample documents (auto-created):
{ "_id": ObjectId(), "username": "john_doe", "email": "john@example.com", "created_at": ISODate() }
{ "_id": ObjectId(), "username": "jane_smith", "email": "jane@example.com", "created_at": ISODate() }
{ "_id": ObjectId(), "username": "bob_jones", "email": "bob@example.com", "created_at": ISODate() }
{ "_id": ObjectId(), "username": "alice_brown", "email": "alice@example.com", "created_at": ISODate() }`,
    },
    {
      name: 'products',
      title: '🛍️ Products (6 fields)',
      sql: `// MongoDB Collection: products
// Sample documents (auto-created):
{ "_id": ObjectId(), "name": "Laptop Pro", "description": "High performance laptop", "price": 1299.99, "stock": 45, "created_at": ISODate() }
{ "_id": ObjectId(), "name": "Wireless Mouse", "description": "Ergonomic design", "price": 29.99, "stock": 150, "created_at": ISODate() }
{ "_id": ObjectId(), "name": "USB-C Cable", "description": "6ft charging cable", "price": 12.99, "stock": 500, "created_at": ISODate() }
{ "_id": ObjectId(), "name": "Monitor 4K", "description": "Ultra HD display", "price": 599.99, "stock": 30, "created_at": ISODate() }`,
    },
    {
      name: 'orders',
      title: '📦 Orders (5 fields)',
      sql: `// MongoDB Collection: orders
// Sample documents (auto-created):
{ "_id": ObjectId(), "user_id": ObjectId(), "order_date": ISODate(), "total_amount": 1329.97, "status": "completed" }
{ "_id": ObjectId(), "user_id": ObjectId(), "order_date": ISODate(), "total_amount": 89.98, "status": "pending" }
{ "_id": ObjectId(), "user_id": ObjectId(), "order_date": ISODate(), "total_amount": 299.99, "status": "shipped" }
{ "_id": ObjectId(), "user_id": ObjectId(), "order_date": ISODate(), "total_amount": 149.98, "status": "completed" }`,
    },
    {
      name: 'employees',
      title: '👔 Employees (8 fields)',
      sql: `// MongoDB Collection: employees
// Sample documents (auto-created):
{ "_id": ObjectId(), "first_name": "John", "last_name": "Smith", "email": "john.smith@company.com", "salary": 75000, "department": "Engineering", "hire_date": ISODate(), "created_at": ISODate() }
{ "_id": ObjectId(), "first_name": "Sarah", "last_name": "Johnson", "email": "sarah.j@company.com", "salary": 85000, "department": "Management", "hire_date": ISODate(), "created_at": ISODate() }
{ "_id": ObjectId(), "first_name": "Mike", "last_name": "Davis", "email": "m.davis@company.com", "salary": 65000, "department": "Support", "hire_date": ISODate(), "created_at": ISODate() }
{ "_id": ObjectId(), "first_name": "Lisa", "last_name": "Anderson", "email": "l.anderson@company.com", "salary": 95000, "department": "Engineering", "hire_date": ISODate(), "created_at": ISODate() }`,
    },
    {
      name: 'transactions',
      title: '💰 Transactions (7 fields)',
      sql: `// MongoDB Collection: transactions
// Sample documents (auto-created):
{ "_id": ObjectId(), "user_id": ObjectId(), "amount": 500, "type": "credit", "status": "completed", "description": "Account deposit", "date": ISODate() }
{ "_id": ObjectId(), "user_id": ObjectId(), "amount": 150, "type": "debit", "status": "completed", "description": "Purchase order #123", "date": ISODate() }
{ "_id": ObjectId(), "user_id": ObjectId(), "amount": 1000, "type": "transfer", "status": "pending", "description": "Wire transfer", "date": ISODate() }
{ "_id": ObjectId(), "user_id": ObjectId(), "amount": 50, "type": "refund", "status": "completed", "description": "Product return", "date": ISODate() }`,
    },
    {
      name: 'categories',
      title: '📂 Categories (3 fields)',
      sql: `// MongoDB Collection: categories
// Sample documents (auto-created):
{ "_id": ObjectId(), "name": "Electronics", "description": "Electronic devices and gadgets" }
{ "_id": ObjectId(), "name": "Clothing", "description": "Apparel and fashion items" }
{ "_id": ObjectId(), "name": "Books", "description": "Physical and digital books" }
{ "_id": ObjectId(), "name": "Home & Garden", "description": "Home improvement and garden supplies" }`,
    },
    {
      name: 'customers',
      title: '🏪 Customers (6 fields)',
      sql: `// MongoDB Collection: customers
// Sample documents (auto-created):
{ "_id": ObjectId(), "first_name": "Robert", "last_name": "Wilson", "phone": "+1-555-0101", "address": "123 Main St, NYC, NY 10001", "created_at": ISODate() }
{ "_id": ObjectId(), "first_name": "Emily", "last_name": "Martinez", "phone": "+1-555-0102", "address": "456 Oak Ave, LA, CA 90001", "created_at": ISODate() }
{ "_id": ObjectId(), "first_name": "James", "last_name": "Taylor", "phone": "+1-555-0103", "address": "789 Pine Rd, Chicago, IL 60601", "created_at": ISODate() }
{ "_id": ObjectId(), "first_name": "Victoria", "last_name": "Garcia", "phone": "+1-555-0104", "address": "321 Elm St, Houston, TX 77001", "created_at": ISODate() }`,
    },
    {
      name: 'inventory',
      title: '📊 Inventory (8 fields)',
      sql: `// MongoDB Collection: inventory
// Sample documents (auto-created):
{ "_id": ObjectId(), "product_id": ObjectId(), "warehouse_id": 1, "quantity": 100, "reorder_level": 20, "last_updated": ISODate(), "supplier_id": 5, "cost": 899.99 }
{ "_id": ObjectId(), "product_id": ObjectId(), "warehouse_id": 2, "quantity": 45, "reorder_level": 10, "last_updated": ISODate(), "supplier_id": 3, "cost": 899.99 }
{ "_id": ObjectId(), "product_id": ObjectId(), "warehouse_id": 1, "quantity": 200, "reorder_level": 50, "last_updated": ISODate(), "supplier_id": 7, "cost": 20.00 }
{ "_id": ObjectId(), "product_id": ObjectId(), "warehouse_id": 3, "quantity": 75, "reorder_level": 15, "last_updated": ISODate(), "supplier_id": 2, "cost": 499.99 }`,
    },
    {
      name: 'reviews',
      title: '⭐ Reviews (5 fields)',
      sql: `// MongoDB Collection: reviews
// Sample documents (auto-created):
{ "_id": ObjectId(), "product_id": ObjectId(), "user_id": ObjectId(), "rating": 5, "comment": "Excellent quality and fast shipping!", "created_at": ISODate() }
{ "_id": ObjectId(), "product_id": ObjectId(), "user_id": ObjectId(), "rating": 4, "comment": "Good product, minor packaging issue", "created_at": ISODate() }
{ "_id": ObjectId(), "product_id": ObjectId(), "user_id": ObjectId(), "rating": 5, "comment": "Exceeded expectations, highly recommended", "created_at": ISODate() }
{ "_id": ObjectId(), "product_id": ObjectId(), "user_id": ObjectId(), "rating": 3, "comment": "Average product, as described", "created_at": ISODate() }`,
    },
    {
      name: 'analytics',
      title: '📈 Analytics (10 fields)',
      sql: `// MongoDB Collection: analytics
// Sample documents (auto-created):
{ "_id": ObjectId(), "date": ISODate("2026-04-10"), "user_count": 1250, "sessions": 3450, "page_views": 12300, "bounce_rate": 32.5, "avg_session_duration": 145, "conversion_rate": 2.8, "revenue": 8750.50, "top_page": "/products", "updated_at": ISODate() }
{ "_id": ObjectId(), "date": ISODate("2026-04-11"), "user_count": 1340, "sessions": 3680, "page_views": 13200, "bounce_rate": 30.2, "avg_session_duration": 152, "conversion_rate": 3.1, "revenue": 9250.75, "top_page": "/checkout", "updated_at": ISODate() }
{ "_id": ObjectId(), "date": ISODate("2026-04-12"), "user_count": 1450, "sessions": 4120, "page_views": 14500, "bounce_rate": 28.1, "avg_session_duration": 168, "conversion_rate": 3.5, "revenue": 10300.25, "top_page": "/products", "updated_at": ISODate() }
{ "_id": ObjectId(), "date": ISODate("2026-04-13"), "user_count": 1380, "sessions": 3950, "page_views": 13800, "bounce_rate": 31.3, "avg_session_duration": 158, "conversion_rate": 3.2, "revenue": 9800.00, "top_page": "/sale", "updated_at": ISODate() }`,
    },
  ],
  clickhouse: [
    {
      name: 'users',
      title: '👤 Users (4 cols)',
      sql: `CREATE TABLE IF NOT EXISTS users (
  id UInt32,
  username String,
  email String,
  created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY id;`,
    },
    {
      name: 'products',
      title: '🛍️ Products (6 cols)',
      sql: `CREATE TABLE IF NOT EXISTS products (
  id UInt32,
  name String,
  description String,
  price Decimal(10, 2),
  stock UInt32,
  created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY id;`,
    },
    {
      name: 'orders',
      title: '📦 Orders (5 cols)',
      sql: `CREATE TABLE IF NOT EXISTS orders (
  id UInt32,
  user_id UInt32,
  order_date DateTime DEFAULT now(),
  total_amount Decimal(10, 2),
  status String
) ENGINE = MergeTree()
ORDER BY (id, user_id, order_date);`,
    },
    {
      name: 'employees',
      title: '👔 Employees (8 cols)',
      sql: `CREATE TABLE IF NOT EXISTS employees (
  id UInt32,
  first_name String,
  last_name String,
  email String,
  salary Decimal(10, 2),
  department String,
  hire_date Date,
  created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY id;`,
    },
    {
      name: 'transactions',
      title: '💰 Transactions (7 cols)',
      sql: `CREATE TABLE IF NOT EXISTS transactions (
  id UInt32,
  user_id UInt32,
  amount Decimal(10, 2),
  transaction_type String,
  status String,
  description String,
  transaction_date DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (transaction_date, user_id);`,
    },
    {
      name: 'categories',
      title: '📂 Categories (3 cols)',
      sql: `CREATE TABLE IF NOT EXISTS categories (
  id UInt32,
  name String,
  description String
) ENGINE = MergeTree()
ORDER BY id;`,
    },
    {
      name: 'customers',
      title: '🏪 Customers (6 cols)',
      sql: `CREATE TABLE IF NOT EXISTS customers (
  id UInt32,
  first_name String,
  last_name String,
  phone String,
  address String,
  created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY id;`,
    },
    {
      name: 'inventory',
      title: '📊 Inventory (8 cols)',
      sql: `CREATE TABLE IF NOT EXISTS inventory (
  id UInt32,
  product_id UInt32,
  warehouse_id UInt32,
  quantity UInt32,
  reorder_level UInt32,
  last_updated DateTime DEFAULT now(),
  supplier_id UInt32,
  cost Decimal(10, 2)
) ENGINE = MergeTree()
ORDER BY (warehouse_id, product_id);`,
    },
    {
      name: 'reviews',
      title: '⭐ Reviews (5 cols)',
      sql: `CREATE TABLE IF NOT EXISTS reviews (
  id UInt32,
  product_id UInt32,
  user_id UInt32,
  rating UInt8,
  comment String,
  created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (product_id, created_at);`,
    },
    {
      name: 'analytics',
      title: '📈 Analytics (10 cols)',
      sql: `CREATE TABLE IF NOT EXISTS analytics (
  id UInt32,
  date Date,
  user_count UInt32,
  sessions UInt32,
  page_views UInt32,
  bounce_rate Decimal(5, 2),
  avg_session_duration UInt32,
  conversion_rate Decimal(5, 2),
  revenue Decimal(10, 2),
  top_page String
) ENGINE = MergeTree()
ORDER BY date;`,
    },
  ],
};

const SEED_SQL_BY_DB: Record<string, Record<string, string>> = {
  postgresql: {
  products: `INSERT INTO products (name, description, price, stock) VALUES
  ('Laptop Pro', 'High-performance laptop', 1299.99, 45),
  ('Wireless Mouse', 'Ergonomic wireless mouse', 29.99, 150),
  ('USB-C Cable', '6ft charging cable', 12.99, 500);`,
  employees: `INSERT INTO employees (first_name, last_name, email, salary, department, hire_date) VALUES
  ('John', 'Smith', 'john.smith@company.com', 75000.00, 'Engineering', '2024-01-10'),
  ('Sarah', 'Johnson', 'sarah.johnson@company.com', 85000.00, 'Management', '2023-08-15'),
  ('Mike', 'Davis', 'mike.davis@company.com', 65000.00, 'Support', '2024-03-01');`,
  transactions: `INSERT INTO transactions (user_id, amount, transaction_type, status, description, transaction_date) VALUES
  (1, 500.00, 'credit', 'completed', 'Account deposit', CURRENT_TIMESTAMP),
  (2, 150.00, 'debit', 'completed', 'Purchase order #123', CURRENT_TIMESTAMP),
  (1, 1000.00, 'transfer', 'pending', 'Wire transfer', CURRENT_TIMESTAMP);`,
  categories: `INSERT INTO categories (name, description) VALUES
  ('Electronics', 'Electronic devices and gadgets'),
  ('Clothing', 'Apparel and fashion items'),
  ('Books', 'Physical and digital books');`,
  customers: `INSERT INTO customers (first_name, last_name, phone, address) VALUES
  ('Robert', 'Wilson', '+1-555-0101', '123 Main St, NYC, NY 10001'),
  ('Emily', 'Martinez', '+1-555-0102', '456 Oak Ave, LA, CA 90001'),
  ('James', 'Taylor', '+1-555-0103', '789 Pine Rd, Chicago, IL 60601');`,
  inventory: `INSERT INTO inventory (product_id, warehouse_id, quantity, reorder_level, last_updated, supplier_id, cost) VALUES
  (1, 1, 100, 20, CURRENT_TIMESTAMP, 5, 899.99),
  (2, 2, 45, 10, CURRENT_TIMESTAMP, 3, 199.99),
  (3, 1, 200, 50, CURRENT_TIMESTAMP, 7, 20.00);`,
  reviews: `INSERT INTO reviews (product_id, user_id, rating, comment) VALUES
  (1, 1, 5, 'Excellent quality and fast shipping!'),
  (2, 2, 4, 'Good product with great value'),
  (3, 1, 5, 'Exceeded expectations.');`,
  analytics: `INSERT INTO analytics (date, user_count, sessions, page_views, bounce_rate, avg_session_duration, conversion_rate, revenue, top_page) VALUES
  ('2026-04-10', 1250, 3450, 12300, 32.5, 145, 2.8, 8750.50, '/products'),
  ('2026-04-11', 1340, 3680, 13200, 30.2, 152, 3.1, 9250.75, '/checkout'),
  ('2026-04-12', 1450, 4120, 14500, 28.1, 168, 3.5, 10300.25, '/products');`,
  },
  mysql: {
    transactions: `INSERT INTO transactions (user_id, amount, transaction_type, status, description, transaction_date) VALUES
  (1, 500.00, 'credit', 'completed', 'Account deposit', CURRENT_TIMESTAMP),
  (2, 150.00, 'debit', 'completed', 'Purchase order #123', CURRENT_TIMESTAMP),
  (1, 1000.00, 'transfer', 'pending', 'Wire transfer', CURRENT_TIMESTAMP);`,
  },
  clickhouse: {
    transactions: `INSERT INTO transactions (id, user_id, amount, transaction_type, status, description, transaction_date) VALUES
  (1, 1, 500.00, 'credit', 'completed', 'Account deposit', now()),
  (2, 2, 150.00, 'debit', 'completed', 'Purchase order #123', now()),
  (3, 1, 1000.00, 'transfer', 'pending', 'Wire transfer', now());`,
  },
};

const composeTemplateSql = (template: { name: string; sql: string }, dbType: string) => {
  const normalizedSql = template.sql.toLowerCase();
  const alreadyContainsSampleData =
    normalizedSql.includes('insert into') ||
    normalizedSql.includes('sample documents');

  if (alreadyContainsSampleData) {
    return template.sql;
  }

  const seedSql = SEED_SQL_BY_DB[dbType]?.[template.name];
  if (seedSql) {
    return `${template.sql}\n\n${seedSql}`;
  }

  return template.sql;
};

export function TableCreationForm({ connection, onTableCreated }: TableCreationFormProps) {
  const toast = useToast();
  const [isExpanded, setIsExpanded] = useState(false);
  const [tableName, setTableName] = useState('');
  const [sqlStatement, setSqlStatement] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  if (!connection) {
    return null;
  }

  const templates = TABLE_TEMPLATES[connection.db_type as keyof typeof TABLE_TEMPLATES] || [];

  const handleRandomTemplate = () => {
    const randomIndex = Math.floor(Math.random() * templates.length);
    const template = templates[randomIndex];
    setTableName(template.name);
    setSqlStatement(composeTemplateSql(template, connection.db_type));
  };

  const handleSelectTemplate = (template: typeof templates[0]) => {
    setTableName(template.name);
    setSqlStatement(composeTemplateSql(template, connection.db_type));
  };

  const handleCreateTable = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!tableName.trim()) {
      toast.error('Please enter a table name');
      return;
    }

    if (!sqlStatement.trim()) {
      toast.error('Please enter a SQL statement');
      return;
    }

    setIsLoading(true);
    try {
      await createTable(connection.id, sqlStatement);
      
      // Reset form
      setTableName('');
      setSqlStatement('');
      setIsExpanded(false);
      
      toast.success(`Table "${tableName}" created successfully!`);
      if (onTableCreated) {
        onTableCreated();
      }
    } catch (err) {
      toast.error(`Failed to create table: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-4 border rounded-lg bg-blue-50 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-bold text-blue-900 flex items-center gap-2">
          📋 Create New Table
          {isExpanded && <span className="text-xs bg-blue-200 px-2 py-1 rounded">No tables found</span>}
        </h3>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-xs bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition"
        >
          {isExpanded ? 'Hide' : 'Show'}
        </button>
      </div>

      {isExpanded && (
        <form onSubmit={handleCreateTable} className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Table Name
            </label>
            <input
              type="text"
              value={tableName}
              onChange={(e) => setTableName(e.target.value)}
              placeholder="Enter table name"
              className="w-full px-2 py-2 border border-gray-300 rounded text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-xs font-medium text-gray-700">
                SQL Statement
              </label>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={handleRandomTemplate}
                  className="text-xs text-green-600 hover:text-green-800 underline font-semibold"
                  title="Load a random template"
                >
                  🎲 Random
                </button>
                <button
                  type="button"
                  onClick={() => setSqlStatement('')}
                  className="text-xs text-gray-600 hover:text-gray-800 underline"
                >
                  Clear
                </button>
              </div>
            </div>

            {/* Template Selection Grid */}
            <div className="grid grid-cols-2 gap-2 mb-3 p-2 bg-white rounded border border-gray-200">
              {templates.map((template, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => handleSelectTemplate(template)}
                  className={`px-2 py-1 text-xs rounded transition ${
                    tableName === template.name
                      ? 'bg-blue-500 text-white font-semibold'
                      : 'bg-gray-100 hover:bg-gray-200 text-gray-800'
                  }`}
                  title={template.sql}
                >
                  {template.title}
                </button>
              ))}
            </div>

            <textarea
              value={sqlStatement}
              onChange={(e) => setSqlStatement(e.target.value)}
              placeholder="Enter SQL CREATE TABLE statement or select a template above"
              className="w-full px-2 py-2 border border-gray-300 rounded text-xs font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 h-24"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              Database: <span className="font-semibold">{connection.db_type.toUpperCase()}</span>
            </p>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full px-3 py-2 bg-blue-500 text-white text-sm font-medium rounded hover:bg-blue-600 disabled:bg-gray-400 transition"
          >
            {isLoading ? 'Creating...' : 'Create Table'}
          </button>
        </form>
      )}

      {!isExpanded && (
        <p className="text-xs text-gray-600">
          Click "Show" to create a new table for this connection
        </p>
      )}
    </div>
  );
}
