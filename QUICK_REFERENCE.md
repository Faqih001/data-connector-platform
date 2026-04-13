# 🚀 RBAC Demo - Quick Start Guide

**Status:** ✅ Demo Data Created and Ready to Test  
**Date:** April 13, 2026  
**Database Connections:** 10 (PostgreSQL, MySQL, MongoDB, ClickHouse)  
**Demo Users:** 4 (Admin + 3 Regular Users)  
**Demo Files:** 18 (with 3 files shared)  

---

## 🎯 Quick Test (5 minutes)

### Step 1: Start Services

**Terminal 1 - Backend:**
```bash
cd ~/Desktop/projects/data-connector-platform/backend
source .venv/bin/activate
python3 manage.py runserver 8001
```

**Terminal 2 - Frontend:**
```bash
cd ~/Desktop/projects/data-connector-platform
npm run dev
```

### Step 2: Open Application

```
http://localhost:3000/
```

### Step 3: Test Each User

#### 👑 Admin Access
- **Login:** `admin` / `admin123`
- **Should See:** 18 files total (all users' files)
- **Actions:** Can delete, modify, share ANY file
- **UI Badge:** 👑 **ADMIN** on all files

#### 🔒 John (Sales)
- **Login:** `john_sales` / `john123`
- **Should See:** 3 files
  - 2 own files (🔒 **OWNER**)
  - 1 shared from sarah (📤 **SHARED**)
- **Actions:** Can modify own files only
- **Try:** Click delete on shared file → button disabled

#### 🔒 Sarah (Analytics)
- **Login:** `sarah_analytics` / `sarah456`
- **Should See:** 3 files
  - 2 own files (🔒 **OWNER**)
  - 1 shared from john (📤 **SHARED**)
- **Actions:** Can modify own files only
- **Note:** Can see 1 file she shares with Mike

#### 🔒 Mike (Reporting)
- **Login:** `mike_reporting` / `mike789`
- **Should See:** 4 files
  - 2 own files (🔒 **OWNER**)
  - 1 shared from john (📤 **SHARED**)
  - 1 shared from sarah (📤 **SHARED**)
- **Actions:** Can only modify own files

---

## 📊 What's Implemented

### ✅ Role-Based Access Control
- [x] Admin full system access
- [x] Users see only own + shared files
- [x] Shared files are read-only
- [x] Admin can manage all files

### ✅ File Sharing System
- [x] Owners can share files
- [x] Shared users get read-only access
- [x] Share/unshare endpoints
- [x] Permission API endpoints

### ✅ UI/UX Features
- [x] Access level badges (👑 Admin, 🔒 Owner, 📤 Shared)
- [x] Conditional button visibility
- [x] Permission display in expanded view
- [x] Disabled actions for unauthorized users

### ✅ API Security
- [x] Permission classes on all endpoints
- [x] Object-level permission checks
- [x] Read vs. write permission separation
- [x] 403 Forbidden for unauthorized access

### ✅ Database Support
- [x] 3 PostgreSQL connections
- [x] 3 MySQL connections
- [x] 3 MongoDB connections
- [x] 1 ClickHouse connection

---

## 📋 Credentials Reference

### Users
| Username | Password | Email | Role |
|----------|----------|-------|------|
| admin | admin123 | admin@platform.local | Super Admin |
| john_sales | john123 | john@company.com | Sales User |
| sarah_analytics | sarah456 | sarah@company.com | Analytics User |
| mike_reporting | mike789 | mike@company.com | Reporting User |

### Database Connections
```
1. PostgreSQL Sales DB            → localhost:5432
2. PostgreSQL Users Database       → 192.168.1.100:5432
3. PostgreSQL Analytics           → analytics.company.com:5432
4. MySQL Customer DB              → mysql.company.local:3306
5. MySQL Inventory System         → inventory.prod.local:3306
6. MySQL Financial Data           → finance-server.internal:3306
7. MongoDB Event Logs             → mongodb.cluster.io:27017
8. MongoDB User Activity          → auth-mongo.internal:27017
9. MongoDB Session Store          → session-db.company.com:27017
10. ClickHouse Metrics            → metrics.analytics.com:9000
```

---

## 🧪 Test Scenarios

### Scenario 1: Admin Oversight
```
1. Login as admin
2. Check file list → See 18 files (all users)
3. Try deleting john's file → Works ✅
4. Try modifying sarah's data → Works ✅
5. Admin badge shown on all files
```

**Result:** ✅ Admin has full access to all files

---

### Scenario 2: User Isolation
```
1. Login as john_sales
2. Check file list → See 3 files (2 own + 1 shared)
3. Try deleting shared file → Button disabled ✅
4. Try modifying shared file → Permission denied ✅
5. Can only see own files + shared
```

**Result:** ✅ Users can only access authorized files

---

### Scenario 3: Shared File Access
```
1. Login as mike_reporting
2. Check file list → See 4 files
3. Expand shared file from john
4. Download button works ✅
5. Delete button disabled ✅
6. Modify button disabled ✅
```

**Result:** ✅ Shared files are read-only

---

### Scenario 4: API Security
```
Open DevTools → Network → Console

As john_sales, try:
curl 'http://localhost:8001/api/files/[sarah_own_file_id]/'

Expected: 403 Forbidden ✅
Message: "Access denied. You can only access files..."
```

**Result:** ✅ API enforces permissions

---

## 📁 Files Created

### Demo Scripts
- `populate_demo_data.py` - Creates users and connections
- `create_demo_files.py` - Creates extracted files with sharing
- `reset_admin.py` - Resets admin password

### Documentation
- `RBAC_DEMO_GUIDE.md` - Comprehensive guide (detailed)
- `QUICK_REFERENCE.md` - This file (quick reference)

### Code Changes
- `connector/permissions.py` - Permission classes
- `connector/serializers.py` - Updated serializers with user info
- `connector/views.py` - RBAC endpoints
- `app/types.ts` - Updated TypeScript types
- `app/components/FileViewer.tsx` - Enhanced with RBAC UI
- `app/lib/api.ts` - Exported API_URL

---

## 🔍 Verification Checklist

### Backend
- [ ] Database connections created (10 total)
- [ ] Demo users created (4 users)
- [ ] Permission classes implemented
- [ ] Share/unshare endpoints working
- [ ] Permissions API endpoint working
- [ ] Files filtered by get_queryset()

### Frontend
- [ ] Users can log in
- [ ] File list shows correct files per user
- [ ] Access badges display correctly
- [ ] Buttons disabled for non-owners
- [ ] Shared file info displays
- [ ] No console errors

### API
- [ ] GET /api/files/ returns filtered list
- [ ] GET /api/files/{id}/permissions/ works
- [ ] DELETE forbidden for non-owners
- [ ] 403 errors shown properly

---

## 🐛 Troubleshooting

### Files Not Showing
```bash
# Verify database data
cd backend
source .venv/bin/activate
python3 manage.py shell
```

```python
from connector.models import StoredFile
for f in StoredFile.objects.all():
    print(f"File: {f.filepath}, Owner: {f.user.username}, Shared: {f.shared_with.count()}")
```

### Login Issues
```bash
# Reset admin password
cd backend
source .venv/bin/activate
python3 reset_admin.py
# Now use: admin / admin123
```

### API Errors
```bash
# Check backend logs
# Terminal running `python3 manage.py runserver 8001`
# Look for 403 or 404 errors
```

---

## 📈 Performance Notes

- Query optimization: Uses `select_related()` and `prefetch_related()`
- Permission checks: Object-level, not resource-level
- File filtering: Done in `get_queryset()` for efficiency
- UI re-renders: Only on file access fetch completion

---

## 🔒 Security Features

1. **Authentication Required** - All file endpoints require login
2. **Object Permissions** - Admin and owner checks on each file
3. **Read vs. Write** - Shared users cannot modify
4. **API Validation** - Permission checks on all endpoints
5. **Serial Number Check** - Prevents ID enumeration
6. **User Isolation** - get_queryset() filters unauthorized files

---

## 📞 Next Steps

### To Make This Production-Ready:

1. **Add Authentication** - OAuth2 / SAML integration
2. **Audit Logs** - Track all file access
3. **Encryption** - Encrypt sensitive data at rest
4. **Rate Limiting** - Prevent API abuse
5. **Two-Factor Auth** - Enhanced security
6. **GDPR Compliance** - Right to be forgotten
7. **Data Retention** - Automatic cleanup policies

---

## 📚 Documentation Files

1. **RBAC_DEMO_GUIDE.md** - Comprehensive technical guide
2. **QUICK_REFERENCE.md** - This quick start (5 min version)

---

**Last Updated:** April 13, 2026  
**Status:** ✅ Ready for Testing  
**Demo Duration:** ~5-10 minutes per test scenario  

Enjoy testing the RBAC system! 🎉
