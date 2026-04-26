#!/usr/bin/env python3
"""
Populate demo database connections for easy testing.
This script creates pre-configured connections to each database type.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Add current directory to path (we're in /app in Docker, backend code is in /app)
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

django.setup()

from connector.models import DatabaseConnection, User
from django.contrib.auth.models import User as DjangoUser

def create_demo_connections():
    """Create demo database connections."""
    
    # Get admin user
    admin_user = DjangoUser.objects.filter(username='admin').first()
    if not admin_user:
        print("✗ Admin user not found. Please create admin user first.")
        return False
    
    # Define demo connections with Docker service names
    demo_connections = [
        {
            'name': 'Demo PostgreSQL (Docker)',
            'db_type': 'postgresql',
            'host': 'db',
            'port': 5432,
            'username': 'user',
            'password': 'password',
            'database_name': 'dataconnector',
        },
        {
            'name': 'Demo MySQL (Docker)',
            'db_type': 'mysql',
            'host': 'mysql',
            'port': 3306,
            'username': 'user',
            'password': 'password',
            'database_name': 'testdb',
        },
        {
            'name': 'Demo MongoDB (Docker)',
            'db_type': 'mongodb',
            'host': 'mongo',
            'port': 27017,
            'username': '',
            'password': '',
            'database_name': 'test_db',
        },
        {
            'name': 'Demo ClickHouse (Docker)',
            'db_type': 'clickhouse',
            'host': 'clickhouse',
            'port': 9000,
            'username': 'default',
            'password': '',
            'database_name': 'default',
        },
    ]
    
    created_count = 0
    for conn_data in demo_connections:
        # Check if connection already exists
        existing = DatabaseConnection.objects.filter(
            name=conn_data['name'],
            user=admin_user
        ).first()
        
        if existing:
            print(f"✓ Connection already exists: {conn_data['name']}")
            continue
        
        # Create connection
        try:
            connection = DatabaseConnection.objects.create(
                user=admin_user,
                **conn_data
            )
            print(f"✓ Created connection: {conn_data['name']}")
            created_count += 1
        except Exception as e:
            print(f"✗ Failed to create connection {conn_data['name']}: {str(e)}")
    
    return created_count > 0 or len(demo_connections) > 0

if __name__ == '__main__':
    try:
        success = create_demo_connections()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        sys.exit(1)
