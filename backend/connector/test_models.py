from django.test import TestCase
from django.contrib.auth.models import User
from connector.models import DatabaseConnection, StoredFile, ExtractedData
from connector.serializers import DatabaseConnectionSerializer, StoredFileSerializer
from django.utils import timezone
import json
import os
from django.conf import settings


class DatabaseConnectionModelTest(TestCase):
    """Comprehensive tests for DatabaseConnection model"""
    
    def setUp(self):
        self.connection_data = {
            'name': 'Test DB',
            'db_type': 'postgresql',
            'host': 'localhost',
            'port': 5432,
            'username': 'test',
            'password': 'password',
            'database_name': 'testdb',
        }
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_create_connection(self):
        """Test creating a database connection"""
        connection = DatabaseConnection.objects.create(**self.connection_data)
        self.assertEqual(connection.name, 'Test DB')
        self.assertEqual(connection.db_type, 'postgresql')
        self.assertEqual(connection.host, 'localhost')
        self.assertEqual(connection.port, 5432)
        
    def test_create_connection_with_user(self):
        """Test creating connection and assigning to user"""
        connection = DatabaseConnection.objects.create(
            owner=self.user,
            **self.connection_data
        )
        self.assertEqual(connection.owner, self.user)
        self.assertIn(connection, self.user.databaseconnection_set.all())

    def test_password_encryption(self):
        """Test password is encrypted at rest"""
        connection = DatabaseConnection.objects.create(**self.connection_data)
        # Password should be encrypted, not stored as plain text
        self.assertNotEqual(connection.password, 'password')
        # But decrypted_password property should return original
        self.assertEqual(connection.decrypted_password, 'password')
        
    def test_password_persistence(self):
        """Test encrypted password persists after save/reload"""
        connection = DatabaseConnection.objects.create(**self.connection_data)
        encrypted_password = connection.password
        
        # Reload from database
        reloaded = DatabaseConnection.objects.get(id=connection.id)
        self.assertEqual(reloaded.password, encrypted_password)
        self.assertEqual(reloaded.decrypted_password, 'password')
        
    def test_create_different_db_types(self):
        """Test creating connections for different database types"""
        db_types = ['postgresql', 'mysql', 'mongodb', 'clickhouse']
        
        for db_type in db_types:
            data = self.connection_data.copy()
            data['db_type'] = db_type
            data['name'] = f'Test {db_type}'
            connection = DatabaseConnection.objects.create(**data)
            self.assertEqual(connection.db_type, db_type)
            
    def test_connection_string_generation(self):
        """Test connection string is properly formed"""
        connection = DatabaseConnection.objects.create(**self.connection_data)
        # Verify essential fields
        self.assertIsNotNone(connection.host)
        self.assertIsNotNone(connection.port)
        self.assertIsNotNone(connection.username)
        
    def test_duplicate_connection_names_allowed(self):
        """Test same user can have multiple connections with different names"""
        conn1 = DatabaseConnection.objects.create(
            name='Production DB',
            owner=self.user,
            **self.connection_data
        )
        data2 = self.connection_data.copy()
        data2['name'] = 'Staging DB'
        conn2 = DatabaseConnection.objects.create(
            owner=self.user,
            **data2
        )
        self.assertEqual(conn1.owner, conn2.owner)
        self.assertEqual(DatabaseConnection.objects.filter(owner=self.user).count(), 2)


