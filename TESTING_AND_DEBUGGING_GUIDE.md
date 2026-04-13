# 🧪 Testing & Debugging Guide

**Project**: Data Connector Platform  
**Date**: April 13, 2026  
**Status**: Complete with debugging instructions

---

## 🐛 ERRORS ENCOUNTERED & SOLUTIONS

### ERROR 1: Django 404 at Root Path

**Error Message**:
```
Page not found (404)
Request Method:	GET
Request URL:	http://localhost:8001/
Using the URLconf defined in backend.urls, Django tried these URL patterns, in this order:
  admin/
  api/
The empty path didn't match any of these.
```

**Root Cause**: No URL pattern defined for the root path `/` in Django's URL configuration.

**Why This Is OK**: 
- ✅ This is expected behavior
- ✅ All API endpoints are correctly routed to `/api/`
- ✅ The development server is working properly
- ✅ The frontend (Next.js) handles the UI at localhost:3000

**Solution**: This is not an error - it's the correct configuration. Access the app via **http://localhost:3000** instead of http://localhost:8001

---

### ERROR 2: Frontend Form Elements Not Loading

**Error Message**:
```
Failed to load files.
Extract Data
Table Name
Extract Data
Failed to load initial data.
```

**Root Cause Analysis**:
1. **Missing Connection** - No connections created yet (empty dropdown)
2. **API Not Initialized** - Backend API initialization on startup
3. **CORS or Network Issue** - Possible cross-origin resource sharing problem
4. **Database Services Not Running** - Can't establish connections to databases

**Solutions**:

#### Solution A: Ensure Backend is Running ✅
```bash
# Check Django server
ps aux | grep "python manage.py runserver"

# Should show:
# > Starting development server at http://0.0.0.0:8001/

# If not running, start it:
cd /home/amir/Desktop/projects/data-connector-platform/backend
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8001
```

#### Solution B: Start Database Services ✅
```bash
# Start all Docker Compose services
cd /home/amir/Desktop/projects/data-connector-platform
docker-compose up -d

# Verify they're running
docker-compose ps

# Should show:
# NAME               STATUS
# dataconnector-postgres-1    Up
# dataconnector-mysql-1       Up
# dataconnector-mongo-1       Up
# dataconnector-clickhouse-1  Up
```

#### Solution C: Clear Browser Cache ✅
```bash
# Hard refresh in browser
# Press: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
# or use DevTools: Ctrl+Shift+K then Network tab clear cache
```

#### Solution D: Check API Connection ✅
```bash
# Test the API directly
curl -X GET http://localhost:8001/api/connections/

# Expected response:
# {"count":0,"next":null,"previous":null,"results":[]}
```

---

## ✅ STEP-BY-STEP TESTING GUIDE

### STEP 1: Verify Frontend is Running

```bash
# Check if Next.js is running
ps aux | grep "next dev" || ps aux | grep "npm run dev"

# Should show:
# > > Local: http://localhost:3000

# If not running:
cd /home/amir/Desktop/projects/data-connector-platform
npm run dev
```

**Expected Result**: Browser shows http://localhost:3000 with Connection Form

---

### STEP 2: Verify Backend is Running

```bash
# Check Django server
ps aux | grep "python manage.py runserver"

# Should show:
# Starting development server at http://0.0.0.0:8001/

# If not running:
cd /home/amir/Desktop/projects/data-connector-platform/backend
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8001
```

**Expected Result**: Terminal shows "System check identified no issues (0 silenced)"

---

### STEP 3: Start Database Services

```bash
docker-compose up -d
```

**Verify Running**:
```bash
docker-compose ps
```

**Expected Result**:
```
NAME                      STATUS
dataconnector-db-1        Up (PostgreSQL port 5433)
dataconnector-mysql-1     Up (MySQL port 3307)
dataconnector-mongo-1     Up (MongoDB port 27018)
dataconnector-clickhouse-1 Up (ClickHouse port 9001)
```

