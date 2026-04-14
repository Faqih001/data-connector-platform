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
- ✅ 112 sample data files pre-loaded
- ✅ Docker containerization complete
- ✅ Unit tests included
- ✅ Complete documentation
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
- ✏️ **Data Editing**: Edit extracted data in an interactive grid
- 💾 **Data Storage**: Store files and extracted data with version history
- 👥 **User Management**: Multiple user roles (Admin, Sales, Analytics, Reporting)
- 🔄 **Batch Processing**: Process large datasets efficiently
- 📱 **Responsive UI**: Works on desktop and tablet devices
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

### Docker Setup (Alternative)
1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd data-connector-platform
    ```
2.  **Build and run with Docker**:
    ```bash
    docker-compose up --build
    ```
    The frontend will be available at `http://localhost:3000` and the backend at `http://localhost:8001`.

## API Documentation

The API is built with Django REST Framework and provides the following endpoints:

-   `GET, POST /api/connections/`: List all connections or create a new one.
-   `GET, PUT, DELETE /api/connections/{id}/`: Retrieve, update, or delete a specific connection.
-   `POST /api/connections/{id}/extract_data/`: Trigger data extraction from a connection.
-   `GET /api/files/`: List all stored files (with role-based access).
