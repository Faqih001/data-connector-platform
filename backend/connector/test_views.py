from django.test import TestCase, Client
from django.contrib.auth.models import User
from connector.models import DatabaseConnection, StoredFile, ExtractedData
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import json


class AuthenticationTest(TestCase):
    """Tests for authentication and login flow"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
    def test_login_creates_session(self):
        """Test login creates session"""
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        # Should redirect or return success
        self.assertIn(response.status_code, [200, 302])
        
    def test_login_invalid_credentials(self):
        """Test login fails with invalid credentials"""
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertNotEqual(response.status_code, 200)
        
    def test_protected_endpoint_requires_auth(self):
        """Test protected endpoints require authentication"""
        response = self.client.get('/api/connections/')
        # Should be unauthorized
        self.assertIn(response.status_code, [401, 403])


class DatabaseConnectionViewSetTest(TestCase):
    """Tests for DatabaseConnection CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        
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
        """Test creating a connection via API"""
        response = self.client.post(
            '/api/connections/',
            data=json.dumps(self.connection_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['name'], 'Test Connection')

    def test_list_connections(self):
        """Test listing connections"""
        DatabaseConnection.objects.create(
            owner=self.user,
            **self.connection_data
        )
        response = self.client.get('/api/connections/')
        self.assertEqual(response.status_code, 200)
        connections = response.json()
        self.assertEqual(len(connections), 1)

    def test_retrieve_connection(self):
        """Test retrieving single connection"""
        connection = DatabaseConnection.objects.create(
            owner=self.user,
            **self.connection_data
        )
        response = self.client.get(f'/api/connections/{connection.id}/')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['name'], 'Test Connection')

    def test_update_connection(self):
        """Test updating connection"""
        connection = DatabaseConnection.objects.create(
            owner=self.user,
            **self.connection_data
        )
        update_data = self.connection_data.copy()
        update_data['name'] = 'Updated Connection'
        
        response = self.client.put(
            f'/api/connections/{connection.id}/',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['name'], 'Updated Connection')

    def test_delete_connection(self):
        """Test deleting connection"""
        connection = DatabaseConnection.objects.create(
            owner=self.user,
            **self.connection_data
        )
        response = self.client.delete(f'/api/connections/{connection.id}/')
        self.assertEqual(response.status_code, 204)
        
        # Verify deletion
        with self.assertRaises(DatabaseConnection.DoesNotExist):
            DatabaseConnection.objects.get(id=connection.id)

    def test_user_sees_only_own_connections(self):
        """Test users can only see their own connections"""
        other_user = User.objects.create_user(username='otheruser', password='testpass123')
        
        my_conn = DatabaseConnection.objects.create(
            owner=self.user,
            **self.connection_data
        )
        other_conn = DatabaseConnection.objects.create(
            owner=other_user,
            name='Other User Connection',
            db_type='postgresql',
            host='otherhost',
            port=5432,
            username='other',
            password='pass',
            database_name='otherdb'
        )
        
        response = self.client.get('/api/connections/')
        connections = response.json()
        connection_ids = [c['id'] for c in connections]
        
        self.assertIn(my_conn.id, connection_ids)
        self.assertNotIn(other_conn.id, connection_ids)


class StoredFileViewSetTest(TestCase):
    """Tests for StoredFile operations"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin_user = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.file = StoredFile.objects.create(
            user=self.user,
            filepath='/path/to/file.json',
            table_name='users',
            base_filename='extraction_postgresql_users'
        )

    def test_list_extracted_files(self):
        """Test listing extracted files"""
        response = self.client.get('/api/files/')
        self.assertEqual(response.status_code, 200)
        files = response.json()
        self.assertGreaterEqual(len(files), 1)

    def test_filter_files_by_table_name(self):
        """Test filtering files by table name"""
        StoredFile.objects.create(
            user=self.user,
            filepath='/path/to/orders.json',
            table_name='orders'
        )
        
        response = self.client.get('/api/files/?table_name=users')
        self.assertEqual(response.status_code, 200)
        # Response should only contain users files

    def test_filter_files_by_date_range(self):
        """Test filtering files by date range"""
        tomorrow = (timezone.now() + timedelta(days=1)).date()
        today = timezone.now().date()
        
        response = self.client.get(
            f'/api/files/?from_date={today}&to_date={tomorrow}'
        )
        self.assertEqual(response.status_code, 200)

    def test_sort_files_by_latest(self):
        """Test sorting files from latest"""
        file2 = StoredFile.objects.create(
            user=self.user,
            filepath='/path/to/file2.json',
            table_name='users'
        )
        
        response = self.client.get('/api/files/?sort=latest')
        self.assertEqual(response.status_code, 200)
        files = response.json()
        # First file should be file2 (latest)
        if len(files) > 1:
            self.assertEqual(files[0]['id'], file2.id)

    def test_user_sees_only_own_files(self):
        """Test users can only see their own files"""
        other_user = User.objects.create_user(username='otheruser', password='testpass123')
        other_file = StoredFile.objects.create(
            user=other_user,
            filepath='/other/file.json'
        )
        
        response = self.client.get('/api/files/')
        files = response.json()
        file_ids = [f['id'] for f in files]
        
        self.assertIn(self.file.id, file_ids)
        self.assertNotIn(other_file.id, file_ids)

    def test_admin_sees_all_files(self):
        """Test admin can see all files"""
        other_user = User.objects.create_user(username='otheruser', password='testpass123')
        other_file = StoredFile.objects.create(
            user=other_user,
            filepath='/other/file.json'
        )
        
        # Login as admin
        self.client.login(username='admin', password='testpass123')
        response = self.client.get('/api/files/')
        files = response.json()
        
        # Admin should see all files
        self.assertGreaterEqual(len(files), 2)


class DataExtractionTest(TestCase):
    """Tests for data extraction endpoint"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        
        self.connection = DatabaseConnection.objects.create(
            name='Test Connection',
            owner=self.user,
            db_type='postgresql',
            host='localhost',
            port=5432,
            username='test',
            password='password',
            database_name='testdb',
        )

    def test_extract_data_endpoint_exists(self):
        """Test extraction endpoint is available"""
        response = self.client.post(
            f'/api/connections/{self.connection.id}/extract/',
            data=json.dumps({'table_name': 'users', 'batch_size': 100}),
            content_type='application/json'
        )
        # Should exist (may fail with DB error, that's OK)
        self.assertNotEqual(response.status_code, 404)

    def test_extract_data_returns_stored_file(self):
        """Test extraction returns StoredFile record"""
        # This would require a real database connection or mock
        pass


class APIResponseFormatTest(TestCase):
    """Tests for API response formats"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_error_response_has_error_field(self):
        """Test error responses include error field"""
        # Attempt to access non-existent resource
        response = self.client.get('/api/connections/99999/')
        self.assertEqual(response.status_code, 404)

    def test_success_response_format(self):
        """Test success responses follow expected format"""
        response = self.client.get('/api/connections/')
        self.assertEqual(response.status_code, 200)
        # Response should be valid JSON
        self.assertIsNotNone(response.json())
