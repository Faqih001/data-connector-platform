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
# STEP 2: CREATE DEMO DATABASE CONNECTIONS
# ============================================================================
print("\n📡 STEP 2: Creating Demo Database Connections...")
print("-" * 80)

demo_connections = [
    # PostgreSQL - Sales Database
    {
        'name': 'PostgreSQL Sales DB',
        'db_type': 'postgresql',
        'host': 'localhost',
        'port': 5432,
        'username': 'sales_user',
        'password': 'sales_pass_123',
        'database_name': 'sales_database',
    },
    {
        'name': 'PostgreSQL Users Database',
        'db_type': 'postgresql',
        'host': '192.168.1.100',
        'port': 5432,
        'username': 'postgres_admin',
        'password': 'postgres_secure_456',
        'database_name': 'users_db',
    },
    {
        'name': 'PostgreSQL Analytics',
        'db_type': 'postgresql',
        'host': 'analytics.company.com',
        'port': 5432,
        'username': 'analytics_read',
        'password': 'analytics_readonly_789',
        'database_name': 'analytics_prod',
    },
    # MySQL - Customer Database
    {
        'name': 'MySQL Customer DB',
        'db_type': 'mysql',
        'host': 'mysql.company.local',
        'port': 3306,
        'username': 'customer_user',
        'password': 'customer_pass_123',
        'database_name': 'customers',
    },
    {
        'name': 'MySQL Inventory System',
        'db_type': 'mysql',
        'host': 'inventory.prod.local',
        'port': 3306,
        'username': 'inventory_app',
        'password': 'inv_app_456',
        'database_name': 'inventory_db',
    },
    {
        'name': 'MySQL Financial Data',
        'db_type': 'mysql',
        'host': 'finance-server.internal',
        'port': 3306,
        'username': 'finance_read',
        'password': 'fin_secure_789',
        'database_name': 'financial_records',
    },
    # MongoDB - Event Logs
    {
        'name': 'MongoDB Event Logs',
        'db_type': 'mongodb',
        'host': 'mongodb.cluster.io',
        'port': 27017,
        'username': 'mongo_user',
        'password': 'mongo_pass_123',
        'database_name': 'eventlogs',
    },
    {
        'name': 'MongoDB User Activity',
        'db_type': 'mongodb',
        'host': 'auth-mongo.internal',
        'port': 27017,
        'username': 'activity_monitor',
        'password': 'activity_456',
        'database_name': 'user_activity',
    },
    {
        'name': 'MongoDB Session Store',
        'db_type': 'mongodb',
        'host': 'session-db.company.com',
        'port': 27017,
        'username': 'session_mgr',
        'password': 'session_pass_789',
        'database_name': 'sessions',
    },
    # ClickHouse - Metrics/Analytics
    {
        'name': 'ClickHouse Metrics',
        'db_type': 'clickhouse',
        'host': 'metrics.analytics.com',
        'port': 9000,
        'username': 'metrics_read',
        'password': 'metrics_123',
        'database_name': 'metrics_database',
    },
]

connections_map = {}
for conn_data in demo_connections:
    conn, created = DatabaseConnection.objects.get_or_create(
        name=conn_data['name'],
        defaults={
            'db_type': conn_data['db_type'],
            'host': conn_data['host'],
            'port': conn_data['port'],
            'username': conn_data['username'],
            'password': conn_data['password'],
            'database_name': conn_data['database_name'],
        }
    )
    connections_map[conn.name] = conn
    status = "✅ Created" if created else "⚠️  Existing"
    print(f"  {status}: {conn.name}")
    print(f"            → {conn.db_type}://{conn.host}:{conn.port}/{conn.database_name}")

# ============================================================================
# STEP 3: CREATE DEMO EXTRACTED DATA & STORED FILES
# ============================================================================
print("\n📊 STEP 3: Creating Demo Extracted Data & Files...")
print("-" * 80)

# Sample data for different databases
sample_data = {
    'users': [
        {'id': 1, 'username': 'john_doe', 'email': 'john@example.com', 'role': 'admin', 'created_at': '2024-01-15'},
        {'id': 2, 'username': 'jane_smith', 'email': 'jane@example.com', 'role': 'user', 'created_at': '2024-02-20'},
        {'id': 3, 'username': 'bob_wilson', 'email': 'bob@example.com', 'role': 'user', 'created_at': '2024-03-10'},
    ],
    'orders': [
        {'order_id': 1001, 'customer_id': 1, 'amount': 1500.00, 'status': 'completed', 'date': '2024-04-01'},
        {'order_id': 1002, 'customer_id': 2, 'amount': 2300.50, 'status': 'pending', 'date': '2024-04-05'},
        {'order_id': 1003, 'customer_id': 3, 'amount': 890.25, 'status': 'completed', 'date': '2024-04-10'},
    ],
    'products': [
        {'product_id': 101, 'name': 'Laptop Pro', 'price': 999.99, 'stock': 45, 'category': 'Electronics'},
        {'product_id': 102, 'name': 'Mouse Wireless', 'price': 29.99, 'stock': 200, 'category': 'Accessories'},
        {'product_id': 103, 'name': 'USB Cable 2m', 'price': 9.99, 'stock': 500, 'category': 'Cables'},
    ],
    'metrics': [
        {'metric_id': 1, 'name': 'page_views', 'value': 15420, 'timestamp': '2024-04-13T10:00:00'},
        {'metric_id': 2, 'name': 'active_users', 'value': 342, 'timestamp': '2024-04-13T10:05:00'},
        {'metric_id': 3, 'name': 'api_latency_ms', 'value': 45, 'timestamp': '2024-04-13T10:10:00'},
    ],
}

