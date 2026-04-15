# Database Connection & Table Creation Tests

## Overview
Comprehensive test suite for the Data Connector Platform supporting 4 database types:
- PostgreSQL 13
- MySQL 8.0
- MongoDB 4.4
- ClickHouse (latest)

## Test Files

### 1. **test_all_databases.py** - Comprehensive All-in-One Test
- Tests all 4 databases sequentially
- Creates test tables/collections for each
- Verifies creation with database-specific queries
- Provides summary report
- **Usage:** `python test_all_databases.py`
- **Expected Output:** All 4 databases PASS

### 2. **test_postgresql.py** - PostgreSQL Specific Test
- Tests PostgreSQL connection
- Creates `test_connection_postgresql` table
- Verifies table existence
- Inserts and queries test data
- **Usage:** `python test_postgresql.py`
- **Expected:** ✅ PostgreSQL connection test PASSED

### 3. **test_mysql.py** - MySQL Specific Test
- Tests MySQL connection
- Creates `test_connection_mysql` table
- Verifies table existence
- Inserts and queries test data
- **Usage:** `python test_mysql.py`
- **Expected:** ✅ MySQL connection test PASSED

### 4. **test_mongodb.py** - MongoDB Specific Test
- Tests MongoDB connection
- Creates `test_connection_mongodb` collection
- Inserts test document
- Verifies collection existence
- **Usage:** `python test_mongodb.py`
- **Expected:** ✅ MongoDB connection test PASSED

### 5. **test_clickhouse.py** - ClickHouse Specific Test
- Tests ClickHouse connection
- Creates `test_connection_clickhouse` table
- Verifies table existence
- Inserts and queries test data
- **Usage:** `python test_clickhouse.py`
- **Expected:** ✅ ClickHouse connection test PASSED

### 6. **run_all_tests.sh** - Test Runner Script
- Bash script to run all tests sequentially
- Activates Python virtual environment
- Sets proper Django settings
- Displays formatted output
- **Usage:** `bash run_all_tests.sh`
- **Output:** Summary of all test results

## Test Database Configurations

### PostgreSQL
- Host: localhost
- Port: 5433 (Docker mapping)
- Username: user
- Password: password
- Database: dataconnector

### MySQL
- Host: localhost
- Port: 3307 (Docker mapping)
- Username: user
- Password: password
- Database: testdb

### MongoDB
- Host: localhost
- Port: 27018 (Docker mapping)
- No authentication required
- Database: test_mongodb

### ClickHouse
- Host: localhost
- Port: 9001 (Docker mapping for native TCP)
- Username: default (no password)
- Database: default

## Features Tested

### Connection Management
✅ Create connections for each database type
✅ Store encrypted credentials
✅ Verify connection parameters

### Table/Collection Creation
✅ PostgreSQL: CREATE TABLE with serial ID, varchar, and timestamp
✅ MySQL: CREATE TABLE with auto_increment ID
✅ MongoDB: Auto-create collections on first insert
✅ ClickHouse: CREATE TABLE with MergeTree engine

### Data Operations
✅ Insert test data
✅ Query verification
✅ Collection existence verification

### Error Handling
✅ Connection failures with helpful messages
✅ Permission errors
✅ Database-specific error handling

## Backend Fixes Applied

### CSRF Token Security
- Added `@ensure_csrf_cookie` to csrf_token_view
- Added `@ensure_csrf_cookie` to login_view
- Ensures CSRF cookies are properly set for all POST requests

### Connector Fixes
- Fixed MongoConnector import (MongoDBConnector → MongoConnector)
- Fixed ClickHouse cursor method (direct execute instead of cursor)
- Fixed ClickHouse close method (override that does nothing)

### Port Mappings (Docker Compose)
- PostgreSQL: 5433:5432
- MySQL: 3307:3306
- MongoDB: 27018:27017
- ClickHouse: 9001:9000

## UI/API Testing Completed

### Connection Creation UI
✅ Tested creating new connection through web interface
✅ Form validation working correctly
✅ Connection saved successfully
✅ Success toast notification displayed

### Table Creation Feature
✅ Table creation form visible when no tables exist
✅ SQL template loading for selected database
✅ Table name field working
✅ Create Table button executes successfully
✅ Success toast notification shows table name
✅ Form resets after successful creation

### Error Handling UI
✅ Toast notifications for errors
✅ Helpful error messages displayed
✅ Failed connections show detailed error text

## How to Run Tests

### Run All Tests
```bash
bash tests/run_all_tests.sh
```

### Run Individual Database Test
```bash
cd backend
source .venv/bin/activate
python ../tests/test_postgresql.py  # or test_mysql.py, test_mongodb.py, test_clickhouse.py
```

### Run Comprehensive Test Only
```bash
cd backend
source .venv/bin/activate
python ../tests/test_all_databases.py
```

## Test Results Summary (Latest Run)

```
================================================================================
                    🧪 FINAL DATABASE TEST - ALL 4 DATABASES                     
================================================================================

[1] PostgreSQL
    ✅ PASS - PostgreSQL table creation working

[2] MySQL
    ✅ PASS - MySQL table creation working

[3] MongoDB
    ✅ PASS - MongoDB collection creation working

[4] ClickHouse
    ✅ PASS - ClickHouse table creation working

================================================================================
                                 📊 TEST SUMMARY                                 
================================================================================
  PostgreSQL           ✅ PASS
  MySQL                ✅ PASS
  MongoDB              ✅ PASS
  ClickHouse           ✅ PASS

                              🎉 ALL TESTS PASSED!                               
================================================================================
```

## Key Accomplishments

1. ✅ **All 4 databases working end-to-end**
2. ✅ **Table creation feature fully functional**
3. ✅ **CSRF token security properly implemented**
4. ✅ **User-friendly UI with success notifications**
5. ✅ **Comprehensive test coverage for all database types**
6. ✅ **Database-specific SQL templates**
7. ✅ **Error handling and validation**

## Next Steps for Future Testing

- Performance testing with large datasets
- Stress testing with concurrent connections
- Integration testing with data extraction
- UI end-to-end testing with Selenium/Playwright
- Load testing with multiple users
- Backup and recovery testing
- Security penetration testing

## Troubleshooting

### Connection Refused
- Ensure Docker containers are running: `docker-compose up -d`
- Verify port mappings match configuration
- Check database credentials

### CSRF Token Errors
- Clear browser cookies and login again
- Ensure backend is restarted after code changes
- Verify `@ensure_csrf_cookie` decorators are applied

### Port Conflicts
- Check what's using the ports: `netstat -tlnp | grep <port>`
- Update port mappings in docker-compose.yml if needed

## References

- PostgreSQL: psycopg2 library
- MySQL: mysql-connector library
- MongoDB: pymongo library
- ClickHouse: clickhouse-driver library
- Django REST Framework for API layer
- Next.js for frontend UI
