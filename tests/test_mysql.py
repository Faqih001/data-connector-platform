"""
MySQL Connection & Table Creation Test
Tests MySQL connection establishment and table creation capability
"""
import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from connector.models import DatabaseConnection
from connector.connectors import MySQLConnector


def test_mysql_connection():
    """Test MySQL connection and operations"""
    print("\n" + "=" * 70)
    print("MySQL Connection Test")
    print("=" * 70)
    
    try:
        # Get connection
        mysql_conn = DatabaseConnection.objects.get(name='Mysql Connection (admin)')
        print(f"\n✓ Connection config found:")
        print(f"  Host: {mysql_conn.host}")
        print(f"  Port: {mysql_conn.port}")
        print(f"  User: {mysql_conn.username}")
        print(f"  Database: {mysql_conn.database_name}")
        
        # Create connector and connect
        connector = MySQLConnector(mysql_conn)
        connector.connect()
        print(f"\n✓ Connected to MySQL")
        
        # List tables
        tables = connector.get_tables()
        print(f"✓ Found {len(tables)} tables:")
        for table in tables[:5]:
            print(f"  - {table}")
        if len(tables) > 5:
            print(f"  ... and {len(tables) - 5} more")
        
        # Create test table
        sql = """CREATE TABLE IF NOT EXISTS test_connection_mysql (
            id INT AUTO_INCREMENT PRIMARY KEY,
            test_name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        cursor = connector.connection.cursor()
        cursor.execute(sql)
        connector.connection.commit()
        print(f"\n✓ Created test table: test_connection_mysql")
        
        # Verify table exists
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_name = 'test_connection_mysql' AND table_schema = DATABASE()
        """)
        if cursor.fetchone():
            print(f"✓ Verified table exists in database")
        
        # Insert test data
        cursor.execute("""
            INSERT INTO test_connection_mysql (test_name) 
            VALUES (%s)
        """, ("Test Entry",))
        connector.connection.commit()
        print(f"✓ Inserted test data")
        
        # Query data
        cursor.execute("SELECT COUNT(*) FROM test_connection_mysql")
        count = cursor.fetchone()[0]
        print(f"✓ Query returned {count} row(s)")
        
        connector.close()
        print(f"\n✅ MySQL connection test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ MySQL connection test FAILED")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_mysql_connection()
    sys.exit(0 if success else 1)
