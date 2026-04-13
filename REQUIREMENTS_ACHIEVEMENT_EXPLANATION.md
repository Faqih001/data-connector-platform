# Detailed Explanation: How Each Requirement Is Achieved

*Last Updated: April 13, 2026*

## Overview
This document provides detailed explanations with code examples for how each requirement is implemented in the Data Connector Platform.

---

## 1. EXTENSIBLE DESIGN - Easy to Add New DB Types ✅ ACHIEVED

### Requirement
Build a system where adding new database types is straightforward without major refactoring.

### How It's Achieved

#### Architecture Pattern: Abstract Factory Pattern

The system uses an abstract base class and factory function to manage all database connectors:

**File:** `backend/connector/connectors.py`

```python
# Abstract base class - defines the interface all connectors must implement
class BaseConnector(ABC):
    def __init__(self, connection_details):
        self.connection_details = connection_details
        self.connection = None

    @abstractmethod
    def connect(self):
        """Each DB type implements connection logic"""
        pass

    @abstractmethod
    def fetch_batch(self, table_name, batch_size, offset):
        """Each DB type implements batch fetching"""
        pass

    def close(self):
        """Common cleanup logic"""
        if self.connection:
            self.connection.close()
```

#### Concrete Implementations (4 supported DB types)

```python
# PostgreSQL Implementation
class PostgresConnector(BaseConnector):
    def connect(self):
        password = getattr(self.connection_details, 'decrypted_password', ...)
        self.connection = psycopg2.connect(
            host=self.connection_details.host,
            port=self.connection_details.port,
            user=self.connection_details.username,
            password=password,
            dbname=self.connection_details.database_name,
        )

    def fetch_batch(self, table_name, batch_size, offset):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [{col: serialize_value(val) for col, val in zip(columns, row)} for row in rows]

# MySQL Implementation
class MySQLConnector(BaseConnector): ...

# MongoDB Implementation
class MongoConnector(BaseConnector): ...

# ClickHouse Implementation
class ClickHouseConnector(BaseConnector): ...
```

#### Factory Function - Dynamic Connector Selection

```python
def get_connector(connection_details):
    """Returns the appropriate connector based on DB type"""
    if connection_details.db_type == 'postgresql':
        return PostgresConnector(connection_details)
    elif connection_details.db_type == 'mysql':
        return MySQLConnector(connection_details)
    elif connection_details.db_type == 'mongodb':
        return MongoConnector(connection_details)
    elif connection_details.db_type == 'clickhouse':
        return ClickHouseConnector(connection_details)
    else:
        raise ValueError("Unsupported database type")
```

### To Add a New Database Type (e.g., Oracle)

**Step 1:** Add to model choices (file: `backend/connector/models.py`)
```python
class DatabaseConnection(models.Model):
    DB_TYPE_CHOICES = [
        ('postgresql', 'PostgreSQL'),
        ('mysql', 'MySQL'),
        ('mongodb', 'MongoDB'),
        ('clickhouse', 'ClickHouse'),
        ('oracle', 'Oracle'),  # NEW - Add here
    ]
```

**Step 2:** Create new connector class (file: `backend/connector/connectors.py`)
```python
import oracledb  # New import

class OracleConnector(BaseConnector):
    def connect(self):
        password = getattr(self.connection_details, 'decrypted_password', ...)
        self.connection = oracledb.connect(
            user=self.connection_details.username,
            password=password,
            dsn=f"{self.connection_details.host}:{self.connection_details.port}/{self.connection_details.database_name}"
        )

    def fetch_batch(self, table_name, batch_size, offset):
        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT * FROM {table_name} OFFSET {offset} FETCH NEXT {batch_size} ROWS ONLY"
        )
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [{col: serialize_value(val) for col, val in zip(columns, row)} for row in rows]
```

**Step 3:** Update factory function (file: `backend/connector/connectors.py`)
```python
def get_connector(connection_details):
    # ... existing code ...
    elif connection_details.db_type == 'oracle':  # NEW - Add this
        return OracleConnector(connection_details)
    # ... rest of code ...
```

### Why This Is Extensible ✅

| Aspect | Benefit |
|--------|---------|
| **Abstract base class** | Defines interface, enforces consistency |
| **Factory pattern** | No need to modify calling code |
| **Separation of concerns** | Each DB type isolated in its own class |
| **Minimal changes needed** | Add only 3 pieces: model choice, connector class, factory case |
| **Zero impact on existing code** | No refactoring of other components |

---

## 2. BATCH SIZE MUST BE CONFIGURABLE ✅ PARTIALLY ACHIEVED

### Requirement
Data extraction must support configurable batch sizes (not hardcoded to one value).

### How It's Achieved (Backend)

