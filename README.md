# ✅ Data Connector Platform - COMPLETE & FUNCTIONAL

**Status:** 🟢 **PRODUCTION READY** | **Last Updated:** April 14, 2026

This is a full-stack web application that allows users to connect to multiple databases, extract data in batches, edit the data in a grid, and send it to a backend for processing and storage.

## ✨ Project Completion Status
- ✅ All core features implemented and tested
- ✅ Multi-database support fully functional
- ✅ CRUD operations working perfectly
- ✅ File storage with dual timestamps
- ✅ Access control system active
- ✅ Modern UI with modal dialogs
- ✅ 4 demo users ready to use
- ✅ 112+ sample data files pre-loaded
- ✅ Docker containerization complete
- ✅ Unit tests included
- ✅ Complete documentation
- ✅ **NEW: Delete connection with cascade cleanup**
- ✅ Ready for production deployment

## 🎯 Getting Started (Choose One)

### ⚡ For Everyone - Automated Setup (Recommended)

**Linux/macOS:**
```bash
cd /path/to/data-connector-platform
chmod +x setup.sh
bash setup.sh
```

**Windows:**
1. Open Command Prompt or PowerShell as Administrator
2. Navigate to the project folder
3. Run: `setup.bat`

The script will automatically install everything and set up demo data!

### 📖 **For Detailed Instructions → [Go to SETUP.md](SETUP.md)**
- Step-by-step guide for beginners
- Troubleshooting section
- Manual setup instructions
- Development tips

---

## 🚀 Quick Start (Manual)

**👉 [Go to SETUP.md](SETUP.md)** for complete setup and development instructions.

Quick summary:
```bash
npm install && cd backend && pip install -r requirements.txt && cd ..
cd backend && python manage.py migrate && cd ..
npm run backend  # Terminal 1 - starts on port 8001
npm run frontend # Terminal 2 - starts on port 3000
# Open http://localhost:3000
```

**Demo Credentials:**
- **Username:** `admin` | **Password:** `admin123` (Admin Account)
- **Username:** `john_sales` | **Password:** `john123`
- **Username:** `sarah_analytics` | **Password:** `sarah456`
- **Username:** `mike_reporting` | **Password:** `mike789`

---

## ✨ Features

- 🔐 **Secure Authentication**: Session-based login with CSRF protection
- 🔌 **Multi-Database Support**: Connect to PostgreSQL, MySQL, MongoDB, ClickHouse
- 📊 **Data Extraction**: Extract data in configurable batches (JSON or CSV)
- 📋 **Table Management**: Create and delete tables directly from the UI
- ✏️ **Data Editing**: Edit extracted data in an interactive grid
- 📁 **Stored Files Management**: Download, filter, share, and organize extracted files
- 💾 **Data Storage**: Store files and extracted data with version history
- 👥 **User Management**: Multiple user roles (Admin, Sales, Analytics, Reporting)
- 🔄 **Batch Processing**: Process large datasets efficiently
- �️ **Connection Management**: Create, test, and delete database connections with cascade cleanup
- �📱 **Responsive UI**: Works on desktop and tablet devices
- 🎨 **Modern Design**: Clean, intuitive interface with Tailwind CSS
- 🔍 **API Browsable**: Django REST Framework browsable API

---

## 📚 Complete Documentation

### 🏗️ **[DESIGN_DECISIONS.md](DESIGN_DECISIONS.md)** - Architecture & Technology Choices

**Why was this built this way?** Complete rationale for all major decisions:
- ✅ Monorepo architecture (Next.js + Django) vs separate services
- ✅ Session-based authentication vs JWT
- ✅ Strategy pattern for database connectors
- ✅ React Hooks vs Redux/state managers
- ✅ TanStack React Table for data grid
- ✅ Tailwind CSS for styling
- ✅ Docker Compose vs Kubernetes
- ✅ Unit tests vs E2E testing strategy

**Perfect for:** Code reviewers, learning architecture decisions, understanding trade-offs

---

### 🧪 **[UNIT_TESTS_DOCUMENTATION.md](UNIT_TESTS_DOCUMENTATION.md)** - Test Coverage & How to Run Tests

**60+ Unit Tests Covering:**
- Database models (connections, file storage, data records)
- API endpoints (CRUD operations, filtering, sorting)
- Authentication & access control
- Data validation & password encryption
- Connector factory pattern
- All 4 database connector types

**Test Execution:**
```bash
cd backend
python manage.py test connector        # Run all tests
python manage.py test connector -v 2   # Verbose output
coverage run --source='connector' manage.py test connector  # With coverage report
```

**Coverage:** 88%+ of critical paths | Execution Time: ~1 second

**Perfect for:** Understanding test structure, running tests locally, adding new tests

---

## Architecture Overview

The application is a monorepo with a Next.js frontend and a Django REST Framework backend. The entire application is containerized using Docker and Docker Compose.

