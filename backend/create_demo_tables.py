#!/usr/bin/env python3
"""
Create demo tables and data in ALL test databases (PostgreSQL, MySQL, MongoDB, ClickHouse)
Creates tables for each database type with sample data so extractions work.
Supports all 4 users and all 4 database types.
"""

import os
import django
import mysql.connector
import pymongo
import psycopg2
from clickhouse_driver import Client
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# PostgreSQL Demo Data
def create_postgresql_tables():
    print("\n📊 Creating PostgreSQL demo tables...")
    try:
        conn = psycopg2.connect(
            host='db',
            port=5432,
            user='user',
            password='password',
            database='dataconnector'
        )
        cursor = conn.cursor()
        
        # Create clients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                country VARCHAR(100)
            )
        """)
        cursor.execute("INSERT INTO clients (id, name, email, phone, country) VALUES (1, 'Acme Corp', 'contact@acme.com', '555-0001', 'USA') ON CONFLICT DO NOTHING")
        cursor.execute("INSERT INTO clients (id, name, email, phone, country) VALUES (2, 'Global Industries', 'info@global.com', '555-0002', 'UK') ON CONFLICT DO NOTHING")
        cursor.execute("INSERT INTO clients (id, name, email, phone, country) VALUES (3, 'Tech Solutions', 'hello@techsol.com', '555-0003', 'Canada') ON CONFLICT DO NOTHING")
        
        # Create invoices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id SERIAL PRIMARY KEY,
                client_id INT NOT NULL,
                amount DECIMAL(10,2),
                status VARCHAR(50),
                created_at DATE
            )
        """)
        cursor.execute("INSERT INTO invoices (id, client_id, amount, status, created_at) VALUES (101, 1, 5000.00, 'paid', '2026-01-15') ON CONFLICT DO NOTHING")
        cursor.execute("INSERT INTO invoices (id, client_id, amount, status, created_at) VALUES (102, 2, 3500.50, 'pending', '2026-02-20') ON CONFLICT DO NOTHING")
        cursor.execute("INSERT INTO invoices (id, client_id, amount, status, created_at) VALUES (103, 3, 7200.00, 'paid', '2026-03-10') ON CONFLICT DO NOTHING")
        
        # Create payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                invoice_id INT NOT NULL,
                amount DECIMAL(10,2),
                payment_date DATE,
                method VARCHAR(50)
            )
        """)
        cursor.execute("INSERT INTO payments (id, invoice_id, amount, payment_date, method) VALUES (201, 101, 5000.00, '2026-01-20', 'bank_transfer') ON CONFLICT DO NOTHING")
        cursor.execute("INSERT INTO payments (id, invoice_id, amount, payment_date, method) VALUES (202, 103, 7200.00, '2026-03-15', 'credit_card') ON CONFLICT DO NOTHING")
        
        # Create suppliers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                contact_email VARCHAR(255),
                country VARCHAR(100)
            )
        """)
        cursor.execute("INSERT INTO suppliers (id, name, contact_email, country) VALUES (1, 'Parts Supplier Inc', 'supply@parts.com', 'Germany') ON CONFLICT DO NOTHING")
        cursor.execute("INSERT INTO suppliers (id, name, contact_email, country) VALUES (2, 'Materials Co', 'info@materials.com', 'Japan') ON CONFLICT DO NOTHING")
        
        # Create purchase_orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id SERIAL PRIMARY KEY,
                supplier_id INT NOT NULL,
                order_date DATE,
                total_amount DECIMAL(10,2)
            )
        """)
        cursor.execute("INSERT INTO purchase_orders (id, supplier_id, order_date, total_amount) VALUES (501, 1, '2026-01-05', 15000.00) ON CONFLICT DO NOTHING")
        cursor.execute("INSERT INTO purchase_orders (id, supplier_id, order_date, total_amount) VALUES (502, 2, '2026-02-10', 22000.00) ON CONFLICT DO NOTHING")
        
        # Create shipments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shipments (
                id SERIAL PRIMARY KEY,
                purchase_order_id INT NOT NULL,
                ship_date DATE,
                delivery_date DATE,
                status VARCHAR(50)
            )
        """)
        cursor.execute("INSERT INTO shipments (id, purchase_order_id, ship_date, delivery_date, status) VALUES (601, 501, '2026-01-10', '2026-01-25', 'delivered') ON CONFLICT DO NOTHING")
        cursor.execute("INSERT INTO shipments (id, purchase_order_id, ship_date, delivery_date, status) VALUES (602, 502, '2026-02-15', '2026-03-05', 'in_transit') ON CONFLICT DO NOTHING")
        
        # Create locations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                city VARCHAR(100),
                country VARCHAR(100),
                warehouse BOOLEAN
            )
        """)
        cursor.execute("INSERT INTO locations (id, name, city, country, warehouse) VALUES (701, 'NYC Office', 'New York', 'USA', false) ON CONFLICT DO NOTHING")
        cursor.execute("INSERT INTO locations (id, name, city, country, warehouse) VALUES (702, 'Chicago Warehouse', 'Chicago', 'USA', true) ON CONFLICT DO NOTHING")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ PostgreSQL tables created successfully")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL error: {e}")
        return False


# MySQL Demo Data
def create_mysql_tables():
    print("\n📊 Creating MySQL demo tables...")
    try:
        conn = mysql.connector.connect(
            host='mysql',
            port=3306,
            user='root',
            password='rootpassword',
            database='testdb'
        )
        cursor = conn.cursor()
        
        # Create clients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                country VARCHAR(100)
            )
        """)
        cursor.execute("INSERT IGNORE INTO clients (id, name, email, phone, country) VALUES (1, 'Acme Corp', 'contact@acme.com', '555-0001', 'USA')")
        cursor.execute("INSERT IGNORE INTO clients (id, name, email, phone, country) VALUES (2, 'Global Industries', 'info@global.com', '555-0002', 'UK')")
        cursor.execute("INSERT IGNORE INTO clients (id, name, email, phone, country) VALUES (3, 'Tech Solutions', 'hello@techsol.com', '555-0003', 'Canada')")
        
        # Create invoices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INT PRIMARY KEY AUTO_INCREMENT,
                client_id INT NOT NULL,
                amount DECIMAL(10,2),
                status VARCHAR(50),
                created_at DATE
            )
        """)
        cursor.execute("INSERT IGNORE INTO invoices (id, client_id, amount, status, created_at) VALUES (101, 1, 5000.00, 'paid', '2026-01-15')")
        cursor.execute("INSERT IGNORE INTO invoices (id, client_id, amount, status, created_at) VALUES (102, 2, 3500.50, 'pending', '2026-02-20')")
        cursor.execute("INSERT IGNORE INTO invoices (id, client_id, amount, status, created_at) VALUES (103, 3, 7200.00, 'paid', '2026-03-10')")
        
        # Create payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INT PRIMARY KEY AUTO_INCREMENT,
                invoice_id INT NOT NULL,
                amount DECIMAL(10,2),
                payment_date DATE,
                method VARCHAR(50)
            )
        """)
        cursor.execute("INSERT IGNORE INTO payments (id, invoice_id, amount, payment_date, method) VALUES (201, 101, 5000.00, '2026-01-20', 'bank_transfer')")
        cursor.execute("INSERT IGNORE INTO payments (id, invoice_id, amount, payment_date, method) VALUES (202, 103, 7200.00, '2026-03-15', 'credit_card')")
        
        # Create suppliers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                contact_email VARCHAR(255),
                country VARCHAR(100)
            )
        """)
        cursor.execute("INSERT IGNORE INTO suppliers (id, name, contact_email, country) VALUES (1, 'Parts Supplier Inc', 'supply@parts.com', 'Germany')")
        cursor.execute("INSERT IGNORE INTO suppliers (id, name, contact_email, country) VALUES (2, 'Materials Co', 'info@materials.com', 'Japan')")
        
        # Create purchase_orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id INT PRIMARY KEY AUTO_INCREMENT,
                supplier_id INT NOT NULL,
                order_date DATE,
                total_amount DECIMAL(10,2)
            )
        """)
        cursor.execute("INSERT IGNORE INTO purchase_orders (id, supplier_id, order_date, total_amount) VALUES (501, 1, '2026-01-05', 15000.00)")
        cursor.execute("INSERT IGNORE INTO purchase_orders (id, supplier_id, order_date, total_amount) VALUES (502, 2, '2026-02-10', 22000.00)")
        
        # Create shipments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shipments (
                id INT PRIMARY KEY AUTO_INCREMENT,
                purchase_order_id INT NOT NULL,
                ship_date DATE,
                delivery_date DATE,
                status VARCHAR(50)
            )
        """)
        cursor.execute("INSERT IGNORE INTO shipments (id, purchase_order_id, ship_date, delivery_date, status) VALUES (601, 501, '2026-01-10', '2026-01-25', 'delivered')")
        cursor.execute("INSERT IGNORE INTO shipments (id, purchase_order_id, ship_date, delivery_date, status) VALUES (602, 502, '2026-02-15', '2026-03-05', 'in_transit')")
        
        # Create locations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                city VARCHAR(100),
                country VARCHAR(100),
                warehouse BOOLEAN
            )
        """)
        cursor.execute("INSERT IGNORE INTO locations (id, name, city, country, warehouse) VALUES (701, 'NYC Office', 'New York', 'USA', 0)")
        cursor.execute("INSERT IGNORE INTO locations (id, name, city, country, warehouse) VALUES (702, 'Chicago Warehouse', 'Chicago', 'USA', 1)")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ MySQL tables created successfully")
        return True
    except Exception as e:
        print(f"❌ MySQL error: {e}")
        return False