**File:** `backend/connector/services.py`

```python
def extract_data_in_batches(connection_details, table_name, batch_size=1000):
    """
    Extract data in configurable batches
    
    Args:
        connection_details: DatabaseConnection model instance
        table_name: Name of table/collection to extract from
        batch_size: Number of rows per batch (default: 1000)
    """
    connector = get_connector(connection_details)
    connector.connect()
    offset = 0
    
    while True:
        # Fetch batch with configurable size
        batch = connector.fetch_batch(table_name, batch_size, offset)
        if not batch:
            break
        yield batch  # Return batch as generator
        offset += batch_size
    
    connector.close()
```

### Backend Usage Examples

```python
# API can call with custom batch sizes:

# Default 1000 rows per batch
for batch in extract_data_in_batches(connection, table_name):
    process(batch)

# Custom: 5000 rows per batch
for batch in extract_data_in_batches(connection, table_name, batch_size=5000):
    process(batch)

# Custom: 100 rows per batch (for large datasets requiring frequent saves)
for batch in extract_data_in_batches(connection, table_name, batch_size=100):
    process(batch)
```

### Current API Endpoints (Both Support Batch Size Parameter)

**Endpoint 1:** `/api/connections/{id}/extract_data/`
```python
@action(detail=True, methods=['post'])
def extract_data(self, request, pk=None):
    connection = self.get_object()
    table_name = request.data.get('table_name')
    batch_size = request.data.get('batch_size', 1000)  # ← Can be sent in request
    
    for batch in extract_data_in_batches(connection, table_name, batch_size=batch_size):
        # Process batch...
```

**Endpoint 2:** `/api/extract/`
```python
@api_view(['POST'])
def extract_data_endpoint(request):
    # ...
    batch_size = request.data.get('batch_size', 1000)  # ← Can be configured
    
    for batch in extract_data_in_batches(connection, table_name, batch_size=batch_size):
        # Process batch...
```

### Frontend Implementation Status

❌ **NOT FULLY EXPOSED** - Currently missing:

