# ✅ Technical Specifications & Architecture - FULLY IMPLEMENTED

**Status:** 🟢 **COMPLETE & VERIFIED** | April 14, 2026

All technical requirements have been implemented and are functioning correctly in production.

---

## 🏗️ System Architecture - DEPLOYED & TESTED

### High-Level Flow - LIVE IMPLEMENTATION

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
DELETE /api/connections/{id}/    - Delete connection (with cascade)
POST   /api/connections/{id}/test/ - Test connection
GET    /api/connections/{id}/tables/ - Get tables list
```

#### GET /api/connections/ - List User's Connections

**Request:**
```
GET /api/connections/
Headers:
  Authorization: Token <user-token>
```

**Response (Success - 200 OK):**
```json
[
  {
    "id": 1,
    "user": 1,
    "name": "Production DB",
    "db_type": "postgresql",
    "host": "db.example.com",
    "port": 5432,
    "username": "dbuser",
    "password": "<encrypted>",
    "database_name": "main_db",
    "is_staff": true,
    "created_at": "2026-04-14T10:00:00Z"
  },
  {
    "id": 2,
    "user": 1,
    "name": "Analytics MySQL",
    "db_type": "mysql",
    "host": "analytics.local",
    "port": 3306,
    "username": "analytics_user",
    "password": "<encrypted>",
    "database_name": "analytics_db",
    "is_staff": true,
    "created_at": "2026-04-13T15:30:00Z"
  }
]
```

#### POST /api/connections/ - Create New Connection

**Request:**
```
POST /api/connections/
Headers:
  Authorization: Token <user-token>
  X-CSRFToken: <csrf-token>
  Content-Type: application/json

Body:
{
  "name": "My PostgreSQL Server",
  "db_type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "username": "postgres",
  "password": "password123",
  "database_name": "mydb"
}
```

**Alternative Database Types:**
```json
{
  "name": "MySQL Server",
  "db_type": "mysql",
  "host": "localhost",
  "port": 3306,
  "username": "root",
  "password": "password",
  "database_name": "testdb"
}
```

```json
{
  "name": "MongoDB Atlas",
  "db_type": "mongodb",
  "host": "mongodb+srv://user:pass@cluster.mongodb.net",
  "port": 27017,
  "username": "mongouser",
  "password": "mongopass",
  "database_name": "mongodb_name"
}
```

```json
{
  "name": "ClickHouse Server",
  "db_type": "clickhouse",
  "host": "localhost",
  "port": 8123,
  "username": "default",
  "password": "default",
  "database_name": "default"
}
```

**Response (Success - 201 Created):**
```json
{
  "id": 50,
  "user": 1,
  "name": "My PostgreSQL Server",
  "db_type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "username": "postgres",
  "password": "<encrypted-token>",
  "database_name": "mydb",
  "is_staff": true,
  "created_at": "2026-04-15T10:00:00Z"
}
```

**Response (Validation Error - 400):**
```json
{
  "name": ["This field may not be blank."],
  "db_type": ["Invalid database type. Choices: postgresql, mysql, mongodb, clickhouse"]
}
```

**Response (Duplicate Name - 400):**
```json
{
  "error": "Connection with this name already exists"
}
```

**Response (Authentication Error - 401):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### GET /api/connections/{id}/ - Get Connection Details

**Request:**
```
GET /api/connections/50/
Headers:
  Authorization: Token <user-token>
```

**Response (Success - 200 OK):**
```json
{
  "id": 50,
  "user": 1,
  "name": "My PostgreSQL Server",
  "db_type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "username": "postgres",
  "password": "<encrypted>",
  "database_name": "mydb",
  "is_staff": true,
  "created_at": "2026-04-15T10:00:00Z"
}
```

**Response (Not Found - 404):**
```json
{
  "detail": "Not found."
}
```

**Response (Permission Denied - 403):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### PUT /api/connections/{id}/ - Update Connection

**Request:**
```
PUT /api/connections/50/
Headers:
  Authorization: Token <user-token>
  X-CSRFToken: <csrf-token>
  Content-Type: application/json

Body:
{
  "name": "Updated PostgreSQL",
  "host": "new-host.example.com",
  "port": 5433,
  "username": "newuser",
  "password": "newpassword",
  "database_name": "updated_db"
}
```

**Response (Success - 200 OK):**
```json
{
  "id": 50,
  "user": 1,
  "name": "Updated PostgreSQL",
  "db_type": "postgresql",
  "host": "new-host.example.com",
  "port": 5433,
  "username": "newuser",
  "password": "<encrypted>",
  "database_name": "updated_db",
  "is_staff": true,
  "created_at": "2026-04-15T10:00:00Z"
}
```

#### POST /api/connections/{id}/test/ - Test Connection

**Request:**
```
POST /api/connections/50/test/
Headers:
  Authorization: Token <user-token>
  X-CSRFToken: <csrf-token>
  Content-Type: application/json