# MongoDB Demo Data
def create_mongodb_collections():
    print("\n📊 Creating MongoDB demo collections...")
    try:
        client = pymongo.MongoClient('mongodb://mongo:27017/')
        db = client['test_mongodb']
        
        # Create articles collection
        articles_collection = db['articles']
        articles_collection.drop()
        articles_collection.insert_many([
            {'_id': 1, 'title': 'Introduction to MongoDB', 'author': 'Alice', 'date': '2026-01-01', 'views': 150},
            {'_id': 2, 'title': 'Advanced MongoDB Queries', 'author': 'Bob', 'date': '2026-01-15', 'views': 320},
            {'_id': 3, 'title': 'MongoDB Best Practices', 'author': 'Charlie', 'date': '2026-02-01', 'views': 250},
        ])
        
        # Create comments collection
        comments_collection = db['comments']
        comments_collection.drop()
        comments_collection.insert_many([
            {'_id': 1, 'article_id': 1, 'user': 'user1', 'text': 'Great article!', 'date': '2026-01-02'},
            {'_id': 2, 'article_id': 1, 'user': 'user2', 'text': 'Very helpful', 'date': '2026-01-03'},
            {'_id': 3, 'article_id': 2, 'user': 'user3', 'text': 'Thanks for sharing', 'date': '2026-01-16'},
        ])
        
        # Create authors collection
        authors_collection = db['authors']
        authors_collection.drop()
        authors_collection.insert_many([
            {'_id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'bio': 'Data Engineer'},
            {'_id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'bio': 'Full Stack Developer'},
            {'_id': 3, 'name': 'Charlie', 'email': 'charlie@example.com', 'bio': 'DevOps Engineer'},
        ])
        
        # Create sessions collection
        sessions_collection = db['sessions']
        sessions_collection.drop()
        sessions_collection.insert_many([
            {'_id': 1, 'user_id': 'user1', 'login_time': '2026-04-17T10:00:00', 'logout_time': '2026-04-17T10:30:00'},
            {'_id': 2, 'user_id': 'user2', 'login_time': '2026-04-17T10:15:00', 'logout_time': '2026-04-17T11:00:00'},
        ])
        
        # Create logs collection
        logs_collection = db['logs']
        logs_collection.drop()
        logs_collection.insert_many([
            {'_id': 1, 'level': 'INFO', 'message': 'Application started', 'timestamp': '2026-04-17T09:00:00'},
            {'_id': 2, 'level': 'WARNING', 'message': 'High memory usage', 'timestamp': '2026-04-17T09:30:00'},
        ])
        
        # Create media collection
        media_collection = db['media']
        media_collection.drop()
        media_collection.insert_many([
            {'_id': 1, 'type': 'image', 'filename': 'photo1.jpg', 'size_bytes': 2048000, 'uploaded_by': 'alice'},
            {'_id': 2, 'type': 'video', 'filename': 'tutorial.mp4', 'size_bytes': 102400000, 'uploaded_by': 'bob'},
        ])
        
        # Create tags collection
        tags_collection = db['tags']
        tags_collection.drop()
        tags_collection.insert_many([
            {'_id': 1, 'name': 'mongodb', 'count': 25},
            {'_id': 2, 'name': 'database', 'count': 45},
            {'_id': 3, 'name': 'tutorial', 'count': 18},
        ])
        
        client.close()
        print("✅ MongoDB collections created successfully")
        return True
    except Exception as e:
        print(f"❌ MongoDB error: {e}")
        return False


# ClickHouse Demo Data
def create_clickhouse_tables():
    print("\n📊 Creating ClickHouse demo tables...")
    try:
        client = Client('clickhouse', port=9000)
        
        # Create page_views table
        client.execute("""
            CREATE TABLE IF NOT EXISTS page_views (
                page_id String,
                view_time DateTime,
                user_id String,
                country String
            ) ENGINE = Memory
        """)
        client.execute("INSERT INTO page_views VALUES ('page1', now(), 'user1', 'USA')")
        client.execute("INSERT INTO page_views VALUES ('page2', now(), 'user2', 'UK')")
        client.execute("INSERT INTO page_views VALUES ('page1', now(), 'user3', 'Canada')")
        
        # Create events table
        client.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id String,
                event_type String,
                event_time DateTime,
                user_id String
            ) ENGINE = Memory
        """)
        client.execute("INSERT INTO events VALUES ('evt1', 'click', now(), 'user1')")
        client.execute("INSERT INTO events VALUES ('evt2', 'scroll', now(), 'user2')")
        
        # Create users_ch table
        client.execute("""
            CREATE TABLE IF NOT EXISTS users_ch (
                user_id String,
                name String,
                signup_date Date
            ) ENGINE = Memory
        """)
        client.execute("INSERT INTO users_ch VALUES ('user1', 'Alice', toDate(now()))")
        client.execute("INSERT INTO users_ch VALUES ('user2', 'Bob', toDate(now()))")
        
        # Create sessions_ch table
        client.execute("""
            CREATE TABLE IF NOT EXISTS sessions_ch (
                session_id String,
                user_id String,
                duration_seconds Int32
            ) ENGINE = Memory
        """)
        client.execute("INSERT INTO sessions_ch VALUES ('sess1', 'user1', 1800)")
        client.execute("INSERT INTO sessions_ch VALUES ('sess2', 'user2', 2400)")
        
        # Create performance table
        client.execute("""
            CREATE TABLE IF NOT EXISTS performance (
                metric_name String,
                value Float32,
                timestamp DateTime
            ) ENGINE = Memory
        """)
        client.execute("INSERT INTO performance VALUES ('cpu_usage', 45.5, now())")
        client.execute("INSERT INTO performance VALUES ('memory_usage', 62.3, now())")
        
        # Create errors table
        client.execute("""
            CREATE TABLE IF NOT EXISTS errors (
                error_id String,
                error_message String,
                stack_trace String,
                timestamp DateTime
            ) ENGINE = Memory
        """)
        client.execute("INSERT INTO errors VALUES ('err1', 'Database connection failed', 'at connect()', now())")
        
        # Create campaigns table
        client.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                campaign_id String,
                campaign_name String,
                budget Float32,
                status String
            ) ENGINE = Memory
        """)
        client.execute("INSERT INTO campaigns VALUES ('camp1', 'Spring Sale', 5000.0, 'active')")
        client.execute("INSERT INTO campaigns VALUES ('camp2', 'Summer Promo', 7500.0, 'planned')")
        
        print("✅ ClickHouse tables created successfully")
        return True
    except Exception as e:
        print(f"❌ ClickHouse error: {e}")
        return False


