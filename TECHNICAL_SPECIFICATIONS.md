# Technical Specifications & Architecture

---

## 🏗️ System Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Next.js)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Login │ Connections │ Extract │ Edit Grid │ Submit  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ (API)
┌─────────────────────────────────────────────────────────────┐
│              BACKEND (Django REST Framework)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Authentication │ Connectors │ Validators │ Storage   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         ↕                    ↕                     ↕
    ┌─────────┐          ┌──────────┐       ┌─────────────┐
    │   App   │          │  Source  │       │   File      │
    │Database │          │Databases │       │  Storage    │
    │(Psql)   │          │(Multiple)│       │(JSON/CSV)   │
    └─────────┘          └──────────┘       └─────────────┘
```

---

## 🔌 Database Connector Abstraction

### Connector Interface Pattern

All database connectors should implement a common interface:

```python
class DatabaseConnector:
    """Abstract base for all database connectors"""
    
    def connect(self, config: ConnectionConfig) -> bool:
        """Test and establish connection"""
        raise NotImplementedError
    
    def get_tables(self) -> List[str]:
        """Get list of available tables in database"""
        raise NotImplementedError
    
    def get_table_schema(self, table_name: str) -> Dict:
        """Get column names and types"""
        raise NotImplementedError
    
    def extract_data(self, table_name: str, batch_size: int, 
                     offset: int = 0) -> List[Dict]:
        """Extract data with pagination support"""
        raise NotImplementedError
    
    def close(self):
        """Close database connection"""
        raise NotImplementedError
```

### Supported Connectors

#### 1. PostgreSQL Connector
- **Library:** psycopg2 or psycopg3
- **Connection Params:**
  - Host, Port (5432)
  - Database name
  - Username, Password
  - SSL option
- **Data Types:** Native Python type mapping

#### 2. MySQL Connector
- **Library:** mysql-connector-python or PyMySQL
- **Connection Params:**
  - Host, Port (3306)
  - Database name
  - Username, Password
  - Charset (utf8mb4)
- **Data Types:** Native Python type mapping

#### 3. MongoDB Connector
- **Library:** pymongo
- **Connection Params:**
  - Host, Port (27017)
  - Database name
  - Collection name
  - Username, Password (if Auth enabled)
- **Query:** Return documents as dicts
- **Note:** MongoDB doesn't have "tables" - use collections

#### 4. ClickHouse Connector
- **Library:** clickhouse-driver
- **Connection Params:**
  - Host, Port (8123)
  - Database name
  - Username, Password
  - HTTPS option
- **Batch Queries:** Use LIMIT/OFFSET

---

## 📊 Data Model

### Core Models

#### DatabaseConnection
```python
class DatabaseConnection(models.Model):
    user = ForeignKey(User)
    name = CharField()  # e.g., "Production PostgreSQL"
    db_type = CharField(choices=[
        ('postgresql', 'PostgreSQL'),
        ('mysql', 'MySQL'),
        ('mongodb', 'MongoDB'),
        ('clickhouse', 'ClickHouse'),
    ])
    
    # Connection config (encrypted)
    config = JSONField()  # {host, port, database, user, password}
    
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'name')
```

#### ExtractedData
```python
class ExtractedData(models.Model):
    connection = ForeignKey(DatabaseConnection)
    source_table = CharField()
    
    # Original data snapshot
    original_data = JSONField()
    
    # Modified data
    modified_data = JSONField(null=True, blank=True)
    
    submission_status = CharField(choices=[
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('error', 'Error'),
    ])
    
    created_at = DateTimeField(auto_now_add=True)
    submitted_at = DateTimeField(null=True)
    
    edited_by = ForeignKey(User, null=True)
```

#### StoredFile
```python
class StoredFile(models.Model):
    extracted_data = ForeignKey(ExtractedData)
    user = ForeignKey(User)
    
    file_path = CharField()  # Path in storage
    file_format = CharField(choices=[
        ('json', 'JSON'),
        ('csv', 'CSV'),
    ])
    
    file_size = IntegerField()
    
    # Metadata
    source_connection = CharField()
    source_table = CharField()
    submission_timestamp = DateTimeField()
    
    class Meta:
        permissions = [
            ('can_download_file', 'Can download file'),
            ('can_share_file', 'Can share file'),
        ]
```

---

## 🔐 Authentication & Authorization

### Authentication Flow

```
1. User submits login form
   ↓
2. Backend validates credentials
   ↓
3. Session/Token created
   ↓
4. Frontend stores session/token
   ↓
5. Subsequent requests include auth token
   ↓
6. Backend validates token before processing
```

### Permission Model

```python
# User roles
class UserRole(models.Model):
    user = OneToOneField(User)
    role = CharField(choices=[
        ('admin', 'Administrator'),
        ('user', 'Regular User'),
    ])
    permissions = ManyToManyField(Permission)
```

**Admin Permissions:**
- View/edit all database connections
- Access all extracted files
- Manage user permissions
- View audit logs

**Regular User Permissions:**
- Create own database connections
- Extract from own connections
- View/download own files
- Access files shared with them

### File Access Control

```python
class FileShare(models.Model):
    file = ForeignKey(StoredFile)
    shared_with_user = ForeignKey(User)
    permission = CharField(choices=[
        ('view', 'View Only'),
        ('download', 'View & Download'),
        ('edit', 'View, Download & Edit'),
    ])
    created_at = DateTimeField(auto_now_add=True)
