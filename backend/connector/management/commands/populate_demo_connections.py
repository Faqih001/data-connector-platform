"""
Django management command to populate demo database connections.
Usage: python manage.py populate_demo_connections
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from connector.models import DatabaseConnection


class Command(BaseCommand):
    help = 'Create demo database connections for testing'

    def handle(self, *args, **options):
        # Get admin user
        admin_user = User.objects.filter(username='admin').first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('✗ Admin user not found. Please create admin user first.'))
            return

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
                self.stdout.write(self.style.SUCCESS(f'✓ Connection already exists: {conn_data["name"]}'))
                continue

            # Create connection
            try:
                DatabaseConnection.objects.create(
                    user=admin_user,
                    **conn_data
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Created connection: {conn_data["name"]}'))
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to create connection {conn_data["name"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Demo connections setup complete! {created_count} new connections created.'))