files_created = []

# Create extracted data for john_sales (owner)
print("\n  👤 Creating files for john_sales (file owner):")
for conn_name, data_list in sample_data.items():
    if conn_name in connections_map:
        extracted_data = ExtractedData.objects.create(
            connection=connections_map[conn_name],
            data=data_list
        )
        stored_file = StoredFile.objects.create(
            user=users_map['john_sales'],
            extracted_data=extracted_data,
            filepath=f"/media/extraction_{conn_name}_john_{datetime.now().strftime('%Y%m%d%H%M%S')}.json",
            format_type='json'
        )
        files_created.append(('john_sales', stored_file))
        print(f"    ✅ {conn_name} data extraction")

# Create extracted data for sarah_analytics (will be shared)
print("\n  👤 Creating files for sarah_analytics:")
for conn_name, data_list in sample_data.items():
    if conn_name in connections_map:
        extracted_data = ExtractedData.objects.create(
            connection=connections_map[conn_name],
            data=data_list
        )
        stored_file = StoredFile.objects.create(
            user=users_map['sarah_analytics'],
            extracted_data=extracted_data,
            filepath=f"/media/extraction_{conn_name}_sarah_{datetime.now().strftime('%Y%m%d%H%M%S')}.json",
            format_type='json'
        )
        files_created.append(('sarah_analytics', stored_file))
        print(f"    ✅ {conn_name} data extraction")

# Create extracted data for mike_reporting
print("\n  👤 Creating files for mike_reporting:")
for conn_name, data_list in sample_data.items():
    if conn_name in connections_map:
        extracted_data = ExtractedData.objects.create(
            connection=connections_map[conn_name],
            data=data_list
        )
        stored_file = StoredFile.objects.create(
            user=users_map['mike_reporting'],
            extracted_data=extracted_data,
            filepath=f"/media/extraction_{conn_name}_mike_{datetime.now().strftime('%Y%m%d%H%M%S')}.json",
            format_type='json'
        )
        files_created.append(('mike_reporting', stored_file))
        print(f"    ✅ {conn_name} data extraction")

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

print("\n📋 SUMMARY:")
print(f"  ✅ Users Created: {len(demo_users)}")
print(f"  ✅ Database Connections: {len(demo_connections)}")
print(f"  ✅ Extracted Files: {len(files_created)}")
print(f"  ✅ Shared Files: Multiple (see access rules below)")

print("\n👥 USER CREDENTIALS:")
for user in demo_users:
    print(f"  • {user['username']:20} | Password: {user['password']:15} | {user['email']}")

print("\n🔐 ACCESS RULES DEMONSTRATION:")
print("  ADMIN (admin):")
print("    ✅ Can see ALL files from ALL users")
print("    ✅ Can modify ANY file")
print("    ✅ Can share/unshare ANY file")
print("    ✅ Full system access")
print("\n  SALES USER (john_sales):")
print("    ✅ Can see his own files (john_sales_*.json)")
print("    ✅ Can see files shared with him (2 files from sarah)")
print("    ❌ Cannot see sarah's other files")
print("    ✅ Can share his files with others")
print("\n  ANALYTICS USER (sarah_analytics):")
print("    ✅ Can see her own files (sarah_analytics_*.json)")
print("    ✅ Can see files shared with her (2 files from john)")
print("    ✅ Can see files shared with mike (shares with mike)")
print("    ❌ Cannot see john's other files")
print("\n  REPORTING USER (mike_reporting):")
print("    ✅ Can see his own files (mike_reporting_*.json)")
print("    ✅ Can see file shared with him (1 file from sarah)")
print("    ❌ Cannot see other users' files")

print("\n🌐 ACCESS AT UI:")
print("  http://localhost:3000/")
print("    • Login with any user credentials above")
print("    • Each user will see different files based on RBAC rules")
print("    • Files show access level badges: 👑 Admin | 🔒 Owner | 📤 Shared")

print("\n📊 DATABASE CONNECTIONS AVAILABLE:")
for i, conn_data in enumerate(demo_connections, 1):
    print(f"  {i}. {conn_data['name']}")
    print(f"     → {conn_data['db_type']}://{conn_data['username']}@{conn_data['host']}:{conn_data['port']}/{conn_data['database_name']}")

print("\n" + "=" * 80)
