"""
PostgreSQL Connection & Table Creation Test
Tests PostgreSQL connection establishment and table creation capability
"""
import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from connector.models import DatabaseConnection
from connector.connectors import PostgresConnector


def test_postgresql_connection():
    """Test PostgreSQL connection and operations"""
    print("\n" + "=" * 70)
    print("PostgreSQL Connection Test")
    print("=" * 70)
    
    try:
        # Get connection
        pg_conn = DatabaseConnection.objects.get(name='Postgresql Connection (admin)')
        print(f"\n✓ Connection config found:")
        print(f"  Host: {pg_conn.host}")
        print(f"  Port: {pg_conn.port}")
        print(f"  User: {pg_conn.username}")
        print(f"  Database: {pg_conn.database_name}")
        
        # Create connector and connect
        connector = PostgresConnector(pg_conn)
        connector.connect()
        print(f"\n✓ Connected to PostgreSQL")
        
        # List tables
        tables = connector.get_tables()
        print(f"✓ Found {len(tables)} tables:")
        for table in tables[:5]:
            print(f"  - {table}")
        if len(tables) > 5:
            print(f"  ... and {len(tables) - 5} more")
        
        # Create test table
        sql = """CREATE TABLE IF NOT EXISTS test_connection_postgresql (
            id SERIAL PRIMARY KEY,
            test_name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        cursor = connector.connection.cursor()
        cursor.execute(sql)
        connector.connection.commit()
        print(f"\n✓ Created test table: test_connection_postgresql")
        
        # Verify table exists
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_name = 'test_connection_postgresql'
        """)
        if cursor.fetchone():
            print(f"✓ Verified table exists in database")
        
        # Insert test data
        cursor.execute("""
            INSERT INTO test_connection_postgresql (test_name) 
            VALUES (%s)
        """, ("Test Entry",))
        connector.connection.commit()
        print(f"✓ Inserted test data")
        
        # Query data
        cursor.execute("SELECT COUNT(*) FROM test_connection_postgresql")
        count = cursor.fetchone()[0]
        print(f"✓ Query returned {count} row(s)")
        
        connector.close()
        print(f"\n✅ PostgreSQL connection test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ PostgreSQL connection test FAILED")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_postgresql_connection()
    sys.exit(0 if success else 1)
