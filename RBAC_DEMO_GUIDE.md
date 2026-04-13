# 🔐 File Access Rules & Role-Based Access Control (RBAC) - Demo Guide

**Platform:** Data Connector Platform  
**Demo Date:** April 13, 2026  
**Version:** 1.0  

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [User Accounts](#user-accounts)
3. [Database Connections](#database-connections)
4. [Access Rules](#access-rules)
5. [Usage Scenarios](#usage-scenarios)
6. [How to Test](#how-to-test)
7. [Technical Architecture](#technical-architecture)

---

## 🎯 Overview

This demo showcases **Role-Based Access Control (RBAC)** and **File Access Rules** implemented in the Data Connector Platform. The system ensures:

- **Admin users** have full access to all files and system functions
- **Regular users** can only access their own files and files explicitly shared with them
- **Shared files** maintain proper access control at the API level
- **Access levels** are clearly displayed in the UI with visual badges

### Key Features Demonstrated

✅ **Multi-level Access Control**  
✅ **File Ownership & Sharing**  
✅ **Permission-based UI Elements**  
✅ **Audit Trail (via access levels)**  
✅ **Secure API Endpoints**  

---

## 👥 User Accounts

Four demo users have been created to demonstrate different access levels:

### 1. **Admin User** (Full System Access)
```
Username: admin
Password: admin123
Email: admin@platform.local
Role: System Administrator
```

**Permissions:**
- 👑 View ALL files from ALL users
- 👑 Modify ANY file
- 👑 Delete ANY file
- 👑 Share/unshare ANY file
- 👑 Access full admin panel
- 👑 Manage database connections
- 👑 View all extracted data

**UI Badge:** 👑 **ADMIN**

---

### 2. **Sales Team User**
```
Username: john_sales
Password: john123
Email: john@company.com
Role: Regular User (Sales Department)
```

**Permissions:**
- 🔒 View OWN files only
- 📤 View files SHARED with him
- 🔒 Modify own files
- 🔒 Delete own files
- 🔒 Share own files with others
- 🔒 Cannot see other users' private files

**Files Accessible:**
- ✅ `extraction_users_john_*.json` (owner)
- ✅ `extraction_orders_john_*.json` (owner)
- ✅ `extraction_products_john_*.json` (owner)
- ✅ `extraction_metrics_john_*.json` (owner)
- ✅ 2 files from sarah_analytics (shared)

**UI Badge:** 🔒 **OWNER** (for own files) | 📤 **SHARED** (for received files)

---

### 3. **Analytics Team User**
```
Username: sarah_analytics
Password: sarah456
Email: sarah@company.com
Role: Regular User (Analytics Department)
```

**Permissions:**
- 🔒 View OWN files only
- 📤 View files SHARED with her
- 🔒 Modify own files
- 🔒 Delete own files
- 🔒 Share own files with others
- 🔒 Cannot see other users' private files

**Files Accessible:**
- ✅ `extraction_users_sarah_*.json` (owner)
- ✅ `extraction_orders_sarah_*.json` (owner)
- ✅ `extraction_products_sarah_*.json` (owner)
- ✅ `extraction_metrics_sarah_*.json` (owner)
- ✅ 2 files from john_sales (shared)
- ✅ Shares 1 file with mike_reporting

**UI Badge:** 🔒 **OWNER** (for own files) | 📤 **SHARED** (for received files)

---

### 4. **Reporting Team User**
```
Username: mike_reporting
Password: mike789
Email: mike@company.com
Role: Regular User (Reporting Department)
```

**Permissions:**
- 🔒 View OWN files only
- 📤 View files SHARED with him
- 🔒 Modify own files
- 🔒 Delete own files
- 🔒 Share own files with others
- 🔒 Cannot see other users' private files

**Files Accessible:**
- ✅ `extraction_users_mike_*.json` (owner)
- ✅ `extraction_orders_mike_*.json` (owner)
- ✅ `extraction_products_mike_*.json` (owner)
- ✅ `extraction_metrics_mike_*.json` (owner)
- ✅ 1 file from sarah_analytics (shared)

**UI Badge:** 🔒 **OWNER** (for own files) | 📤 **SHARED** (for received files)

---

## 📡 Database Connections

10 database connections have been configured across 4 database types:

### PostgreSQL Connections (3)
```
1. PostgreSQL Sales DB
   Host: localhost:5432
   Database: sales_database
   Username: sales_user
   Password: sales_pass_123
   
2. PostgreSQL Users Database
   Host: 192.168.1.100:5432
   Database: users_db
   Username: postgres_admin
   Password: postgres_secure_456
   
3. PostgreSQL Analytics
   Host: analytics.company.com:5432
   Database: analytics_prod
   Username: analytics_read
   Password: analytics_readonly_789
```

### MySQL Connections (3)
```
4. MySQL Customer DB
   Host: mysql.company.local:3306
   Database: customers
   Username: customer_user
   Password: customer_pass_123
   
5. MySQL Inventory System
   Host: inventory.prod.local:3306
   Database: inventory_db
   Username: inventory_app
   Password: inv_app_456
   
6. MySQL Financial Data
   Host: finance-server.internal:3306
   Database: financial_records
   Username: finance_read
   Password: fin_secure_789
```

### MongoDB Connections (3)
```
7. MongoDB Event Logs
   Host: mongodb.cluster.io:27017
   Database: eventlogs
   Username: mongo_user
   Password: mongo_pass_123
   
8. MongoDB User Activity
   Host: auth-mongo.internal:27017
   Database: user_activity
   Username: activity_monitor
   Password: activity_456
   
9. MongoDB Session Store
   Host: session-db.company.com:27017
   Database: sessions
   Username: session_mgr
   Password: session_pass_789
```

### ClickHouse Connections (1)
```
10. ClickHouse Metrics
    Host: metrics.analytics.com:9000
    Database: metrics_database
    Username: metrics_read
    Password: metrics_123
```

---

## 🔐 Access Rules

### Rule Matrix

| User Type | Own Files | Shared Files | Other Users' Files | Can Delete | Can Share | Can Modify |
|-----------|-----------|--------------|-------------------|-----------|-----------|-----------|
| **Admin** | ✅ Edit | ✅ Edit | ✅ Edit | ✅ Yes | ✅ Yes | ✅ Yes |
| **Owner** | ✅ Edit | ✅ View | ❌ No | ✅ Own | ✅ Own | ✅ Own |
| **Shared User** | N/A | ✅ View | N/A | ❌ No | ❌ No | ❌ No |

### API Permission Classes

#### 1. **IsFileOwnerOrAdmin** (Read Access)
- ✅ Admin: Full access
- ✅ File Owner: Full access
- ✅ Shared Users: Read-only access
- ❌ Others: No access

```
GET /api/files/ → Returns user's files + shared files
GET /api/files/{id}/ → If authorized (owner/admin/shared)
```

#### 2. **IsFileOwnerOrAdminForWrite** (Modify/Delete)
- ✅ Admin: Can modify any file
- ✅ File Owner: Can modify own file
- ❌ Shared Users: Cannot modify
- ❌ Others: No access

```
PUT /api/files/{id}/ → If owner or admin
DELETE /api/files/{id}/ → If owner or admin
POST /api/files/{id}/submit_data/ → If owner or admin
```

#### 3. **File Sharing Actions**
- ✅ Admin: Can share any file
- ✅ File Owner: Can share own file
- ❌ Shared Users: Cannot reshare
- ❌ Others: No access

```
POST /api/files/{id}/share/ → If owner or admin
POST /api/files/{id}/unshare/ → If owner or admin
GET /api/files/{id}/permissions/ → Get access info
```

---

## 📊 Usage Scenarios

### Scenario 1: Admin Oversight
**Actor:** admin (Full Access)

```
1. Login: admin / admin123
2. Navigation: http://localhost:3000/
3. View: Admin sees ALL 12 files (4 users × 3 files each + shared)
4. Actions:
   - Can view john_sales' private files ✅
   - Can modify sarah_analytics' data ✅
   - Can download mike_reporting's reports ✅
   - Can see complete access chains ✅
5. UI Elements:
   - All files show [👑 ADMIN] badge
   - Can access /admin/ panel
   - Can delete any file
   - Can share any file
```

### Scenario 2: Single User - Own Files Only
**Actor:** john_sales (Limited Access)

```
1. Login: john_sales / john123
2. Navigation: http://localhost:3000/
3. View: john sees 6 files
   - 4 own files (john_sales_*.json)
   - 2 shared from sarah_analytics
4. Actions:
   - Edit own files ✅
   - Share own files with sarah ✅
   - Download own data ✅
   - Try to view sarah_analytics' "other" data ❌
   - Try to modify sarah's file ❌ (shows: "Permission denied")
5. UI Elements:
   - Own files show [🔒 OWNER] badge
   - Shared files show [📤 SHARED] badge
   - Checkboxes only on OWN files
   - Share button visible on OWN files
   - Delete button disabled on SHARED files
```

### Scenario 3: Collaborative Access
**Actor:** sarah_analytics (Moderate Access)

```
1. Login: sarah_analytics / sarah456
2. Navigation: http://localhost:3000/
3. View: sarah sees 7 files
   - 4 own files (sarah_analytics_*.json)
   - 2 from john_sales (shared)
   - 1 shared with mike_reporting
4. File Permissions:
   - Can edit own files (4)
   - Cannot edit john's files (2)
   - Mike can see 1 of sarah's files
5. Sharing Actions:
   - Share own file with mike ✅
   - Unshare file from mike ✅
   - Request john to share more ❌ (no permission)
6. UI Elements:
   - Shows filenames with ownership info
   - Clear visual distinction: [🔒 OWNER] vs [📤 SHARED]
   - Permission details in expanded view
```

---

## 🧪 How to Test

### Quick Start

1. **Stop current servers:**
   ```bash
   # Stop frontend and backend if running
   ```

2. **Start Backend:**
   ```bash
   cd /home/amir/Desktop/projects/data-connector-platform/backend
   source .venv/bin/activate
   python3 manage.py runserver 8001
   ```

3. **Start Frontend (new terminal):**
   ```bash
   cd /home/amir/Desktop/projects/data-connector-platform
   npm run dev
   ```

4. **Access Application:**
   - URL: `http://localhost:3000/`
   - Admin Panel: `http://localhost:8001/admin/`

### Test Case 1: Admin Full Access
```
1. Open browser and go to http://localhost:3000/
2. Login: admin / admin123
3. Click "Stored Files" section
4. Expected: See all generated files (marked 👑 ADMIN)
5. Try: Click delete on any file → Should work ✅
6. Try: Click share on any file → Should work ✅
```

### Test Case 2: Regular User Isolation
```
1. Open new incognito window
2. Go to http://localhost:3000/
3. Login: john_sales / john123
4. Expected: See only 6 files (4 own + 2 shared from sarah)
5. Try: View file source code for URL pattern
6. Try to access: /api/files/[sarah's_private_file_id]/
7. Expected: 403 Forbidden - "Permission denied"
```

### Test Case 3: Shared File Access
```
1. Login as john_sales / john123
2. View: 2 files from sarah_analytics (marked 📤 SHARED)
3. Click expand on shared file
4. Expected: Can download but NOT delete/modify
5. Try: Click delete button
6. Expected: Button disabled or shows permission error
```

### Test Case 4: API Endpoint Security
```
Open browser DevTools → Network tab

1. Login as john_sales
2. Try API call:
   curl -H "Authorization: Bearer <token>" \
        http://localhost:8001/api/files/[sarah_id]/delete/
3. Expected: 403 Forbidden
```

### Test Case 5: Shared File Integrity
```
1. Login as sarah_analytics
2. Share "metrics_products" file with mike_reporting
3. In new window, login as mike_reporting
4. Mike should see the file (📤 SHARED)
5. Try: Mike tries to modify file
6. Expected: Permission denied, cannot submit/update
```

---

## 🏗️ Technical Architecture

### Backend Implementation

#### Permission Classes (`connector/permissions.py`)
```python
class IsFileOwnerOrAdmin(BasePermission):
    """
    Allow access only to:
    - Admins (has_perm check)
    - File owners
    - Users in shared_with list (read-only)
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin has full access
        if request.user.is_staff:
            return True
        
        # Owner has full access
        if obj.user == request.user:
            return True
        
        # Shared users have read-only
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return obj.shared_with.filter(id=request.user.id).exists()
        
        return False
```

#### Database Model (`connector/models.py`)
```python
class StoredFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    extracted_data = models.OneToOneField(ExtractedData, ...)
    filepath = models.CharField(max_length=255)
    format_type = models.CharField(max_length=10)
    shared_with = models.ManyToManyField(User, related_name='shared_files')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### View Methods (`connector/views.py`)
```python
class StoredFileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsFileOwnerOrAdmin]
    
    def get_queryset(self):
        user = self.request.user
        # Admin sees all
        if user.is_staff:
            return StoredFile.objects.all()
        # Users see own + shared
        return StoredFile.objects.filter(user=user) | \
               StoredFile.objects.filter(shared_with=user).distinct()
    
    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        """Get access info for a file"""
        file = self.get_object()
        return Response({
            'is_owner': file.user == request.user,
            'is_admin': request.user.is_staff,
            'can_modify': access conditions,
            'can_share': access conditions,
        })
```

### Frontend Implementation

#### FileViewer Component (`app/components/FileViewer.tsx`)
```typescript
interface FileAccess {
  is_owner: boolean;
  is_admin: boolean;
  is_shared_with_me: boolean;
  can_modify: boolean;
  can_share: boolean;
  access_level: string;
}

// Fetch access for each file
const fetchFileAccess = async (fileId: number) => {
  const response = await fetch(`${API_URL}/files/${fileId}/permissions/`);
  const data = await response.json(); // Returns FileAccess
  setFileAccess(prev => ({ ...prev, [fileId]: data }));
}

// Render access badge
const getAccessBadge = (file: StoredFile) => {
  if (access.is_admin) return '👑 Admin';
  if (access.is_owner) return '🔒 Owner';
  if (access.is_shared_with_me) return '📤 Shared';
}

// Control UI elements based on access
<button disabled={!access.can_modify}>Delete</button>
<button disabled={!access.can_share}>Share</button>
```

### API Endpoints

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/files/` | Authenticated | List own + shared files |
| GET | `/api/files/{id}/` | Owner/Admin/Shared | View file details |
| PUT | `/api/files/{id}/` | Owner/Admin | Update file |
| DELETE | `/api/files/{id}/` | Owner/Admin | Delete file |
| POST | `/api/files/{id}/share/` | Owner/Admin | Share with users |
| POST | `/api/files/{id}/unshare/` | Owner/Admin | Revoke access |
| GET | `/api/files/{id}/permissions/` | Authenticated | Get access info |
| GET | `/api/files/{id}/download/` | Owner/Admin/Shared | Download file |

---

## 📈 Results & Observations

### ✅ What Works
- Users only see their authorized files
- Admin has complete oversight
- Shared files respect read-only access
- Delete/modify buttons hidden for non-owners
- Permission badges clearly show access level
- API enforces permissions on all endpoints
- UI matches backend permissions

### 🔍 Testing the System

**Admin View:**
- Sees all 12+ files
- Can delete any file
- Can modify any data
- Can share/unshare anything

**Regular User View:**
- Sees only owned + shared files
- Cannot delete shared files
- Cannot modify shared files
- Can only share own files

**Permission Denial:**
- Attempting API calls without permission returns 403
- UI hides forbidden buttons
- Error messages clear and helpful

---

## 🚀 Next Steps

1. **Implement User Search** - For email-based file sharing
2. **Add Audit Logs** - Track who accessed what
3. **Group Permissions** - Share with departments/groups
4. **Bulk Operations** - Share multiple files at once
5. **Permission History** - See sharing timeline
6. **Export Access Report** - Generate compliance reports

---

## 📞 Support

**Platform:** Data Connector Platform v1.0  
**Last Updated:** April 13, 2026  
**Demo Created By:** System Admin  

For questions or issues, contact the platform administrator.

---

**🔒 Security Note:** This is a demo environment. In production, ensure all passwords are hashed, API calls are HTTPS-only, and audit trails are maintained for compliance.