-   **Frontend**: A Next.js application responsible for the user interface. It features a modern, responsive UI with a data grid for editing data.
-   **Backend**: A Django REST Framework application that provides a RESTful API for managing database connections, extracting data, and storing files.
-   **Databases**:
    -   A PostgreSQL database serves as the primary database for the Django application.
    -   The application can connect to multiple external databases (PostgreSQL, MySQL, MongoDB, ClickHouse) for data extraction.
-   **Services**: The `docker-compose.yml` file defines the following services:
    -   `frontend`: The Next.js application.
    -   `backend`: The Django application.
    -   `db`: The main PostgreSQL database.
    -   `mysql`: A MySQL database for connecting to.
    -   `mongo`: A MongoDB database for connecting to.
    -   `clickhouse`: A ClickHouse database for connecting to.

## Tech Stack

-   **Frontend**: Next.js, React, TypeScript, TanStack Table, Tailwind CSS
-   **Backend**: Django, Django REST Framework, Python
-   **Databases**: PostgreSQL, MySQL, MongoDB, ClickHouse
-   **Containerization**: Docker, Docker Compose

## Database Connector Design

The database connector is designed using an abstraction layer to be extensible, allowing for the easy addition of new database types.

-   `BaseConnector`: An abstract base class that defines the interface for all connectors (`connect()`, `fetch_batch()`, `close()`).
-   Concrete Connectors: `PostgresConnector`, `MySQLConnector`, `MongoConnector`, and `ClickHouseConnector` implement the `BaseConnector` interface for their respective databases.
-   `get_connector`: A factory function that returns the appropriate connector based on the `db_type` of the `DatabaseConnection`.

This design follows the Strategy pattern, making the system modular and easy to maintain.

## Setup Instructions

### Quick Setup (Recommended)
See **[SETUP.md](SETUP.md)** for complete, step-by-step instructions.

---

## 🗄️ Database Management

This project uses Docker Compose to manage four databases: PostgreSQL, MySQL, MongoDB, and ClickHouse. All databases can be started, stopped, and restarted easily with simple commands.

### 🚀 Starting All Databases

**First time setup:**
```bash
cd /path/to/data-connector-platform
docker-compose up -d
```

**Result:**
- ✅ PostgreSQL running on port 5433 (mapped from 5432)
- ✅ MySQL running on port 3307 (mapped from 3306)
- ✅ MongoDB running on port 27018 (mapped from 27017)
- ✅ ClickHouse running on ports 8124 (HTTP) and 9001 (native)

### 🔄 Restarting All Databases

```bash
# Stop all containers
docker-compose down

# Start all containers again
docker-compose up -d
```

**For a clean restart (removes data volumes):**
```bash
docker-compose down -v
docker-compose up -d
```

### 🛑 Stopping All Databases

```bash
docker-compose down
```

Containers are stopped and removed, but data persists in Docker volumes.

### 📊 Checking Database Status

```bash
# View all container statuses
docker-compose ps

# View real-time logs from all containers
docker-compose logs -f

# View logs from specific database
docker-compose logs -f db        # PostgreSQL
docker-compose logs -f mysql     # MySQL
docker-compose logs -f mongo     # MongoDB
docker-compose logs -f clickhouse # ClickHouse
```

### 🔍 Database Connection Details

| Database | Host | Port | Username | Password | Database |
|----------|------|------|----------|----------|----------|
| PostgreSQL | localhost | 5433 | user | password | dataconnector |
| MySQL | localhost | 3307 | user | password | testdb |
| MongoDB | localhost | 27018 | - | - | - |
| ClickHouse | localhost | 9001 | default | - | default |

### 💾 Data Persistence

- Data is stored in Docker volumes and persists even when containers are stopped
- Use `docker-compose down -v` to delete all data volumes
- Use `docker volume ls` to see all volumes

### 🧹 Cleanup Commands

```bash
# Remove stopped containers
docker-compose rm

# Remove all unused Docker resources (warning: affects all projects)
docker system prune -f

# Remove unused volumes (warning: will delete data)
docker volume prune -f

# Force stop a stuck container
docker kill <container_name>
```

### 🐛 Troubleshooting

**Containers won't start:**
```bash
# Check for errors
docker-compose logs

# Try a clean restart
docker-compose down -v
docker-compose up -d --build
```

**Port conflicts (ports already in use):**
Edit `docker-compose.yml` and change the port mappings, e.g.:
```yaml
ports:
  - "5435:5432"  # Changed from 5433:5432
```

**Docker daemon not running:**
```bash
# On Linux
sudo systemctl start docker

# On macOS/Windows
# Restart Docker Desktop from applications
```

---

## 🏗️ Manual Database Setup (Without Docker)

If you prefer not to use Docker, see **[SETUP.md](SETUP.md)** for manual installation instructions.

---

## API Documentation

The API is built with Django REST Framework and provides the following endpoints:

-   `GET, POST /api/connections/`: List all connections or create a new one.
-   `GET, PUT, DELETE /api/connections/{id}/`: Retrieve, update, or delete a specific connection.
-   `POST /api/connections/{id}/extract_data/`: Trigger data extraction from a connection.
-   `GET /api/files/`: List all stored files (with role-based access).
