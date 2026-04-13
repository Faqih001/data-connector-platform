from django.test import TestCase
from django.contrib.auth.models import User
from connector.models import DatabaseConnection, StoredFile, ExtractedData
from connector.serializers import DatabaseConnectionSerializer, StoredFileSerializer
import json
import os
from django.conf import settings


class DatabaseConnectionModelTest(TestCase):
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

    def test_create_connection(self):
        connection = DatabaseConnection.objects.create(**self.connection_data)
        self.assertEqual(connection.name, 'Test DB')
        self.assertEqual(connection.db_type, 'postgresql')

    def test_password_encryption(self):
        connection = DatabaseConnection.objects.create(**self.connection_data)
        self.assertNotEqual(connection.password, 'password')
        self.assertEqual(connection.decrypted_password, 'password')


class StoredFileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.file = StoredFile.objects.create(
            user=self.user,
            filepath='/path/to/file.json'
        )

    def test_create_stored_file(self):
        self.assertEqual(self.file.user.username, 'testuser')
        self.assertEqual(self.file.filepath, '/path/to/file.json')

    def test_file_sharing(self):
        other_user = User.objects.create_user(username='otheruser', password='password')
        self.file.shared_with.add(other_user)
        self.assertIn(other_user, self.file.shared_with.all())


class ExtractedDataModelTest(TestCase):
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
        data = {'id': 1, 'name': 'Test', 'value': 100}
        extracted = ExtractedData.objects.create(
            connection=self.connection,
            data=data
        )
        self.assertEqual(extracted.data, data)
        self.assertEqual(extracted.connection, self.connection)


class DatabaseConnectionSerializerTest(TestCase):
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
        serializer = DatabaseConnectionSerializer(data=self.connection_data)
        self.assertTrue(serializer.is_valid())
        connection = serializer.save()
        self.assertEqual(connection.name, 'Test DB')

    def test_serializer_validation(self):
        invalid_data = {'name': 'Test DB'}
        serializer = DatabaseConnectionSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class StoredFileSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_serializer_includes_fields(self):
        from connector.serializers import StoredFileSerializer
        serializer = StoredFileSerializer()
        self.assertIn('user', serializer.fields)
        self.assertIn('filepath', serializer.fields)
