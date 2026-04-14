#!/usr/bin/env python3
"""
Demo Data Population Script
Demonstrates File Access Rules and Role-Based Access Control
for Data Connector Platform
"""

import os
import django
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from django.conf import settings
from connector.models import DatabaseConnection, StoredFile, ExtractedData

print("=" * 80)
print("🚀 Data Connector Platform - Demo Data Population")
print("=" * 80)

# ============================================================================
# STEP 1: CREATE DEMO USERS
# ============================================================================
print("\n📝 STEP 1: Creating Demo Users...")
print("-" * 80)

demo_users = [
    {'username': 'admin', 'password': 'admin123', 'is_staff': True, 'is_superuser': True, 'email': 'admin@platform.local'},
    {'username': 'john_sales', 'password': 'john123', 'is_staff': False, 'is_superuser': False, 'email': 'john@company.com'},
    {'username': 'sarah_analytics', 'password': 'sarah456', 'is_staff': False, 'is_superuser': False, 'email': 'sarah@company.com'},
    {'username': 'mike_reporting', 'password': 'mike789', 'is_staff': False, 'is_superuser': False, 'email': 'mike@company.com'},
]

users_map = {}
for user_data in demo_users:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'is_staff': user_data['is_staff'],
            'is_superuser': user_data['is_superuser'],
        }
    )
    user.set_password(user_data['password'])
    user.save()
    users_map[user_data['username']] = user
    status = "✅ Created" if created else "⚠️  Existing"
    print(f"  {status}: {user.username} ({user.email})")

# ============================================================================
# STEP 2: CREATE DEMO DATABASE CONNECTIONS (Per User - All 4 Database Types)
# ============================================================================
print("\n📡 STEP 2: Creating Demo Database Connections for Each User...")
print("-" * 80)

# Define connection templates for each database type
connection_templates = {
    'postgresql': {
        'db_type': 'postgresql',
        'host': 'localhost',
        'port': 5432,
        'database_name': 'test_db',
    },
    'mysql': {
        'db_type': 'mysql',
        'host': 'localhost',
        'port': 3306,
        'database_name': 'test_database',
    },
    'mongodb': {
        'db_type': 'mongodb',
        'host': 'localhost',
        'port': 27017,
        'database_name': 'test_mongodb',
    },
    'clickhouse': {
        'db_type': 'clickhouse',
        'host': 'localhost',
        'port': 9000,
        'database_name': 'default',
    },
}

# Define credentials for each database type
connection_credentials = {
    'postgresql': {
        'username': 'postgres',
        'password': 'postgres',
    },
    'mysql': {
        'username': 'root',
        'password': 'root',
    },
    'mongodb': {
        'username': 'admin',
        'password': 'admin',
    },
    'clickhouse': {
        'username': 'default',
        'password': 'default',
    },
}

connections_map = {}

# Create connections for each user (one of each database type)
for username, user in users_map.items():
    print(f"\n  👤 Creating connections for {username}:")
    
    for db_type, credentials in connection_credentials.items():
        template = connection_templates[db_type]
        conn_name = f"{db_type.capitalize()} Connection ({username})"
        
        conn, created = DatabaseConnection.objects.get_or_create(
            user=user,
            name=conn_name,
            defaults={
                'db_type': template['db_type'],
                'host': template['host'],
                'port': template['port'],
                'username': credentials['username'],
                'password': credentials['password'],
                'database_name': template['database_name'],
            }
        )
        
        key = f"{username}_{db_type}"
        connections_map[key] = conn
        status = "✅ Created" if created else "⚠️  Existing"
        print(f"    {status}: {conn_name}")
        print(f"              → {db_type}://{template['host']}:{template['port']}/{template['database_name']}")

# ============================================================================
# STEP 3: CREATE DEMO EXTRACTED DATA & STORED FILES (Per User, All DB Types)
# ============================================================================
print("\n📊 STEP 3: Creating Demo Extracted Data & Files for Each User...")
print("-" * 80)

