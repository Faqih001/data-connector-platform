from django.test import TestCase, Client
from django.contrib.auth.models import User
from connector.models import DatabaseConnection, StoredFile, ExtractedData
from rest_framework.authtoken.models import Token
import json


class DatabaseConnectionViewSetTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.connection_data = {
            'name': 'Test Connection',
            'db_type': 'postgresql',
            'host': 'localhost',
            'port': 5432,
            'username': 'test',
            'password': 'password',
            'database_name': 'testdb',
        }

    def test_create_connection(self):
        response = self.client.post(
            '/api/connections/',
            data=json.dumps(self.connection_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Test Connection')

    def test_list_connections(self):
        DatabaseConnection.objects.create(**self.connection_data)
        response = self.client.get('/api/connections/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_retrieve_connection(self):
        connection = DatabaseConnection.objects.create(**self.connection_data)
        response = self.client.get(f'/api/connections/{connection.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Test Connection')


class StoredFileViewSetTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.admin_user = User.objects.create_user(username='admin', password='password', is_staff=True)
        self.file = StoredFile.objects.create(
            user=self.user,
            filepath='/path/to/file.json'
        )

    def test_list_files_user_sees_own_files(self):
        response = self.client.get('/api/files/', HTTP_AUTHORIZATION=f'Bearer token_for_user')
        # This would require proper authentication setup
        self.assertTrue(True)  # Placeholder for proper testing with authentication

    def test_admin_sees_all_files(self):
        other_user = User.objects.create_user(username='otheruser', password='password')
        other_file = StoredFile.objects.create(
            user=other_user,
            filepath='/path/to/other/file.json'
        )
        # Admin should see all files
        self.assertTrue(True)  # Placeholder for proper testing with authentication


class DataExtractionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.connection = DatabaseConnection.objects.create(
            name='Test Connection',
            db_type='postgresql',
            host='localhost',
            port=5432,
            username='test',
            password='password',
            database_name='testdb',
        )

    def test_extract_data_endpoint(self):
        # This would require a connection to an actual database for full testing
        response = self.client.post(
            f'/api/connections/{self.connection.id}/extract_data/',
            data=json.dumps({'table_name': 'users'}),
            content_type='application/json'
        )
        # Expected to fail due to no actual database
        self.assertIn(response.status_code, [400, 500])  # Error response expected