---

### STEP 4: Test API Endpoints

#### 4a. Test GET Connections Endpoint
```bash
curl -X GET http://localhost:8001/api/connections/
```

**Expected Response**:
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

#### 4b. Test API is Accessible
```bash
curl -I http://localhost:8001/api/
```

**Expected Response**:
```
HTTP/1.1 403 Forbidden
Content-Type: application/json
```

---

### STEP 5: Create First Connection via Frontend

Open **http://localhost:3000** and fill in the form:

#### **Option A: PostgreSQL** (Recommended)

| Field | Value |
|-------|-------|
| **Name** | Test PostgreSQL Connection |
| **Database Type** | PostgreSQL |
| **Host** | localhost |
| **Port** | 5433 |
| **Username** | user |
| **Password** | password |
| **Database Name** | dataconnector |

**Then click**: "Create Connection"

#### **Option B: MySQL**

| Field | Value |
|-------|-------|
| **Name** | Test MySQL Connection |
| **Database Type** | MySQL |
| **Host** | localhost |
| **Port** | 3307 |
| **Username** | user |
| **Password** | password |
| **Database Name** | testdb |

#### **Option C: MongoDB**

| Field | Value |
|-------|-------|
| **Name** | Test MongoDB Connection |
| **Database Type** | MongoDB |
| **Host** | localhost |
| **Port** | 27018 |
| **Username** | (leave blank) |
| **Password** | (leave blank) |
| **Database Name** | test |

#### **Option D: ClickHouse**

| Field | Value |
|-------|-------|
| **Name** | Test ClickHouse Connection |
| **Database Type** | ClickHouse |
| **Host** | localhost |
| **Port** | 9001 |
| **Username** | default |
| **Password** | (leave blank) |
| **Database Name** | default |

**Expected Result**: Connection appears in "Connections" list below

---

### STEP 6: Extract Data

1. **Select Connection**: Choose from "Select a connection" dropdown
2. **Enter Table Name**: 
   - PostgreSQL: `information_schema.schemata`
   - MySQL: `information_schema.columns`
   - MongoDB: `test` (collection name)
   - ClickHouse: `system.tables`
3. **Click**: "Extract Data"

**Expected Result**: Data grid populates with table data

---

### STEP 7: Edit Data

1. **Click any cell** in the data grid
2. **Type to edit** the value
3. **Click outside** the cell to save locally

**Expected Result**: Cell value updates and shows in grid

---

### STEP 8: Submit Changes

1. **After editing**: Click "Submit Data"
2. **Check backend logs** for confirmation

**Expected Result**: Changes saved to backend storage

---

## 🔧 DEBUGGING CHECKLIST

### If "Failed to load files" appears:

- [ ] Backend running? `ps aux | grep "python manage.py"`
- [ ] Port 8001 listening? `lsof -i :8001`
- [ ] Frontend can reach backend? Check browser DevTools Network tab
- [ ] CORS enabled? Check backend/connector/views.py for @permission_classes
- [ ] API responding? `curl http://localhost:8001/api/connections/`

### If "Failed to load initial data" appears:

- [ ] Connection created? Check "Connections" list
- [ ] Database service running? `docker-compose ps`
- [ ] Correct credentials entered? Test with app/lib/api.ts values
- [ ] Network connectivity? `ping localhost`

### If data grid doesn't show:

- [ ] Table name exists? Try `information_schema.schemata`
- [ ] Database has data? Check directly with DB client
- [ ] Extract button clicked? Watch for "Extracting..." state
- [ ] Backend error? Check terminal for error messages

### If Submit Data fails:

- [ ] API key/auth? Check backend authentication setup
- [ ] File permissions? Check storage directory exists
- [ ] Valid JSON? Grid data must be valid
- [ ] Backend error? Check terminal logs

---

## 🚀 FULL STARTUP SEQUENCE

Run these commands in order:

