#!/usr/bin/env python3
"""
Quick Demo Data Populator - Creates extracted files to demonstrate RBAC
Run after: python3 populate_demo_data.py
"""

import os
import django
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from connector.models import DatabaseConnection, StoredFile, ExtractedData

print("\n" + "=" * 80)
print("📊 Creating Demo Extracted Files for RBAC Demonstration")
print("=" * 80 + "\n")

# Get or create users
try:
    admin_user = User.objects.get(username='admin')
    john_user = User.objects.get(username='john_sales')
    sarah_user = User.objects.get(username='sarah_analytics')
    mike_user = User.objects.get(username='mike_reporting')
except User.DoesNotExist:
    print("❌ Error: Demo users not found. Run populate_demo_data.py first!")
    exit(1)

# Get all connections
connections = DatabaseConnection.objects.all()

if not connections.exists():
    print("❌ Error: No database connections found. Run populate_demo_data.py first!")
    exit(1)

print(f"✅ Found {connections.count()} database connections")
print(f"✅ Found 4 demo users\n")

# Sample data for extraction
users_table = [
    {'id': 1, 'username': 'alice_admin', 'email': 'alice@company.com', 'role': 'admin', 'created': '2024-01-01'},
    {'id': 2, 'username': 'bob_user', 'email': 'bob@company.com', 'role': 'user', 'created': '2024-02-15'},
    {'id': 3, 'username': 'carol_user', 'email': 'carol@company.com', 'role': 'user', 'created': '2024-03-20'},
    {'id': 4, 'username': 'dave_admin', 'email': 'dave@company.com', 'role': 'admin', 'created': '2024-04-01'},
]

orders_table = [
    {'order_id': 1001, 'user_id': 1, 'amount': 1500.00, 'status': 'completed', 'date': '2024-04-01'},
    {'order_id': 1002, 'user_id': 2, 'amount': 2300.50, 'status': 'pending', 'date': '2024-04-05'},
    {'order_id': 1003, 'user_id': 3, 'amount': 890.25, 'status': 'completed', 'date': '2024-04-10'},
    {'order_id': 1004, 'user_id': 1, 'amount': 5600.00, 'status': 'completed', 'date': '2024-04-12'},
]

products_table = [
    {'pid': 101, 'name': 'Laptop Pro 16"', 'price': 1999.99, 'stock': 45, 'category': 'Electronics'},
    {'pid': 102, 'name': 'Mouse Wireless', 'price': 29.99, 'stock': 200, 'category': 'Accessories'},
    {'pid': 103, 'name': 'USB-C Cable 2m', 'price': 19.99, 'stock': 500, 'category': 'Cables'},
    {'pid': 104, 'name': 'Monitor 4K 32in', 'price': 599.99, 'stock': 12, 'category': 'Displays'},
]

metrics_table = [
    {'id': 1001, 'metric': 'page_views', 'value': 154200, 'timestamp': '2024-04-13T10:00:00Z', 'source': 'web'},
    {'id': 1002, 'metric': 'unique_users', 'value': 34250, 'timestamp': '2024-04-13T10:05:00Z', 'source': 'web'},
    {'id': 1003, 'metric': 'api_latency_ms', 'value': 45, 'timestamp': '2024-04-13T10:10:00Z', 'source': 'backend'},
    {'id': 1004, 'metric': 'error_rate_pct', 'value': 0.12, 'timestamp': '2024-04-13T10:15:00Z', 'source': 'backend'},
]

# Sample datasets to create
datasets = [
    ('Users Export', users_table, john_user),
    ('Orders Report', orders_table, john_user),
    ('Products Inventory', products_table, sarah_user),
    ('Analytics Metrics', metrics_table, sarah_user),
    ('Users Backup', users_table, mike_user),
    ('Monthly Orders', orders_table, mike_user),
]

print("📄 Creating extracted files...\n")

files_created = []
connection_list = list(connections)

