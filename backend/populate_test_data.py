#!/usr/bin/env python3
"""
Script to populate all databases with test data for the Data Connector Platform
"""
import psycopg2
import mysql.connector
import pymongo
from clickhouse_driver import Client
import json
from datetime import datetime

# Test data
test_users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
    {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'},
    {'id': 4, 'name': 'Diana', 'email': 'diana@example.com'},
    {'id': 5, 'name': 'Eve', 'email': 'eve@example.com'},
]

def populate_postgresql():
    """Populate PostgreSQL with test data"""
    print("Populating PostgreSQL...")
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5433,
            user='user',
            password='password',
            database='dataconnector'
        )
        cursor = conn.cursor()
        
        # Check if table exists and has data
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("  Inserting 5 test records...")
            for user in test_users:
                cursor.execute(
                    "INSERT INTO users (id, name, email) VALUES (%s, %s, %s)",
                    (user['id'], user['name'], user['email'])
                )
            conn.commit()
        else:
            print(f"  Already populated with {count} records")
        
        cursor.execute("SELECT COUNT(*) FROM users")
        final_count = cursor.fetchone()[0]
        print(f"  ✓ PostgreSQL has {final_count} users")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"  ✗ PostgreSQL Error: {e}")

def populate_mysql():
    """Populate MySQL with test data"""
    print("Populating MySQL...")
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='user',
            password='password',
            database='testdb'
        )
        cursor = conn.cursor()
        
        # Drop and recreate table
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("  Inserting 5 test records...")
        for user in test_users:
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (user['name'], user['email'])
            )
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        final_count = cursor.fetchone()[0]
        print(f"  ✓ MySQL has {final_count} users")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"  ✗ MySQL Error: {e}")

def populate_mongodb():
    """Populate MongoDB with test data"""
    print("Populating MongoDB...")
    try:
        client = pymongo.MongoClient(
            'mongodb://localhost:27018',
            serverSelectionTimeoutMS=5000
        )
        # Test connection
        client.admin.command('ping')
        
        db = client['testdb']
        collection = db['users']
        
        # Clear existing data
        collection.delete_many({})
        
        print("  Inserting 5 test records...")
        collection.insert_many(test_users)
        
        final_count = collection.count_documents({})
        print(f"  ✓ MongoDB has {final_count} users")
        
        client.close()
    except Exception as e:
        print(f"  ✗ MongoDB Error: {e}")

def populate_clickhouse():
    """Populate ClickHouse with test data"""
    print("Populating ClickHouse...")
    try:
        client = Client('localhost', port=9001)
        
        # Create database if not exists
        client.execute('CREATE DATABASE IF NOT EXISTS testdb')
        
        # Create or replace table
        client.execute('''
            CREATE TABLE IF NOT EXISTS testdb.users (
                id UInt32,
                name String,
                email String,
                created_at DateTime DEFAULT now()
            ) ENGINE = MergeTree()
            ORDER BY id
        ''')
        
        print("  Inserting 5 test records...")
        data = [
            (user['id'], user['name'], user['email']) 
            for user in test_users
        ]
        client.execute('INSERT INTO testdb.users (id, name, email) VALUES', data)
        
        result = client.execute('SELECT COUNT(*) FROM testdb.users')
        final_count = result[0][0]
        print(f"  ✓ ClickHouse has {final_count} users")
        
        client.disconnect()
    except Exception as e:
        print(f"  ✗ ClickHouse Error: {e}")

def verify_all():
    """Verify all databases are populated"""
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    # PostgreSQL
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5433,
            user='user',
            password='password',
            database='dataconnector'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"✓ PostgreSQL: {count} records")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"✗ PostgreSQL: {e}")
    
    # MySQL
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='user',
            password='password',
            database='testdb'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"✓ MySQL: {count} records")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"✗ MySQL: {e}")
    
    # MongoDB
    try:
        client = pymongo.MongoClient(
            'mongodb://localhost:27018',
            serverSelectionTimeoutMS=5000
        )
        db = client['testdb']
        collection = db['users']
        count = collection.count_documents({})
        print(f"✓ MongoDB: {count} records")
        client.close()
    except Exception as e:
        print(f"✗ MongoDB: {e}")
    
    # ClickHouse
    try:
        client = Client('localhost', port=9001)
        result = client.execute('SELECT COUNT(*) FROM testdb.users')
        count = result[0][0]
        print(f"✓ ClickHouse: {count} records")
        client.disconnect()
    except Exception as e:
        print(f"✗ ClickHouse: {e}")

if __name__ == '__main__':
    print("="*60)
    print("DATA CONNECTOR PLATFORM - TEST DATA POPULATION")
    print("="*60 + "\n")
    
    populate_postgresql()
    populate_mysql()
    populate_mongodb()
    populate_clickhouse()
    
    verify_all()
    
    print("\n" + "="*60)
    print("Population Complete!")
    print("="*60)