# Sample data for different database types - 7 tables each
sample_data_by_db = {
    'postgresql': {
        'users': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}],
        'products': [{'id': 101, 'name': 'Laptop'}, {'id': 102, 'name': 'Mouse'}],
        'orders': [{'id': 1001, 'product_id': 101}, {'id': 1002, 'product_id': 102}],
        'inventory': [{'id': 1, 'product_id': 101, 'stock': 50}],
        'customers': [{'id': 1, 'name': 'Customer A'}, {'id': 2, 'name': 'Customer B'}],
        'employees': [{'id': 1, 'name': 'Employee X'}, {'id': 2, 'name': 'Employee Y'}],
        'departments': [{'id': 1, 'name': 'Sales'}, {'id': 2, 'name': 'Support'}],
    },
    'mysql': {
        'clients': [{'id': 1, 'name': 'Client 1'}, {'id': 2, 'name': 'Client 2'}],
        'invoices': [{'id': 201, 'client_id': 1, 'amount': 500}],
        'payments': [{'id': 301, 'invoice_id': 201, 'amount': 500}],
        'suppliers': [{'id': 1, 'name': 'Supplier Z'}],
        'purchase_orders': [{'id': 401, 'supplier_id': 1}],
        'shipments': [{'id': 501, 'order_id': 401}],
        'locations': [{'id': 1, 'city': 'New York'}, {'id': 2, 'city': 'London'}],
    },
    'mongodb': {
        'articles': [{'_id': 'a1', 'title': 'Mongo Intro'}],
        'comments': [{'_id': 'c1', 'article_id': 'a1', 'text': 'Great!'}],
        'authors': [{'_id': 'au1', 'name': 'John Doe'}],
        'sessions': [{'_id': 's1', 'user_id': 'au1'}],
        'logs': [{'_id': 'l1', 'event': 'login'}],
        'media': [{'_id': 'm1', 'type': 'image'}],
        'tags': [{'_id': 't1', 'name': 'database'}],
    },
    'clickhouse': {
        'page_views': [{'id': 1, 'url': '/home'}],
        'events': [{'id': 1, 'name': 'click'}],
        'users_ch': [{'id': 1, 'name': 'CH User'}],
        'sessions_ch': [{'id': 1, 'user_id': 1}],
        'performance': [{'id': 1, 'metric': 'load_time', 'value': 1.2}],
        'errors': [{'id': 1, 'message': 'Error 500'}],
        'campaigns': [{'id': 1, 'name': 'Summer Sale'}],
    },
}

files_created = []

# Create extracted data for each user with all 4 database types
for username, user in users_map.items():
    print(f"\n  👤 Creating data extractions for {username}:")
    
    for db_type, tables in sample_data_by_db.items():
        conn_key = f"{username}_{db_type}"
        
        if conn_key in connections_map:
            conn = connections_map[conn_key]
            
            # Create one file per table (7 tables per DB type)
            for table_name, sample_data in tables.items():
                # Create extracted data
                extracted_data = ExtractedData.objects.create(
                    connection=conn,
                    data=sample_data
                )
                
                # Generate base filename without timestamp
                base_filename = f"extraction_{db_type}_{table_name}_{username}"
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                
                # Create stored file linked to this extraction with new fields
                filepath = os.path.join(settings.MEDIA_ROOT, f"{base_filename}_{timestamp}.json")
                stored_file = StoredFile.objects.create(
                    user=user,
                    extracted_data=extracted_data,
                    filepath=filepath,
                    format_type='json',
                    base_filename=base_filename,
                    table_name=table_name,
                    connection_name=conn.name
                )
                files_created.append((username, stored_file))
                print(f"    ✅ {db_type.upper()} - Table: {table_name} extraction created")

# ============================================================================
# STEP 4: SET UP FILE SHARING TO DEMONSTRATE RBAC
# ============================================================================
print("\n🔗 STEP 4: Setting Up File Sharing (RBAC Demo)...")
print("-" * 80)