for i, (dataset_name, data, owner) in enumerate(datasets):
    # Use different connections for each file
    connection = connection_list[i % len(connection_list)]
    
    # Create extracted data
    extracted_data = ExtractedData.objects.create(
        connection=connection,
        data=data
    )
    
    # Create stored file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"extraction_{dataset_name.replace(' ', '_')}_{owner.username}_{timestamp}.json"
    
    stored_file = StoredFile.objects.create(
        user=owner,
        extracted_data=extracted_data,
        filepath=f"/media/{filename}",
        format_type='json'
    )
    
    files_created.append(stored_file)
    print(f"  ✅ {owner.username:20} | {dataset_name:20} | {connection.db_type:10} | {len(data)} records")

print(f"\n✅ Created {len(files_created)} extracted files\n")

# Setup sharing to demonstrate RBAC
print("🔗 Setting up file sharing to demonstrate RBAC...\n")

# Get files by owner
john_files = StoredFile.objects.filter(user=john_user)
sarah_files = StoredFile.objects.filter(user=sarah_user)
mike_files = StoredFile.objects.filter(user=mike_user)

# Share john's first file with sarah and mike
if john_files.exists():
    john_file = john_files.first()
    john_file.shared_with.add(sarah_user, mike_user)
    john_file.save()
    print(f"  📤 Shared '{john_file.filepath.split('/')[-1]}'")
    print(f"     → With: sarah_analytics, mike_reporting\n")

# Share sarah's first file with mike
if sarah_files.exists():
    sarah_file = sarah_files.first()
    sarah_file.shared_with.add(mike_user)
    sarah_file.save()
    print(f"  📤 Shared '{sarah_file.filepath.split('/')[-1]}'")
    print(f"     → With: mike_reporting\n")

# Print access matrix
print("=" * 80)
print("📊 FILE ACCESS MATRIX")
print("=" * 80 + "\n")

print("JOHN'S VIEW (john_sales / john123):")
print(f"  👤 Can access {john_files.count() + 1} files:")
print(f"     ✅ {john_files.count()} own files (🔒 OWNER)")
print(f"     ✅ 1 shared file (📤 SHARED from sarah)")
print()

print("SARAH'S VIEW (sarah_analytics / sarah456):")
print(f"  👤 Can access {sarah_files.count() + 1} files:")
print(f"     ✅ {sarah_files.count()} own files (🔒 OWNER)")
print(f"     ✅ 1 shared file (📤 SHARED from john)")
print()

print("MIKE'S VIEW (mike_reporting / mike789):")
print(f"  👤 Can access {mike_files.count() + 2} files:")
print(f"     ✅ {mike_files.count()} own files (🔒 OWNER)")
print(f"     ✅ 1 shared from john (📤 SHARED)")
print(f"     ✅ 1 shared from sarah (📤 SHARED)")
print()

print("ADMIN'S VIEW (admin / admin123):")
total_files = StoredFile.objects.count()
print(f"  👑 Can access ALL {total_files} files (👑 ADMIN)")
print()

print("=" * 80)
print("✨ DEMO FILE SETUP COMPLETE!")
print("=" * 80 + "\n")

print("🌐 TEST AT: http://localhost:3000/")
print("\n📝 Try these test scenarios:\n")

print("1️⃣  LOGIN AS ADMIN")
print("   Username: admin")
print("   Password: admin123")
print("   → Should see ALL files from all users\n")

print("2️⃣  LOGIN AS JOHN SALES")
print("   Username: john_sales")
print("   Password: john123")
print("   → Should see 3 own files + 1 shared file from sarah\n")

print("3️⃣  LOGIN AS SARAH ANALYTICS")
print("   Username: sarah_analytics")
print("   Password: sarah456")
print("   → Should see 3 own files + 1 shared file from john\n")

print("4️⃣  LOGIN AS MIKE REPORTING")
print("   Username: mike_reporting")
print("   Password: mike789")
print("   → Should see 2 own files + 2 shared files (john & sarah)\n")

print("5️⃣  TRY ACCESSING UNAUTHORIZED FILE")
print("   As john_sales, try to modify a file from sarah")
print("   → Should see: ❌ Permission denied or button disabled\n")

print("=" * 80)
