"""
ClickHouse Connection & Table Creation Test
Tests ClickHouse connection establishment and table creation capability
"""
import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from connector.models import DatabaseConnection
from connector.connectors import ClickHouseConnector


def test_clickhouse_connection():
    """Test ClickHouse connection and operations"""
    print("\n" + "=" * 70)
    print("ClickHouse Connection Test")
    print("=" * 70)
    
    try:
        # Get connection
        ch_conn = DatabaseConnection.objects.get(name='Clickhouse Connection (admin)')
        print(f"\n✓ Connection config found:")
        print(f"  Host: {ch_conn.host}")
        print(f"  Port: {ch_conn.port}")
        print(f"  User: {ch_conn.username}")
        print(f"  Database: {ch_conn.database_name}")
        
        # Create connector and connect
        connector = ClickHouseConnector(ch_conn)
        connector.connect()
        print(f"\n✓ Connected to ClickHouse")
        
        # List tables
        tables = connector.get_tables()
        print(f"✓ Found {len(tables)} tables:")
        for table in tables[:5]:
            print(f"  - {table}")
        if len(tables) > 5:
            print(f"  ... and {len(tables) - 5} more")
        
        # Create test table
        sql = """CREATE TABLE IF NOT EXISTS test_connection_clickhouse (
            id UInt32,
            test_name String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY created_at"""
        connector.connection.execute(sql)
        print(f"\n✓ Created test table: test_connection_clickhouse")
        
        # Verify table exists
        result = connector.connection.execute("""
            SELECT name FROM system.tables 
            WHERE name = 'test_connection_clickhouse'
        """)
        if len(result) > 0:
            print(f"✓ Verified table exists in database")
        
        # Insert test data
        connector.connection.execute("""
            INSERT INTO test_connection_clickhouse (id, test_name) 
            VALUES (1, 'Test Entry')
        """)
        print(f"✓ Inserted test data")
        
        # Query data
        result = connector.connection.execute("""
            SELECT COUNT(*) FROM test_connection_clickhouse
        """)
        count = result[0][0] if result else 0
        print(f"✓ Query returned {count} row(s)")
        
        connector.close()
        print(f"\n✅ ClickHouse connection test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ ClickHouse connection test FAILED")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_clickhouse_connection()
    sys.exit(0 if success else 1)