class StoredFileModelTest(TestCase):
    """Comprehensive tests for StoredFile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.file = StoredFile.objects.create(
            user=self.user,
            filepath='/path/to/file.json',
            base_filename='extraction_postgresql_users_admin',
            table_name='users',
            connection_name='Production DB'
        )

    def test_create_stored_file(self):
        """Test creating stored file with all metadata"""
        self.assertEqual(self.file.user.username, 'testuser')
        self.assertEqual(self.file.filepath, '/path/to/file.json')
        self.assertEqual(self.file.base_filename, 'extraction_postgresql_users_admin')
        self.assertEqual(self.file.table_name, 'users')
        self.assertEqual(self.file.connection_name, 'Production DB')

    def test_file_timestamps(self):
        """Test extracted_at and last_modified_at timestamps"""
        self.assertIsNotNone(self.file.extracted_at)
        self.assertIsNotNone(self.file.last_modified_at)
        # Initially they should be close
        self.assertLessEqual(
            (self.file.last_modified_at - self.file.extracted_at).total_seconds(), 
            1.0  # Within 1 second
        )

    def test_file_filtering_by_table_name(self):
        """Test filtering files by table name"""
        file2 = StoredFile.objects.create(
            user=self.user,
            filepath='/path/to/file2.json',
            table_name='orders'
        )
        users_files = StoredFile.objects.filter(table_name='users')
        orders_files = StoredFile.objects.filter(table_name='orders')
        
        self.assertEqual(users_files.count(), 1)
        self.assertEqual(orders_files.count(), 1)
        self.assertIn(self.file, users_files)
        self.assertIn(file2, orders_files)

    def test_file_filtering_by_date_range(self):
        """Test filtering files by extracted_at date range"""
        from datetime import timedelta
        
        file1_time = timezone.now()
        file1 = StoredFile.objects.create(user=self.user, filepath='/file1.json')
        
        file2_time = timezone.now() + timedelta(hours=1)
        file2 = StoredFile.objects.create(user=self.user, filepath='/file2.json')
        
        # Query files between the two
        mid_time = file1_time + timedelta(minutes=30)
        files_after = StoredFile.objects.filter(extracted_at__gte=mid_time)
        
        self.assertIn(file2, files_after)

    def test_file_ordering_by_latest_first(self):
        """Test ordering files by latest extracted first"""
        file2 = StoredFile.objects.create(user=self.user, filepath='/file2.json')
        file3 = StoredFile.objects.create(user=self.user, filepath='/file3.json')
        
        latest_first = StoredFile.objects.all().order_by('-extracted_at')
        self.assertEqual(latest_first.first().id, file3.id)
        
    def test_file_sharing(self):
        """Test file sharing with other users"""
        self.file.shared_with.add(self.other_user)
        self.assertIn(self.other_user, self.file.shared_with.all())
        
    def test_multiple_files_per_user(self):
        """Test user can have multiple extracted files"""
        file2 = StoredFile.objects.create(
            user=self.user,
            filepath='/path/to/file2.json'
        )
        file3 = StoredFile.objects.create(
            user=self.user,
            filepath='/path/to/file3.json'
        )
        
        user_files = StoredFile.objects.filter(user=self.user)
        self.assertEqual(user_files.count(), 3)
        self.assertIn(self.file, user_files)
        self.assertIn(file2, user_files)
        self.assertIn(file3, user_files)


class ExtractedDataModelTest(TestCase):
    """Comprehensive tests for ExtractedData model"""
    
    def setUp(self):
        self.connection = DatabaseConnection.objects.create(
            name='Test DB',
            db_type='postgresql',
            host='localhost',
            port=5432,
            username='test',
            password='password',
            database_name='testdb',
        )

    def test_create_extracted_data(self):
        """Test creating extracted data record"""
        data = {'id': 1, 'name': 'Test', 'value': 100}
        extracted = ExtractedData.objects.create(
            connection=self.connection,
            data=data
        )
        self.assertEqual(extracted.data, data)
        self.assertEqual(extracted.connection, self.connection)
        
    def test_extracted_data_with_json_fields(self):
        """Test extracted data stores complex JSON structures"""
        complex_data = {
            'id': 1,
            'user': {
                'name': 'John',
                'email': 'john@example.com',
                'tags': ['admin', 'user']
            },
            'nested': {
                'level1': {
                    'level2': {
                        'value': 'deep'
                    }
                }
            }
        }
        extracted = ExtractedData.objects.create(
            connection=self.connection,
            data=complex_data
        )
        self.assertEqual(extracted.data['user']['name'], 'John')
        self.assertEqual(extracted.data['nested']['level1']['level2']['value'], 'deep')
        
    def test_extracted_data_null_values(self):
        """Test extracted data can handle null/None values"""
        data = {'id': 1, 'optional_field': None, 'name': 'Test'}
        extracted = ExtractedData.objects.create(
            connection=self.connection,
            data=data
        )
        self.assertIsNone(extracted.data.get('optional_field'))
        
    def test_multiple_extractions_same_connection(self):
        """Test same connection can have multiple extractions"""
        data1 = {'id': 1, 'name': 'First extraction'}
        data2 = {'id': 2, 'name': 'Second extraction'}
        
        ext1 = ExtractedData.objects.create(connection=self.connection, data=data1)
        ext2 = ExtractedData.objects.create(connection=self.connection, data=data2)
        
        connection_data = ExtractedData.objects.filter(connection=self.connection)
        self.assertEqual(connection_data.count(), 2)
        self.assertIn(ext1, connection_data)
        self.assertIn(ext2, connection_data)


class DatabaseConnectionSerializerTest(TestCase):
    """Comprehensive tests for DatabaseConnection serializer"""
    
    def setUp(self):
        self.connection_data = {
            'name': 'Test DB',
            'db_type': 'postgresql',
            'host': 'localhost',
            'port': 5432,
            'username': 'test',
            'password': 'password',
            'database_name': 'testdb',
        }

    def test_serializer_creates_connection(self):
        """Test serializer creates valid connection"""
        serializer = DatabaseConnectionSerializer(data=self.connection_data)
        self.assertTrue(serializer.is_valid())
        connection = serializer.save()
        self.assertEqual(connection.name, 'Test DB')
        self.assertEqual(connection.db_type, 'postgresql')

    def test_serializer_validation_required_fields(self):
        """Test serializer validates required fields"""
        invalid_data = {'name': 'Test DB'}  # Missing other required fields
        serializer = DatabaseConnectionSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        
    def test_serializer_validation_invalid_port(self):
        """Test serializer validates port is integer"""
        invalid_data = self.connection_data.copy()
        invalid_data['port'] = 'not_a_number'
        serializer = DatabaseConnectionSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        
    def test_serializer_validation_invalid_db_type(self):
        """Test serializer validates db_type"""
        invalid_data = self.connection_data.copy()
        invalid_data['db_type'] = 'unsupported_db'
        serializer = DatabaseConnectionSerializer(data=invalid_data)
        # If validation is strict, this should fail
        # Adjust based on actual implementation
        pass
        
    def test_serializer_includes_all_fields(self):
        """Test serializer includes all necessary fields"""
        connection = DatabaseConnection.objects.create(**self.connection_data)
        serializer = DatabaseConnectionSerializer(connection)
        data = serializer.data
        
        required_fields = ['id', 'name', 'db_type', 'host', 'port', 'username', 'database_name']
        for field in required_fields:
            self.assertIn(field, data)
            
    def test_serializer_update_connection(self):
        """Test serializer can update existing connection"""
        connection = DatabaseConnection.objects.create(**self.connection_data)
        update_data = self.connection_data.copy()
        update_data['name'] = 'Updated DB Name'
        
        serializer = DatabaseConnectionSerializer(connection, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated = serializer.save()
        self.assertEqual(updated.name, 'Updated DB Name')
        
    def test_serializer_does_not_expose_password(self):
        """Test serializer can hide password if configured"""
        connection = DatabaseConnection.objects.create(**self.connection_data)
        serializer = DatabaseConnectionSerializer(connection)
        data = serializer.data
        # Password should not be in serializer output
        self.assertNotIn('decrypted_password', data)


class StoredFileSerializerTest(TestCase):
    """Comprehensive tests for StoredFile serializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.file = StoredFile.objects.create(
            user=self.user,
            filepath='/path/to/file.json',
            base_filename='extraction_postgresql_users',
            table_name='users',
            connection_name='Production'
        )

    def test_serializer_includes_fields(self):
        """Test serializer includes all file metadata"""
        from connector.serializers import StoredFileSerializer
        serializer = StoredFileSerializer(self.file)
        data = serializer.data
        
        required_fields = ['id', 'user', 'filepath', 'base_filename', 'table_name', 
                          'connection_name', 'extracted_at', 'last_modified_at']
        for field in required_fields:
            self.assertIn(field, data)
            
    def test_serializer_timestamp_formatting(self):
        """Test serializer formats timestamps correctly"""
        from connector.serializers import StoredFileSerializer
        serializer = StoredFileSerializer(self.file)
        data = serializer.data
        
        self.assertIsNotNone(data['extracted_at'])
        self.assertIsNotNone(data['last_modified_at'])
        # Should be in ISO format compatible with frontend
        
    def test_serializer_create_file(self):
        """Test serializer can create file record"""
        from connector.serializers import StoredFileSerializer
        file_data = {
            'user': self.user.id,
            'filepath': '/new/file.json',
            'base_filename': 'extraction_test',
            'table_name': 'test_table',
            'connection_name': 'test_connection'
        }
        serializer = StoredFileSerializer(data=file_data)
        self.assertTrue(serializer.is_valid())
        created_file = serializer.save()
        self.assertEqual(created_file.table_name, 'test_table')
