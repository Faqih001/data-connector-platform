#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, '/home/amir/Desktop/projects/data-connector-platform/backend')
django.setup()

from connector.models import StoredFile, DatabaseConnection, ExtractedData
from django.contrib.auth.models import User

# Count total tables
total_stored_files = StoredFile.objects.count()
total_extracted_data = ExtractedData.objects.count()

# Count by user
print("\n" + "="*70)
print("📊 DATA VERIFICATION REPORT")
print("="*70)

users = User.objects.filter(username__in=['john_sales', 'sarah_analytics', 'mike_reporting', 'admin'])
for user in users:
    conns = DatabaseConnection.objects.filter(user=user)
    files = StoredFile.objects.filter(user=user)
    extracted = ExtractedData.objects.filter(connection__user=user)
    print(f"\n👤 {user.username} {'(Admin)' if user.is_staff else ''}")
    print(f"   Connections: {conns.count()}")
    print(f"   Stored Files: {files.count()}")
    print(f"   Extracted Data Records: {extracted.count()}")
    
    # Break down by connection type
    for conn in conns:
        db_type = conn.db_type
        files_for_conn = StoredFile.objects.filter(extracted_data__connection=conn)
        print(f"      • {db_type:12} → {files_for_conn.count()} tables")

print(f"\n{'='*70}")
print(f"📈 TOTALS:")
print(f"{'='*70}")
print(f"   Total Connections: {DatabaseConnection.objects.count()} (expected: 16 = 4 users × 4 DB types)")
print(f"   Total Stored Files: {total_stored_files} (expected: 112 = 4 users × 4 DB types × 7 tables)")
print(f"   Total Extracted Data: {total_extracted_data} (expected: 112)")
print(f"\n✅ Status: {'PASS' if total_stored_files == 112 else 'FAIL - Missing tables!'}")
print("="*70 + "\n")