# Cleanup stored files older than 24 hours
def cleanup_old_stored_files():
    """Remove extracted files older than 24 hours to keep storage clean"""
    print("\n🧹 Cleaning up extracted files older than 24 hours...")
    try:
        from connector.models import StoredFile
        from datetime import timedelta
        from django.utils import timezone
        
        cutoff_time = timezone.now() - timedelta(hours=24)
        old_files = StoredFile.objects.filter(extracted_at__lt=cutoff_time)
        count = old_files.count()
        
        if count > 0:
            # Delete the files from storage
            import os
            for stored_file in old_files:
                if stored_file.filepath and os.path.exists(f'/app/backend{stored_file.filepath}'):
                    try:
                        os.remove(f'/app/backend{stored_file.filepath}')
                    except Exception as e:
                        print(f"  ⚠️  Failed to delete file {stored_file.filepath}: {e}")
            
            # Delete from database
            old_files.delete()
            print(f"✅ Deleted {count} files older than 24 hours")
        else:
            print("✅ No files older than 24 hours to delete")
        
        return True
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
        return False


if __name__ == '__main__':
    print("=" * 80)
    print("🚀 Creating Demo Tables in ALL Test Databases (PostgreSQL, MySQL, MongoDB, ClickHouse)")
    print("=" * 80)
    
    results = [
        create_postgresql_tables(),
        create_mysql_tables(),
        create_mongodb_collections(),
        create_clickhouse_tables(),
        cleanup_old_stored_files(),
    ]
    
    print("\n" + "=" * 80)
    if all(results):
        print("✨ All demo tables created successfully!")
        print("✅ Cleanup completed!")
    else:
        print("⚠️  Some operations had issues. Check errors above.")
    print("=" * 80)
    
    print("\n📊 Database Summary:")
    print("  • PostgreSQL: 7 tables (clients, invoices, payments, suppliers, purchase_orders, shipments, locations)")
    print("  • MySQL:      7 tables (clients, invoices, payments, suppliers, purchase_orders, shipments, locations)")
    print("  • MongoDB:    7 collections (articles, comments, authors, sessions, logs, media, tags)")
    print("  • ClickHouse: 7 tables (page_views, events, users_ch, sessions_ch, performance, errors, campaigns)")
    print("\n✅ These tables are now available for extraction by all users!")


