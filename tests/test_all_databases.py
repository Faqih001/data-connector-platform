"""
Comprehensive Database Connection & Table Creation Test Suite
Tests all 4 supported databases: PostgreSQL, MySQL, MongoDB, ClickHouse
"""
import os
import sys
import django
import datetime

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from connector.models import DatabaseConnection
from connector.connectors import (
    PostgresConnector,
    MySQLConnector,
    MongoConnector,
    ClickHouseConnector
)


def test_postgresql():
    """Test PostgreSQL connection and table creation"""
    print("\n[1] PostgreSQL")
    try:
        pg_conn = DatabaseConnection.objects.get(name='Postgresql Connection (admin)')
        connector = PostgresConnector(pg_conn)
        connector.connect()
        
        # Create table
        sql = """CREATE TABLE IF NOT EXISTS final_users_test (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            created_at TIMESTAMP DEFAULT NOW()
        )"""
        cursor = connector.connection.cursor()
        cursor.execute(sql)
        connector.connection.commit()
        
        # Verify
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'final_users_test'")
        exists = cursor.fetchone() is not None
        connector.close()
        
        if exists:
            print("    ✅ PASS - PostgreSQL table creation working")
            return ("PostgreSQL", "✅ PASS")
        else:
            print("    ❌ FAIL - Table not created")
            return ("PostgreSQL", "❌ FAIL")
    except Exception as e:
        print(f"    ❌ ERROR: {str(e)[:80]}")
        return ("PostgreSQL", "❌ ERROR")


def test_mysql():
    """Test MySQL connection and table creation"""
    print("\n[2] MySQL")
    try:
        mysql_conn = DatabaseConnection.objects.get(name='Mysql Connection (admin)')
        connector = MySQLConnector(mysql_conn)
        connector.connect()
        
        # Create table
        sql = """CREATE TABLE IF NOT EXISTS final_products_test (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        cursor = connector.connection.cursor()
        cursor.execute(sql)
        connector.connection.commit()
        
        # Verify
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'final_products_test' AND table_schema = DATABASE()")
        exists = cursor.fetchone() is not None
        connector.close()
        
        if exists:
            print("    ✅ PASS - MySQL table creation working")
            return ("MySQL", "✅ PASS")
        else:
            print("    ❌ FAIL - Table not created")
            return ("MySQL", "❌ FAIL")
    except Exception as e:
        print(f"    ❌ ERROR: {str(e)[:80]}")
        return ("MySQL", "❌ ERROR")


def test_mongodb():
    """Test MongoDB connection and collection creation"""
    print("\n[3] MongoDB")
    try:
        mongo_conn = DatabaseConnection.objects.get(name='Mongodb Connection (admin)')
        connector = MongoConnector(mongo_conn)
        connector.connect()
        
        # Create collection by inserting document
        db = connector.connection[mongo_conn.database_name]
        collection = db['final_orders_test']
        result = collection.insert_one({
            'order_id': 1,
            'customer': 'Test User',
            'amount': 100.00,
            'created_at': datetime.datetime.now()
        })
        
        # Verify
        collections = db.list_collection_names()
        exists = 'final_orders_test' in collections
        connector.close()
        
        if exists:
            print("    ✅ PASS - MongoDB collection creation working")
            return ("MongoDB", "✅ PASS")
        else:
            print("    ❌ FAIL - Collection not created")
            return ("MongoDB", "❌ FAIL")
    except Exception as e:
        print(f"    ❌ ERROR: {str(e)[:80]}")
        return ("MongoDB", "❌ ERROR")


def test_clickhouse():
    """Test ClickHouse connection and table creation"""
    print("\n[4] ClickHouse")
    try:
        ch_conn = DatabaseConnection.objects.get(name='Clickhouse Connection (admin)')
        connector = ClickHouseConnector(ch_conn)
        connector.connect()
        
        # Create table
        sql = """CREATE TABLE IF NOT EXISTS final_events_test (
            id UInt32,
            event String,
            user_id UInt32,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY created_at"""
        connector.connection.execute(sql)
        
        # Verify
        result = connector.connection.execute("SELECT name FROM system.tables WHERE name = 'final_events_test'")
        exists = len(result) > 0
        connector.close()
        
        if exists:
            print("    ✅ PASS - ClickHouse table creation working")
            return ("ClickHouse", "✅ PASS")
        else:
            print("    ❌ FAIL - Table not created")
            return ("ClickHouse", "❌ FAIL")
    except Exception as e:
        print(f"    ❌ ERROR: {str(e)[:80]}")
        return ("ClickHouse", "❌ ERROR")


def run_all_tests():
    """Run all database tests"""
    print("\n" + "=" * 80)
    print("🧪 FINAL DATABASE TEST - ALL 4 DATABASES".center(80))
    print("=" * 80)
    
    results = []
    results.append(test_postgresql())
    results.append(test_mysql())
    results.append(test_mongodb())
    results.append(test_clickhouse())
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY".center(80))
    print("=" * 80)
    for db, result in results:
        print(f"  {db:20} {result}")
    
    all_pass = all("✅ PASS" in r for _, r in results)
    print("\n" + ("🎉 ALL TESTS PASSED!" if all_pass else "⚠️  SOME TESTS FAILED").center(80))
    print("=" * 80 + "\n")
    
    return all_pass


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
