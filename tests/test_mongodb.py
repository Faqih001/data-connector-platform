"""
MongoDB Connection & Collection Creation Test
Tests MongoDB connection establishment and collection creation capability
"""
import os
import sys
import django
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from connector.models import DatabaseConnection
from connector.connectors import MongoConnector


def test_mongodb_connection():
    """Test MongoDB connection and operations"""
    print("\n" + "=" * 70)
    print("MongoDB Connection Test")
    print("=" * 70)
    
    try:
        # Get connection
        mongo_conn = DatabaseConnection.objects.get(name='Mongodb Connection (admin)')
        print(f"\n✓ Connection config found:")
        print(f"  Host: {mongo_conn.host}")
        print(f"  Port: {mongo_conn.port}")
        print(f"  Database: {mongo_conn.database_name}")
        print(f"  Auth: {'Enabled' if mongo_conn.username else 'Disabled'}")
        
        # Create connector and connect
        connector = MongoConnector(mongo_conn)
        connector.connect()
        print(f"\n✓ Connected to MongoDB")
        
        # Get database
        db = connector.connection[mongo_conn.database_name]
        
        # List collections
        collections = db.list_collection_names()
        print(f"✓ Found {len(collections)} collections:")
        for coll in collections[:5]:
            print(f"  - {coll}")
        if len(collections) > 5:
            print(f"  ... and {len(collections) - 5} more")
        
        # Create test collection by inserting document
        collection = db['test_connection_mongodb']
        result = collection.insert_one({
            'test_name': 'Test Entry',
            'created_at': datetime.datetime.now()
        })
        print(f"\n✓ Created test collection: test_connection_mongodb")
        print(f"✓ Inserted test document with ID: {result.inserted_id}")
        
        # Verify collection exists
        if 'test_connection_mongodb' in db.list_collection_names():
            print(f"✓ Verified collection exists in database")
        
        # Query data
        count = collection.count_documents({})
        print(f"✓ Query returned {count} document(s)")
        
        # Find document
        doc = collection.find_one()
        if doc:
            print(f"✓ Retrieved document: {doc.get('test_name')}")
        
        connector.close()
        print(f"\n✅ MongoDB connection test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ MongoDB connection test FAILED")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)