```

---

## 📡 API Endpoints

### Authentication Endpoints
```
POST   /api/auth/login           - User login
POST   /api/auth/logout          - User logout
POST   /api/auth/register        - Register new user
GET    /api/auth/user            - Get current user
POST   /api/auth/refresh-token   - Refresh token (if JWT)
```

### Connection Endpoints
```
GET    /api/connections/         - List user's connections
POST   /api/connections/         - Create new connection
GET    /api/connections/{id}/    - Get connection details
PUT    /api/connections/{id}/    - Update connection
DELETE /api/connections/{id}/    - Delete connection
POST   /api/connections/{id}/test/ - Test connection
GET    /api/connections/{id}/tables/ - Get tables list
```

### Data Extraction Endpoints
```
POST   /api/extract/             - Start extraction
GET    /api/extract/{id}/        - Get extraction status
GET    /api/extract/{id}/data/   - Get extracted data
```

### File Endpoints
```
GET    /api/files/               - List user's files
GET    /api/files/{id}/          - Get file details
GET    /api/files/{id}/download/ - Download file
POST   /api/files/{id}/share/    - Share file with user
DELETE /api/files/{id}/          - Delete file
```

### Submission Endpoints
```
POST   /api/submissions/submit/  - Submit extracted data
GET    /api/submissions/         - List submissions
GET    /api/submissions/{id}/    - Get submission details
```

---

## 🗄️ Data Storage Strategy

### Application Database
- **Type:** PostgreSQL or SQLite
- **Storage:** Direct database records
- **Purpose:** Querying, filtering, permission checking
- **Tables:** Users, Connections, ExtractedData, StoredFiles, Submissions

### File Storage
- **Type:** File system (production: S3/Cloud Storage)
- **Format:** JSON and/or CSV
- **Directory Structure:**
  ```
  storage/
  └── {user_id}/
      └── {connection_id}/
          └── {submission_id}_{timestamp}.{json|csv}
  ```
- **File Content Example (JSON):**
  ```json
  {
    "submission_id": "sub_123456",
    "timestamp": "2026-04-14T10:30:00Z",
    "source": {
      "database": "Production PostgreSQL",
      "table": "users",
      "connection_id": "conn_789"
    },
    "submitted_by": "john_doe",
    "batch_size": 500,
    "total_rows": 1250,
    "data": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "original_value": "john@old.com",
        "modified_value": "john@example.com",
        "changed": true
      },
      ...
    ]
  }
  ```

---

## 🧪 Error Handling Strategy

### Connection Errors
```python
class ConnectionError(Exception):
    """Database connection failed"""
    pass

class AuthenticationError(Exception):
    """Invalid credentials"""
    pass

class TimeoutError(Exception):
    """Connection timeout"""
    pass
```

### Data Validation Errors
```python
class ValidationError(Exception):
    """Data validation failed"""
    pass

class TypeMismatchError(Exception):
    """Column type mismatch"""
    pass
```

### API Response Pattern
```python
# Success
{
    "status": "success",
    "data": {...},
    "message": "Operation completed"
}

# Error
{
    "status": "error",
    "error_code": "INVALID_CREDENTIALS",
    "message": "Connection failed: Invalid credentials",
    "details": {...}
}
```

---

## 🚀 Deployment Architecture

### Docker Compose Structure
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment: [NEXT_PUBLIC_API_URL]
    depends_on: [backend]
  
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment: [DATABASE_URL, SECRET_KEY]
    depends_on: [db]
    volumes: [./backend:/app, ./storage:/app/storage]
  
  db:
    image: postgres:15
    environment: [POSTGRES_DB, POSTGRES_PASSWORD]
    volumes: [postgres_data:/var/lib/postgresql/data]
    ports: ["5432:5432"]

volumes:
  postgres_data:
```

---

## 📈 Performance Considerations

1. **Batch Processing**
   - Implement pagination for large datasets
   - Use batch_size parameter to control memory usage
   - Consider async task processing for large extractions

2. **Caching**
   - Cache database schemas
   - Cache connection status
   - Invalidate cache on changes

3. **Database Indexing**
   - Index on user_id for permission queries
   - Index on connection_id for filtering
   - Index on created_at for date range queries

4. **Connection Pooling**
   - Reuse connections where possible
   - Limit concurrent connections to source databases
   - Properly close connections after use

---

## 🔒 Security Best Practices

1. **Credential Storage**
   - Never store credentials in plaintext
   - Encrypt all connection configs
   - Use environment variables for secrets

2. **SQL Injection Prevention**
   - Use parameterized queries
   - Never concatenate user input into SQL
   - Validate/sanitize all inputs

3. **Access Control**
   - Always check permissions before data access
   - Implement row-level security where needed
   - Log all access attempts

4. **Data Privacy**
   - Hash sensitive data in logs
   - Anonymize file downloads when needed
   - Implement data retention/deletion policies

---

## 📊 Testing Strategy

### Unit Tests
- Connector logic (each database type)
- Data extraction with edge cases
- Permission/RBAC checks
- Data validation rules

### Integration Tests
- End-to-end data flow
- Database operations
- File storage operations
- API endpoint functionality

### Performance Tests
- Large batch extraction (10k+ rows)
- Concurrent user access
- File generation performance

---

**Next:** See ASSESSMENT_DELIVERABLES.md for submission details