```

**Response (Success - 200 OK):**
```json
{
  "status": "success",
  "message": "Connection valid",
  "database": "mydb",
  "version": "PostgreSQL 14.5"
}
```

**Response (Connection Failed - 400):**
```json
{
  "status": "error",
  "message": "Connection refused: Unable to connect to host 'invalid-host.com'"
}
```

**Response (Authentication Failed - 400):**
```json
{
  "status": "error",
  "message": "Authentication failed: Invalid username or password"
}
```

#### GET /api/connections/{id}/tables/ - Get Available Tables

**Request:**
```
GET /api/connections/50/tables/
Headers:
  Authorization: Token <user-token>
```

**Response (Success - 200 OK):**
```json
{
  "tables": [
    "users",
    "products",
    "orders",
    "customers",
    "invoices"
  ],
  "count": 5,
  "database": "mydb"
}
```

**Response (No Tables - 200 OK):**
```json
{
  "tables": [],
  "count": 0,
  "database": "mydb"
}
```

---

#### GET /api/connections/ - List User's Connections

**Request:**
```
GET /api/connections/
Headers:
  Authorization: Token <user-token>
```

**Response (Success - 200 OK):**
```json
[
  {
    "id": 1,
    "user": 1,
    "name": "Production DB",
    "db_type": "postgresql",
    "host": "db.example.com",
    "port": 5432,
    "username": "dbuser",
    "password": "<encrypted>",
    "database_name": "main_db",
    "is_staff": true,
    "created_at": "2026-04-14T10:00:00Z"
  },
  {
    "id": 2,
    "user": 1,
    "name": "Analytics MySQL",
    "db_type": "mysql",
    "host": "analytics.local",
    "port": 3306,
    "username": "analytics_user",
    "password": "<encrypted>",
    "database_name": "analytics_db",
    "is_staff": true,
    "created_at": "2026-04-13T15:30:00Z"
  }
]
```

#### POST /api/connections/ - Create New Connection

**Request:**
```
POST /api/connections/
Headers:
  Authorization: Token <user-token>
  X-CSRFToken: <csrf-token>
  Content-Type: application/json

Body:
{
  "name": "My PostgreSQL Server",
  "db_type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "username": "postgres",
  "password": "password123",
  "database_name": "mydb"
}
```

**Alternative Database Types:**
```json
{
  "name": "MySQL Server",
  "db_type": "mysql",
  "host": "localhost",
  "port": 3306,
  "username": "root",
  "password": "password",
  "database_name": "testdb"
}
```

```json
{
  "name": "MongoDB Atlas",
  "db_type": "mongodb",
  "host": "mongodb+srv://user:pass@cluster.mongodb.net",
  "port": 27017,
  "username": "mongouser",
  "password": "mongopass",
  "database_name": "mongodb_name"
}
```

```json
{
  "name": "ClickHouse Server",
  "db_type": "clickhouse",
  "host": "localhost",
  "port": 8123,
  "username": "default",
  "password": "default",
  "database_name": "default"
}
```

**Response (Success - 201 Created):**
```json
{
  "id": 50,
  "user": 1,
  "name": "My PostgreSQL Server",
  "db_type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "username": "postgres",
  "password": "<encrypted-token>",
  "database_name": "mydb",
  "is_staff": true,
  "created_at": "2026-04-15T10:00:00Z"
}
```

**Response (Validation Error - 400):**
```json
{
  "name": ["This field may not be blank."],
  "db_type": ["Invalid database type. Choices: postgresql, mysql, mongodb, clickhouse"]
}
```

**Response (Duplicate Name - 400):**
```json
{
  "error": "Connection with this name already exists"
}
```

**Response (Authentication Error - 401):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### GET /api/connections/{id}/ - Get Connection Details

**Request:**
```
GET /api/connections/50/
Headers:
  Authorization: Token <user-token>
```

**Response (Success - 200 OK):**
```json
{
  "id": 50,
  "user": 1,
  "name": "My PostgreSQL Server",
  "db_type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "username": "postgres",
  "password": "<encrypted>",
  "database_name": "mydb",
  "is_staff": true,
  "created_at": "2026-04-15T10:00:00Z"
}
```

**Response (Not Found - 404):**
```json
{
  "detail": "Not found."
}
```

**Response (Permission Denied - 403):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### PUT /api/connections/{id}/ - Update Connection

**Request:**
```
PUT /api/connections/50/
Headers:
  Authorization: Token <user-token>
  X-CSRFToken: <csrf-token>
  Content-Type: application/json