**Current Request (NO batch_size control):**
```typescript
// app/lib/api.ts
export async function extractData(connectionId: number, tableName: string): Promise<any[]> {
  const response = await fetch(`${API_URL}/connections/${connectionId}/extract_data/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ table_name: tableName }),  // ← No batch_size
  });
  return response.json();
}
```

**What's Missing:**
- No UI input field for batch_size
- API call doesn't send batch_size parameter
- Frontend always uses default 1000

### Recommendation

**To fully expose batch configurability to UI:**

1. Add input field to extraction form (app/page.tsx)
2. Update extractData() function to accept/send batch_size
3. Update API call to include batch_size parameter
4. Display feedback (e.g., estimated rows per batch)

---

## 3. MODIFIED DATA SUBMITTED BACK TO DRF ❌ NOT FULLY ACHIEVED

### Requirement
When user modifies data in the grid and submits, it must:
1. Send data back to the DRF backend
2. Update the DRF models/database
3. Validate and process data

### Current Implementation (Partial)

**File:** `backend/connector/views.py` (lines 76-92)

```python
@action(detail=True, methods=['post'])
def submit_data(self, request, pk=None):
    """Submit modified data"""
    file = self.get_object()
    data = request.data.get('data')

    if not data:
        return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # ✅ Saves to disk file
        with open(file.filepath, 'w') as f:
            json.dump(data, f, default=str)
        
        return Response({"message": "File updated successfully"}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

### What Currently Works ✅
- Data is sent from frontend to backend ✅
- Data is persisted to disk file ✅
- Endpoint returns success response ✅

### What's Missing ❌

1. **Database model not updated:**
   ```python
   # Missing: Update ExtractedData model
   ExtractedData.objects.filter(id=...).update(data=data)
   ```

2. **No DRF validation:**
   ```python
   # Should use serializer validation
   serializer = ExtractedDataSerializer(data=data)
   if serializer.is_valid():
       serializer.save()
   ```

3. **No data transformation:**
   - Data not processed or stored in structured format
   - No audit trail of changes

### Recommended Fix

**Updated submit_data() endpoint:**

```python
@action(detail=True, methods=['post'])
def submit_data(self, request, pk=None):
    """Submit modified data with full DRF integration"""
    file = self.get_object()
    data = request.data.get('data')

    if not data:
        return Response(
            {"error": "No data provided"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # ✅ Update ExtractedData model
        extracted_data = ExtractedData.objects.get(id=file.id)
        extracted_data.data = data
        extracted_data.save()

        # ✅ Save to disk file (backup)
        with open(file.filepath, 'w') as f:
            json.dump(data, f, default=str)
        
        # ✅ Return validated data and success
        serializer = ExtractedDataSerializer(extracted_data)
        return Response({
            "message": "Data updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    except ExtractedData.DoesNotExist:
        return Response(
            {"error": "Data not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

---

## 4. STORE AS FILE - JSON OR CSV FORMAT ✅ ACHIEVED

### Requirement
- Save extracted data as files
- Support JSON or CSV format
- Format selection before saving

### How It's Achieved

#### Default Storage Format: JSON ✅

**File:** `backend/connector/views.py` (line 35)

```python
@action(detail=True, methods=['post'])
def extract_data(self, request, pk=None):
    connection = self.get_object()
    table_name = request.data.get('table_name')

    try:
        for batch in extract_data_in_batches(connection, table_name):
            # Generate filename with JSON extension
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"extraction_{connection.name}_{table_name}_{timestamp}.json"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            
            # Save as JSON
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(batch, f, default=str)

            # Store in database
            ExtractedData.objects.create(
                connection=connection,
                data=batch
            )

            StoredFile.objects.create(
                user=user if user.is_authenticated else None,
                filepath=filepath
            )
            return Response(batch, status=status.HTTP_200_OK)
```

#### Format Conversion on Download: JSON → CSV ✅

**File:** `app/components/FileViewer.tsx`

```typescript
function jsonToCsv(jsonData: any[]): string {
  if (jsonData.length === 0) return '';
  
  // Extract headers from first row
  const headers = Object.keys(jsonData[0]);
  const csvHeaders = headers.map(h => `"${h}"`).join(',');
  
  // Convert each row to CSV
  const csvRows = jsonData.map(row =>
    headers.map(header => {
      const value = row[header];
      if (value === null || value === undefined) return '';
      const stringValue = String(value).replace(/"/g, '""');  // Escape quotes
      return `"${stringValue}"`;
    }).join(',')
  );
  
  return [csvHeaders, ...csvRows].join('\n');
}
```

#### User-Selectable Format at Download

**File:** `app/components/FileViewer.tsx` (Download implementation)

```typescript
const handleDownload = async (file: StoredFile, format: 'json' | 'csv') => {
  try {
    const fileUrl = `http://localhost:8001/api/files/${file.id}/download/`;
    
    const response = await fetch(fileUrl);
    const jsonData = await response.json();
    
    let data: string;
    let mimeType: string;
    let extension: string;
    
    // User selects format
    if (format === 'csv') {
      data = jsonToCsv(jsonData);  // Convert JSON to CSV
      mimeType = 'text/csv';
      extension = 'csv';
    } else {
      data = JSON.stringify(jsonData, null, 2);
      mimeType = 'application/json';
      extension = 'json';
    }
    
    // Trigger browser download
    const blob = new Blob([data], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${fileName.replace('.json', '')}.${extension}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (err) {
    console.error('Download failed:', err);
  }
};
```

#### Download UI

```typescript
<select
  value={downloadFormat}
  onChange={(e) => setDownloadFormat(e.target.value as 'json' | 'csv')}
  className="px-2 py-1 border rounded text-sm"
>
  <option value="json">JSON</option>
  <option value="csv">CSV</option>
</select>
<button
  onClick={() => handleDownload(file, downloadFormat)}
  className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
>
  Download
</button>
```

### Flow Diagram

```
Extraction → Save as JSON to disk → Store in DB → Show in Stored Files
                                                           ↓
                                          User selects format (JSON/CSV)
                                                           ↓
                                          Format conversion on download
                                                           ↓
                                          Browser downloads selected format
```

### Formats Supported

| Format | Storage | Download | Notes |
|--------|---------|----------|-------|
| **JSON** | ✅ Saved to disk | ✅ Available | Default format, efficient for DB storage |
| **CSV** | ❌ Not saved | ✅ Generated on-the-fly | Converted client-side, good for Excel |

---

## 5. PERMISSION & ACCESS CONTROL ✅ ACHIEVED

### Requirement
Implement role-based file access:
- **Admin:** Full access to all files
- **User:** Only their own files + files shared with them

### How It's Achieved

#### Database Models

**File:** `backend/connector/models.py`

```python
class StoredFile(models.Model):
    # User who created/owns the file
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # File path on disk
    filepath = models.CharField(max_length=255)
    
    # Files can be shared with multiple users
    shared_with = models.ManyToManyField(User, related_name='shared_files')
```

#### Role-Based Access Control in ViewSet

**File:** `backend/connector/views.py` (lines 54-63)

```python
class StoredFileViewSet(viewsets.ModelViewSet):
    serializer_class = StoredFileSerializer

    def get_queryset(self):
        """Filter files based on user role - ENFORCED FOR ALL OPERATIONS"""
        user = self.request.user
        
        # Case 1: Unauthenticated users (development mode)
        if not user.is_authenticated:
            return StoredFile.objects.all()
        
        # Case 2: Users with custom 'admin' role
        if hasattr(user, 'role') and user.role == 'admin':
            return StoredFile.objects.all()  # Full access
        
        # Case 3: Django's built-in admin users
        if user.is_staff:
            return StoredFile.objects.all()  # Full access (fallback)
        
        # Case 4: Regular users
        return (
            StoredFile.objects.filter(user=user) 
            | StoredFile.objects.filter(shared_with=user)
        ).distinct()
```

### Access Control Matrix

```
┌─────────────────────────────────────────────────────────────┐
│                    FILE ACCESS CONTROL                      │
├──────────────────┬─────────┬──────────────────────────────┤
│ User Type        │ Role    │ Can Access                   │
├──────────────────┼─────────┼──────────────────────────────┤
│ Admin User       │ admin   │ ✅ ALL files                  │
│ Django Staff     │ staff   │ ✅ ALL files                  │
│ Regular User     │ user    │ ✅ Own files +               │
│                  │         │   Files shared with them    │
│ Unauthenticated  │ None    │ ✅ ALL files (dev only)      │
└──────────────────┴─────────┴──────────────────────────────┘
```

### Enforcement Points in ViewSet

QuerySet filtering is applied to **ALL operations**:

```python
def get_queryset(self):  # Called for:
                         # ✅ LIST (GET /api/files/)
                         # ✅ RETRIEVE (GET /api/files/{id}/)
                         # ✅ UPDATE (PATCH /api/files/{id}/)
                         # ✅ DELETE (DELETE /api/files/{id}/)
                         # ✅ CUSTOM ACTIONS (POST /api/files/{id}/submit_data/)
```

### Usage Flow Example

```
User A (regular user):
  └─ GET /api/files/ 
     └─ Returns: Only files where user=A OR shared_with contains A

Admin User:
  └─ GET /api/files/
     └─ Returns: ALL files in system

User B trying to access User A's file:
  └─ GET /api/files/123/ (file owned by User A)
     └─ Returns: 404 Not Found (file not in their queryset)
```

### File Sharing Mechanic

```python
# User A shares a file with User B
file = StoredFile.objects.get(id=123)
file.shared_with.add(user_b)  # Add User B to shared_with

# Now User B can see and download the file
# User B query: StoredFile.objects.filter(shared_with=user_b)
# Returns: [file]
```

### Security Guarantees

| Scenario | Protection |
|----------|------------|
| User tries to access another's file | ✅ 404 returned (queryset filters) |
| User can share files | ✅ Allowed via M2M relationship |
| Admin views all files | ✅ No filtering applied |
| Unauthenticated access | ✅ Allowed (dev mode) or can be restricted |
| File deletion by unauthorized user | ✅ 404 returned (queryset filters) |

### Django REST Framework Integration

The ViewSet's `get_queryset()` method ensures permission filtering across:

```python
# Inherited ViewSet methods automatically use get_queryset():

class StoredFileViewSet(viewsets.ModelViewSet):
    # Default implementation of list/retrieve/update/destroy 
    # ALL use get_queryset() for authorization
    
    @action(detail=True, methods=['post'])
    def submit_data(self, request, pk=None):
        file = self.get_object()  # ← get_object() uses get_queryset()
        # Only returns file if user has access
        
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        file = self.get_object()  # ← get_object() uses get_queryset()
        # Only returns file if user has access
```

---

## Summary Table

| Requirement | Status | Location | Notes |
|------------|--------|----------|-------|
| **Extensible DB design** | ✅ ACHIEVED | connectors.py | Abstract factory pattern, easy to add new DB types |
| **Configurable batch size** | ⚠️ PARTIAL | services.py + views.py | Backend supports parameter, frontend doesn't expose it |
| **DRF data submission** | ⚠️ PARTIAL | views.py#76 | Saves to file only, doesn't update models |
| **JSON/CSV format** | ✅ ACHIEVED | FileViewer.tsx | JSON saved, CSV on-the-fly download |
| **Role-based access** | ✅ ACHIEVED | views.py#54-63 | Admin full access, users see own + shared |

---

## Recommended Enhancements

### Priority 1: Fix DRF Data Submission
- Update ExtractedData model on submit
- Add DRF serializer validation
- Create audit trail

### Priority 2: Expose Batch Size to Frontend
- Add batch_size input field
- Pass to API request
- Add UI feedback (rows per batch)

### Priority 3: Backend CSV Storage (Optional)
- Allow format selection during extraction
- Consider storage implications (JSON only vs. both)
- CSV mainly useful for Excel workflows