# Share some of john's files with sarah
print("\n  📤 Sharing john_sales files with sarah_analytics:")
john_files = [f for owner, f in files_created if owner == 'john_sales']
for i, file_obj in enumerate(john_files[:2]):  # Share first 2 files
    file_obj.shared_with.add(users_map['sarah_analytics'])
    file_obj.save()
    print(f"    ✅ Shared: {file_obj.filepath.split('/')[-1]}")

# Share some of sarah's files with mike
print("\n  📤 Sharing sarah_analytics files with mike_reporting:")
sarah_files = [f for owner, f in files_created if owner == 'sarah_analytics']
for i, file_obj in enumerate(sarah_files[:1]):  # Share first file
    file_obj.shared_with.add(users_map['mike_reporting'])
    file_obj.save()
    print(f"    ✅ Shared: {file_obj.filepath.split('/')[-1]}")

# ============================================================================
# STEP 5: SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("✨ DEMO DATA POPULATION COMPLETE!")
print("=" * 80)

total_connections = len([k for k in connections_map.keys()])
print("\n📋 SUMMARY:")
print(f"  ✅ Users Created: {len(demo_users)}")
print(f"  ✅ Database Connections (Per User): 4 types × {len(users_map)} users = {total_connections} connections")
print(f"  ✅ Extracted Files: {len(files_created)} (4 files per user)")
print(f"  ✅ Shared Files: Multiple (see access rules below)")

print("\n👥 USER CREDENTIALS & CONNECTION ASSIGNMENTS:")
for user in demo_users:
    print(f"  • {user['username']:20} | Password: {user['password']:15}")
    print(f"    └─ Database Connections:")
    for db_type in ['postgresql', 'mysql', 'mongodb', 'clickhouse']:
        key = f"{user['username']}_{db_type}"
        if key in connections_map:
            print(f"       ✅ {db_type.upper()}")

print("\n🔐 ACCESS RULES DEMONSTRATION (Per-User Filtering):")
print("  ADMIN (admin):")
print("    ✅ Can see ALL connections from ALL users")
print("    ✅ Can see ALL files from ALL users")
print("    ✅ Can modify ANY file")
print("    ✅ Can share/unshare ANY file")
print("    ✅ Full system access")
print("\n  SALES USER (john_sales):")
print("    ✅ Can see ONLY his own connections (4: PostgreSQL, MySQL, MongoDB, ClickHouse)")
print("    ✅ Can see his own files (4 data extractions from each database type)")
print("    ✅ Can see files shared with him (if any)")
print("    ❌ Cannot see other users' connections")
print("    ❌ Cannot see other users' files (unless shared)")
print("\n  ANALYTICS USER (sarah_analytics):")
print("    ✅ Can see ONLY her own connections (4: PostgreSQL, MySQL, MongoDB, ClickHouse)")
print("    ✅ Can see her own files (4 data extractions from each database type)")
print("    ✅ Can see files shared with her (if any)")
print("    ❌ Cannot see other users' connections")
print("    ❌ Cannot see other users' files (unless shared)")
print("\n  REPORTING USER (mike_reporting):")
print("    ✅ Can see ONLY his own connections (4: PostgreSQL, MySQL, MongoDB, ClickHouse)")
print("    ✅ Can see his own files (4 data extractions from each database type)")
print("    ✅ Can see files shared with him (if any)")
print("    ❌ Cannot see other users' connections")
print("    ❌ Cannot see other users' files (unless shared)")

print("\n🌐 ACCESS AT UI:")
print("  http://localhost:3000/")
print("    • Login with any user credentials above")
print("    • Connections dropdown will show ONLY that user's 4 connections")
print("    • File list will show ONLY that user's files + shared files")
print("    • Each user starts with complete demo data for all 4 database types")

print("\n📊 DATABASE TYPES AVAILABLE TO EACH USER:")
for db_type in ['postgresql', 'mysql', 'mongodb', 'clickhouse']:
    creds = connection_credentials[db_type]
    template = connection_templates[db_type]
    print(f"  • {db_type.upper()}")
    print(f"    └─ {template['host']}:{template['port']}/{template['database_name']}")
    print(f"    └─ Credentials: {creds['username']} / {creds['password']}")

print("\n" + "=" * 80)