```bash
# 1. Navigate to project
cd /home/amir/Desktop/projects/data-connector-platform

# 2. Start Docker services (databases)
docker-compose up -d

# 3. Verify Docker services started
docker-compose ps

# 4. In one terminal: Start backend
cd backend
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8001

# 5. In another terminal: Start frontend
cd /home/amir/Desktop/projects/data-connector-platform
npm run dev

# 6. Open browser
# http://localhost:3000
```

**All startup indicators should show**:
- ✅ Frontend: "Local: http://localhost:3000"
- ✅ Backend: "Starting development server at http://0.0.0.0:8001/"
- ✅ Databases: docker-compose ps shows 4 services "Up"

---

## 📊 EXPECTED BEHAVIOR

| Action | Expected Result | If Not Working |
|--------|-----------------|----------------|
| Load localhost:3000 | See Connection Form | Check npm run dev |
| Fill form + Create | Connection in list | Check API running at 8001 |
| Select connection | Can pick from dropdown | Get latest connections first |
| Extract data | Grid populates | Check table name is correct |
| Edit grid cell | Value updates locally | Should work instantly |
| Submit data | Success message | Check backend permissions |
| Open files | See JSON files list | Check storage directory |

---

## 🔍 ENDPOINT TESTS

### Create Connection
```bash
curl -X POST http://localhost:8001/api/connections/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "db_type": "postgres",
    "host": "localhost",
    "port": 5433,
    "username": "user",
    "password": "password",
    "database_name": "dataconnector"
  }'
```

### Get Connections
```bash
curl -X GET http://localhost:8001/api/connections/
```

### Extract Data
```bash
curl -X POST http://localhost:8001/api/connections/1/extract/ \
  -H "Content-Type: application/json" \
  -d '{"table_name": "information_schema.schemata"}'
```

### Get Files
```bash
curl -X GET http://localhost:8001/api/stored-files/
```

---

## 📝 LOGS TO CHECK

### Backend Logs
Watch for in terminal running Django:
```
[timestamp] "GET /api/connections/ HTTP/1.1" 200
[timestamp] "POST /api/connections/ HTTP/1.1" 201
[timestamp] "POST /api/connections/1/extract/ HTTP/1.1" 200
```

### Browser Console
Open DevTools (F12 → Console):
```
✅ Successful: Network requests show 200/201 status
❌ Error: Check for red error messages
```

### Docker Logs
```bash
# Check specific service
docker-compose logs postgres
docker-compose logs mysql
docker-compose logs mongo
docker-compose logs clickhouse
```

---

## ✨ VERIFICATION CHECKLIST

After completing above steps, verify:

- [ ] Frontend loads (http://localhost:3000)
- [ ] Backend running (port 8001)
- [ ] Database services running (docker-compose ps)
- [ ] API endpoints responding (curl tests work)
- [ ] Can create connection (appears in list)
- [ ] Can extract data (grid populates)
- [ ] Can edit cells (values change)
- [ ] Can submit data (no errors)
- [ ] Can view files (list appears)

**If all checkboxes are ✅**: Application is working perfectly!

---

## 🎯 QUICK REFERENCE

| Issue | Quick Fix |
|-------|-----------|
| 404 at root | Access localhost:3000 not 8001 |
| Failed to load files | Start docker-compose services |
| API not responding | Check `lsof -i :8001` |
| No connections | Create one via form first |
| Data not showing | Verify table name exists |
| Edit not working | Click cell to activate edit mode |
| Submit fails | Check browser console for errors |
| Port already in use | `kill -9 $(lsof -t -i :8001)` |

---

## 📞 Support

**If still having issues**:

1. Check all terminal outputs for error messages
2. Review browser DevTools Network tab for failed requests
3. Check Docker logs: `docker-compose logs`
4. Verify all services with: `docker-compose ps`
5. Try restarting all services: `docker-compose restart`

---

**Everything is configured and ready to test!** 🚀