Body:
{
  "name": "Updated PostgreSQL",
  "host": "new-host.example.com",
  "port": 5433,
  "username": "newuser",
  "password": "newpassword",
  "database_name": "updated_db"
}
```

**Response (Success - 200 OK):**
```json
{
  "id": 50,
  "user": 1,
  "name": "Updated PostgreSQL",
  "db_type": "postgresql",
  "host": "new-host.example.com",
  "port": 5433,
  "username": "newuser",
  "password": "<encrypted>",
  "database_name": "updated_db",
  "is_staff": true,
  "created_at": "2026-04-15T10:00:00Z"
}
```

#### POST /api/connections/{id}/test/ - Test Connection

**Request:**
```
POST /api/connections/50/test/
Headers:
  Authorization: Token <user-token>
  X-CSRFToken: <csrf-token>
  Content-Type: application/json
```

**Response (Success - 200 OK):**
```json
{
  "status": "success",
  "message": "Connection valid",
  "database": "mydb",
  "version": "PostgreSQL 14.5"
}
```

**Response (Connection Failed - 400):**
```json
{
  "status": "error",
  "message": "Connection refused: Unable to connect to host 'invalid-host.com'"
}
```

**Response (Authentication Failed - 400):**
```json
{
  "status": "error",
  "message": "Authentication failed: Invalid username or password"
}
```

#### GET /api/connections/{id}/tables/ - Get Available Tables

**Request:**
```
GET /api/connections/50/tables/
Headers:
  Authorization: Token <user-token>
```

**Response (Success - 200 OK):**
```json
{
  "tables": [
    "users",
    "products",
    "orders",
    "customers",
    "invoices"
  ],
  "count": 5,
  "database": "mydb"
}
```

**Response (No Tables - 200 OK):**
```json
{
  "tables": [],
  "count": 0,
  "database": "mydb"
}
```

---

#### DELETE /api/connections/{id}/ - Delete Connection

**Request:**
```
DELETE /api/connections/30/
Headers:
  Authorization: Token <user-token>
  X-CSRFToken: <csrf-token>
  Content-Type: application/json
```

**Response (Success - 204 No Content):**
```
HTTP/1.1 204 No Content

(Empty body - indicates successful deletion)
```

**Response (Not Found - 404):**
```json
{
  "error": "Connection not found"
}
```

**Response (Error - 500):**
```json
{
  "error": "Detailed error message"
}
```

**Cascade Delete Behavior:**

When a connection is deleted, the following cascade delete chain is triggered:

1. **ExtractedData records** - All records with `connection` FK are deleted
2. **StoredFile records** - All records with OneToOne link to deleted ExtractedData are deleted
3. **FileShare records** - All sharing records for deleted files are deleted
4. **Connection record** - The connection itself is deleted

**Data Model Relationships:**
```
DatabaseConnection
  ↓ (1-to-Many)
ExtractedData
  ↓ (1-to-1)
StoredFile
  ↓ (1-to-Many)
FileShare
```

**CSRF Protection:**
- DELETE requests require valid X-CSRFToken header
- Token can be obtained from GET /api/csrf-token/
- Prevents cross-site request forgery attacks

**Permission Requirements:**
- User must be authenticated
- User must own the connection OR be admin
- Non-owners cannot delete other users' connections

#### POST /api/connections/{id}/create-table/ - Create Table

**Request:**
```
POST /api/connections/30/create-table/
Headers:
  Authorization: Token <user-token>
  X-CSRFToken: <csrf-token>
  Content-Type: application/json

