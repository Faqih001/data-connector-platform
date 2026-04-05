from django.test import TestCase
from .models import DatabaseConnection

class DatabaseConnectionTest(TestCase):
    def test_create_connection(self):
        conn = DatabaseConnection.objects.create(
            name="Test PG",
            db_type="postgres",
            host="localhost",
            port=5432,
            username="user",
            password="password",
            database="testdb"
        )
        self.assertEqual(conn.name, "Test PG")

class DatabaseConnectionModelTest(TestCase):
    def test_create_database_connection(self):
        connection = DatabaseConnection.objects.create(
            name="Test PG",
            db_type="postgresql",
            host="localhost",
            port=5432,
            username="user",
            password="password",
            database_name="testdb"
        )
        self.assertEqual(connection.name, "Test PG")
        self.assertEqual(connection.db_type, "postgresql")

