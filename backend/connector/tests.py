from django.test import TestCase
from django.contrib.auth.models import User
from connector.models import DatabaseConnection
from connector.connectors import get_connector, BaseConnector
from django.core.exceptions import ValidationError
import json


class DatabaseConnectionTest(TestCase):
    """Basic database connection tests"""
    
    def test_create_connection(self):
        """Test basic connection creation"""
        conn = DatabaseConnection.objects.create(
            name="Test PG",
            db_type="postgresql",
            host="localhost",
            port=5432,
            username="user",
            password="password",
            database="testdb"
        )
        self.assertEqual(conn.name, "Test PG")
        self.assertEqual(conn.db_type, "postgresql")

    def test_connection_requires_name(self):
        """Test connection requires a name"""
        with self.assertRaises(Exception):
            DatabaseConnection.objects.create(
                db_type="postgresql",
                host="localhost",
                port=5432,
                username="user",
                password="password",
                database="testdb"
            )


class DatabaseConnectionModelTest(TestCase):
    """Extended database connection model tests"""
    
    def test_create_database_connection(self):
        """Test creating database connection with all fields"""
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
        self.assertEqual(connection.host, "localhost")
        self.assertEqual(connection.port, 5432)
        self.assertEqual(connection.username, "user")
        self.assertEqual(connection.database_name, "testdb")

    def test_all_database_types_supported(self):
        """Test all supported database types"""
        supported_types = ['postgresql', 'mysql', 'mongodb', 'clickhouse']
        
        for db_type in supported_types:
            conn = DatabaseConnection.objects.create(
                name=f"Test {db_type}",
                db_type=db_type,
                host="localhost",
                port=5432,
                username="user",
                password="password",
                database_name="testdb"
            )
            self.assertEqual(conn.db_type, db_type)
            self.assertEqual(conn.name, f"Test {db_type}")

    def test_connection_with_owner(self):
        """Test connection can be owned by user"""
        user = User.objects.create_user(username='testuser', password='password')
        connection = DatabaseConnection.objects.create(
            name="Test PG",
            owner=user,
            db_type="postgresql",
            host="localhost",
            port=5432,
            username="user",
            password="password",
            database_name="testdb"
        )
        self.assertEqual(connection.owner, user)


class ConnectorFactoryTest(TestCase):
    """Tests for connector factory pattern"""
    
    def test_get_postgresql_connector(self):
        """Test getting PostgreSQL connector"""
        connector = get_connector('postgresql')
        self.assertIsNotNone(connector)
        # Should have required methods
        self.assertTrue(hasattr(connector, 'connect'))
        self.assertTrue(hasattr(connector, 'fetch_batch'))
        self.assertTrue(hasattr(connector, 'close'))

    def test_get_mysql_connector(self):
        """Test getting MySQL connector"""
        connector = get_connector('mysql')
        self.assertIsNotNone(connector)

    def test_get_mongodb_connector(self):
        """Test getting MongoDB connector"""
        connector = get_connector('mongodb')
        self.assertIsNotNone(connector)

    def test_get_clickhouse_connector(self):
        """Test getting ClickHouse connector"""
        connector = get_connector('clickhouse')
        self.assertIsNotNone(connector)

    def test_connector_is_base_type(self):
        """Test all connectors are BaseConnector instances"""
        for db_type in ['postgresql', 'mysql', 'mongodb', 'clickhouse']:
            connector = get_connector(db_type)
            self.assertIsInstance(connector, BaseConnector)

    def test_invalid_connector_type(self):
        """Test requesting invalid connector raises error"""
        with self.assertRaises(Exception):
            get_connector('invalid_type')


class PasswordEncryptionTest(TestCase):
    """Tests for password encryption functionality"""
    
    def test_password_encryption_simple(self):
        """Test password is encrypted on save"""
        connection = DatabaseConnection.objects.create(
            name="Test Connection",
            db_type="postgresql",
            host="localhost",
            port=5432,
            username="testuser",
            password="mysecretpassword",
            database_name="testdb"
        )
        
        # Encrypted password should not equal plain text
        self.assertNotEqual(connection.password, "mysecretpassword")
        
        # But should decrypt correctly
        self.assertEqual(connection.decrypted_password, "mysecretpassword")

    def test_password_encryption_persistence(self):
        """Test encrypted password persists across saves"""
        connection = DatabaseConnection.objects.create(
            name="Test Connection",
            db_type="postgresql",
            host="localhost",
            port=5432,
            username="testuser",
            password="mysecretpassword",
            database_name="testdb"
        )
        
        original_encrypted = connection.password
        
        # Reload from database
        reloaded = DatabaseConnection.objects.get(id=connection.id)
        
        # Encrypted should be same
        self.assertEqual(reloaded.password, original_encrypted)
        # Decrypted should be same
        self.assertEqual(reloaded.decrypted_password, "mysecretpassword")

    def test_password_special_characters(self):
        """Test password with special characters is encrypted/decrypted"""
        special_password = "P@ssw0rd!$%^&*()_+-=[]{}|;:',.<>?/`~"
        connection = DatabaseConnection.objects.create(
            name="Test Connection",
            db_type="postgresql",
            host="localhost",
            port=5432,
            username="testuser",
            password=special_password,
            database_name="testdb"
        )
        
        self.assertEqual(connection.decrypted_password, special_password)


class DataValidationTest(TestCase):
    """Tests for data validation in models"""
    
    def test_port_validation(self):
        """Test port must be valid integer"""
        # Port should be a valid integer
        connection = DatabaseConnection.objects.create(
            name="Test",
            db_type="postgresql",
            host="localhost",
            port=5432,  # Valid port
            username="user",
            password="pass",
            database_name="db"
        )
        self.assertEqual(connection.port, 5432)

    def test_host_validation(self):
        """Test host can be filesystem path or network address"""
        hosts = ['localhost', '127.0.0.1', 'db.example.com', '/var/run/socket']
        
        for host in hosts:
            connection = DatabaseConnection.objects.create(
                name=f"Test {host}",
                db_type="postgresql",
                host=host,
                port=5432,
                username="user",
                password="pass",
                database_name="db"
            )
            self.assertEqual(connection.host, host)

    def test_database_name_with_special_chars(self):
        """Test database name can include special characters"""
        special_names = ['test_db', 'test-db', 'test.db', 'test$db']
        
        for db_name in special_names:
            connection = DatabaseConnection.objects.create(
                name=f"Test {db_name}",
                db_type="postgresql",
                host="localhost",
                port=5432,
                username="user",
                password="pass",
                database_name=db_name
            )
            self.assertEqual(connection.database_name, db_name)