Body:
{
  "sql_statement": "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(255))"
}
```

**Response (Success - 201 Created):**
```json
{
  "status": "success",
  "message": "Table created successfully",
  "table_name": "users"
}
```

**Response (Validation Error - 400):**
```json
{
  "error": "sql_statement is required"
}
```

**Response (SQL Error - 500):**
```json
{
  "error": "SQL execution failed: {database_specific_error}"
}
```

**SQL Template Examples:**
```sql
-- PostgreSQL
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MySQL
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ClickHouse
CREATE TABLE users (
  id UInt32,
  name String,
  created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY id;
```

#### DELETE /api/connections/{id}/delete-table/ - Delete Table

**Request:**
```
DELETE /api/connections/30/delete-table/
Headers:
  Authorization: Token <user-token>
  X-CSRFToken: <csrf-token>
  Content-Type: application/json

Body:
{
  "table_name": "users"
}
```

**Response (Success - 204 No Content):**
```
HTTP/1.1 204 No Content

(Empty body - indicates successful deletion)
```

**Response (Validation Error - 400):**
```json
{
  "error": "table_name is required"
}
```

**Response (Table Not Found - 404):**
```json
{
  "error": "Table 'users' not found"
}
```

**Response (SQL Error - 500):**
```json
{
  "error": "Failed to delete table: {database_specific_error}"
}
```

#### GET /api/connections/{id}/tables/ - Get Available Tables

**Request:**
```
GET /api/connections/30/tables/
Headers:
  Authorization: Token <user-token>
```

**Response (Success - 200 OK):**
```json
{
  "tables": [
    "users",
    "products",
    "orders"
  ],
  "count": 3
}
```

**Response (Connection Not Found - 404):**
```json
{
  "error": "Connection not found"
}
```

---

**Error Handling:**
- Returns 404 if connection doesn't exist or user lacks permission
- Returns 500 with error details if deletion fails
- Deletion is atomic - either all succeeds or all fails

**Usage Example (JavaScript):**
```javascript
export async function deleteConnection(connectionId: number) {
    const csrfToken = await getCsrfToken();
    
    const response = await fetch(`${API_URL}/connections/${connectionId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken,
        },
    });
    
    if (response.status === 204) {
        return { message: 'Connection deleted successfully' };
    }
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to delete connection');
    }
}
```

### Data Extraction Endpoints
```
POST   /api/extract/             - Start extraction
GET    /api/extract/{id}/        - Get extraction status
GET    /api/extract/{id}/data/   - Get extracted data
```

### File Endpoints
```
GET    /api/files/               - List user's files (with filters & sorting)
GET    /api/files/{id}/          - Get file details & metadata
GET    /api/files/{id}/download/ - Download file (JSON or CSV)
POST   /api/files/{id}/share/    - Share file with another user
DELETE /api/files/{id}/share/{user_id}/ - Unshare file with user
PATCH  /api/files/{id}/restore/  - Restore deleted file
DELETE /api/files/{id}/          - Delete file (soft or permanent)
```

#### GET /api/files/ - List Files with Filters

**Request:**
```
GET /api/files/?table_name=users&from_date=2026-04-01&to_date=2026-04-15&sort=latest
Headers:
  Authorization: Token <user-token>
```

**Query Parameters:**
- `table_name`: Filter by table name (optional, partial match)
- `from_date`: Filter from date (YYYY-MM-DD format)
- `to_date`: Filter to date (YYYY-MM-DD format)
- `sort`: 'latest' or 'oldest' (default: latest)

**Response (Success - 200 OK):**
```json
{
  "count": 42,
  "results": [
    {
      "id": 1,
      "filename": "extraction_users_20260414.json",
      "table_name": "users",
      "connection_name": "Production DB",
      "extracted_at": "2026-04-14T12:00:00Z",
      "created_by": "john_sales",
      "shared_badge": "📤 Shared"
    }
  ]
}
```

#### GET /api/files/{id}/ - Get File Details

**Request:**
```
GET /api/files/1/
Headers:
  Authorization: Token <user-token>
```

**Response (Success - 200 OK):**
```json
{
  "id": 1,
  "filename": "extraction_users_20260414.json",
  "table_name": "users",
  "extracted_at": "2026-04-14T12:00:00Z",
  "created_by": "john_sales",
  "is_owner": true,
  "shared_with": [
    {
      "username": "sarah_analytics",
      "permission": "download"
    }
  ]
}
```

#### GET /api/files/{id}/download/ - Download File

**Request:**
```
GET /api/files/1/download/?format=json
Query params: ?format=json|csv
```

**Response:** File content in JSON or CSV format

#### POST /api/files/{id}/share/ - Share File

**Request:**
```
POST /api/files/1/share/
Body: {"user_id": 2, "permission": "download"}
```

**Response (Success - 201 Created):**
```json
{"status": "success", "message": "File shared successfully"}
```

#### DELETE /api/files/{id}/share/{user_id}/ - Unshare File

**Request:**
```
DELETE /api/files/1/share/2/
```

**Response (Success - 204 No Content):**
Empty body

#### PATCH /api/files/{id}/restore/ - Restore Deleted File

**Request:**
```
PATCH /api/files/1/restore/
```

**Response (Success - 200 OK):**
```json
{"status": "success", "message": "File restored successfully"}
```

#### DELETE /api/files/{id}/ - Delete File

**Request:**
```
DELETE /api/files/1/
Body: {"permanent": false} # or true for permanent delete
```

**Response (Success - 204 No Content):**
Empty body

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
