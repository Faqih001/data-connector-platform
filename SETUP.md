# 📋 Data Connector Platform - Setup Guide

**Last Updated:** April 14, 2026 | **Status:** ✅ Production Ready

Complete setup instructions for the Data Connector Platform. Choose the setup method that works best for you.

---

## 📑 Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start (Automated)](#quick-start-automated)
3. [Manual Setup](#manual-setup)
4. [Running the Application](#running-the-application)
5. [Database Configuration](#database-configuration)
6. [Demo Credentials](#demo-credentials)
7. [Development Tips](#development-tips)
8. [Troubleshooting](#troubleshooting)
9. [Docker Setup](#docker-setup)

---

## 🖥️ System Requirements

### Minimum Requirements
- **Node.js:** v16 or higher
- **Python:** v3.8 or higher
- **npm:** v7 or higher
- **pip:** v21 or higher

### Recommended Requirements
- **Node.js:** v18 LTS or higher
- **Python:** v3.10 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 500MB minimum

### Supported Platforms
- ✅ Linux (Ubuntu 20.04+, Debian 11+)
- ✅ macOS (10.15+)
- ✅ Windows 10/11 (with WSL2 recommended)

### Verify Your Installation
```bash
node --version    # Should be v16+
npm --version     # Should be v7+
python3 --version # Should be v3.8+
pip3 --version    # Should be v21+
```

---

## ⚡ Quick Start (Automated)

The automated setup scripts handle all installation and configuration for you.

### Linux / macOS

```bash
# 1. Navigate to project folder
cd /path/to/data-connector-platform

# 2. Make setup script executable
chmod +x setup.sh

# 3. Run the setup script
bash setup.sh
```

The script will:
- ✅ Check prerequisites
- ✅ Install Node.js dependencies
- ✅ Set up Python virtual environment
- ✅ Install Python dependencies
- ✅ Initialize database
- ✅ Create demo data
- ✅ Display next steps

### Windows

```powershell
# 1. Open Command Prompt or PowerShell as Administrator
# 2. Navigate to project folder
cd \path\to\data-connector-platform

# 3. Run the setup batch file
setup.bat
```

---

## 📖 Manual Setup

Follow these steps if you prefer manual installation or the automated setup doesn't work.

### Step 1: Install Node.js Dependencies

```bash
cd /path/to/data-connector-platform
npm install
```

This installs all frontend dependencies and scripts.

### Step 2: Set Up Python Environment

#### Option A: Using venv (Recommended)
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

#### Option B: Using conda
```bash
conda create -n data-connector python=3.10
conda activate data-connector
cd backend
```

### Step 3: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Initialize Database

```bash
cd backend

# Run migrations
python manage.py migrate

# Create demo data (optional but recommended)
python manage.py shell
# In the shell, run:
# from connector.models import User, Connection, StoredFile
# ... or use setup_demo_users.py

exit() # or Ctrl+D
```

### Step 5: Create Demo Users

```bash
cd backend
python setup_demo_users.py
```

This creates 4 demo users with different roles:
- **admin** / **admin123** (Administrator)
- **john_sales** / **john123** (Sales role)
- **sarah_analytics** / **sarah456** (Analytics role)
- **mike_reporting** / **mike789** (Reporting role)

### Step 6: Populate Demo Data (Optional)

```bash
cd backend
python populate_demo_data.py
```

This adds sample database connections and test data.

---

## 🚀 Running the Application

### Terminal Setup

You'll need **two terminal windows** - one for the backend, one for the frontend.

### Terminal 1: Start Backend (Django)

```bash
# From project root
npm run backend

# Or manually:
cd backend
python manage.py runserver 8001
```

Backend will start on `http://localhost:8001`

**Backend endpoints:**
- API: `http://localhost:8001/api/`
- Admin: `http://localhost:8001/admin/`
- Browsable API: `http://localhost:8001/api/connections/`

### Terminal 2: Start Frontend (Next.js)

```bash
# From project root, in a NEW terminal
npm run frontend

# Or manually:
npm run dev
```

Frontend will start on `http://localhost:3000`

### Access the Application

Open your browser and go to:
```
http://localhost:3000
```

You should see the login page. Use any of the demo credentials to log in.

---

## 🗄️ Database Configuration

### Supported Databases

The platform supports connections to:
- ✅ **PostgreSQL** (v10+)
- ✅ **MySQL** (v5.7+)
- ✅ **MongoDB** (v3.6+)
- ✅ **ClickHouse** (v20+)

### Setting Up a Test Connection

1. Log in to the application
2. Click **"Add Connection"** button
3. Fill in connection details:

#### PostgreSQL Example
```
Database Type: PostgreSQL
Host: localhost
Port: 5432
Database: test_db
Username: postgres
Password: your_password
```

4. Click **"Test Connection"** to verify
5. Click **"Save Connection"** if test succeeds

### Application Database (SQLite)

The Django backend uses SQLite by default for storing:
- User accounts
- Saved connections
- File metadata
- Access logs

**Database file location:** `backend/db.sqlite3`

To reset the application database:
```bash
cd backend
rm db.sqlite3
python manage.py migrate
python setup_demo_users.py
```

---

## 👤 Demo Credentials

Four demo users are pre-configured with different roles:

| Username | Password | Role | Access |
|----------|----------|------|--------|
| `admin` | `admin123` | Administrator | Full access to all features |
| `john_sales` | `john123` | Sales | Can create connections, extract data |
| `sarah_analytics` | `sarah456` | Analytics | Read-only access, can view analytics |
| `mike_reporting` | `mike789` | Reporting | Can generate reports, view dashboards |

### First Time Login

1. Navigate to `http://localhost:3000`
2. Enter username and password
3. Click **"Sign In"**
4. You'll be redirected to the dashboard

### Resetting User Password

```bash
cd backend
python reset_admin.py  # Resets admin user to admin123
```

Or create a custom Django admin user:
```bash
cd backend
python manage.py createsuperuser
```

---

## 💡 Development Tips

### Project Structure Overview

```
data-connector-platform/
├── app/                    # Next.js frontend
│   ├── api/               # Backend API routes
│   ├── components/        # React components
│   ├── lib/               # Utility functions
│   └── page.tsx           # Main page
├── backend/               # Django backend
│   ├── connector/         # Main app (models, views, serializers)
│   ├── backend/           # Django configuration
│   ├── manage.py          # Django CLI
│   └── requirements.txt    # Python dependencies
├── public/                # Static assets
├── package.json           # Node.js dependencies
├── tsconfig.json          # TypeScript config
├── next.config.ts         # Next.js config
└── docker-compose.yml     # Docker configuration
```

### Useful npm Commands

```bash
# Install dependencies
npm install

# Start frontend (development)
npm run dev

# Start backend
npm run backend

# Build frontend
npm run build

# Start production build
npm start

# Run linting
npm run lint
```

### Useful Django Commands

```bash
cd backend

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Start server
python manage.py runserver

# Open interactive shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test
```

### API Endpoints Reference

#### Connections
```
GET    /api/connections/        # List all connections
POST   /api/connections/        # Create new connection
GET    /api/connections/{id}/   # Get connection details
PUT    /api/connections/{id}/   # Update connection
DELETE /api/connections/{id}/   # Delete connection
POST   /api/connections/{id}/test/  # Test connection
```

#### Files
```
GET    /api/files/              # List all files
POST   /api/files/              # Upload file
GET    /api/files/{id}/         # Get file details
DELETE /api/files/{id}/         # Delete file
```

#### Extraction
```
POST   /api/extract/            # Extract data from connection
```

#### Submission
```
POST   /api/submit/             # Submit processed data
```

### Code Editor Extensions (VS Code)

Recommended extensions:
- **ES7+ React/Redux/React-Native snippets**
- **Python**
- **Pylance**
- **Django**
- **Tailwind CSS IntelliSense**
- **TypeScript Vue Plugin**
- **REST Client** (for API testing)

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Issue: "Port 3000 is already in use"

```bash
# Find process using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use different port
npm run dev -- --port 3001
```

#### Issue: "Port 8001 is already in use"

```bash
# Find process using port 8001
lsof -i :8001

# Kill the process
kill -9 <PID>

# Or use different port
cd backend && python manage.py runserver 8002
```

#### Issue: "ModuleNotFoundError: No module named 'django'"

```bash
# Make sure you're in the backend directory
cd backend

# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate      # Windows

# Reinstall requirements
pip install -r requirements.txt
```

#### Issue: "npm ERR! Cannot find module 'next'"

```bash
# Clear npm cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Issue: "database is locked" (SQLite)

```bash
# This usually means two processes are accessing the database
# Kill all Django processes and try again:
pkill -f "manage.py"

# Or remove any .sqlite3 lock files:
rm backend/db.sqlite3-journal
```

#### Issue: Connection test fails

Check these things:
1. ✅ Database host and port are correct
2. ✅ Database credentials are accurate
3. ✅ Database is running and accessible
4. ✅ Firewall isn't blocking the connection
5. ✅ Network connectivity is working

Try connecting directly from your machine:
```bash
# PostgreSQL
psql -h host -U username -d database

# MySQL
mysql -h host -u username -p database

# MongoDB
mongosh "mongodb://host:port/database"
```

---

## 🐳 Docker Setup

### Using Docker Compose

Build and run the entire stack in containers:

```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8001`

### Building Individual Containers

```bash
# Frontend
docker build -f Dockerfile.frontend -t data-connector-frontend .
docker run -p 3000:3000 data-connector-frontend

# Backend
docker build -f Dockerfile.backend -t data-connector-backend .
docker run -p 8001:8001 data-connector-backend
```

---

## 📞 Support & Resources

### Documentation
- [README.md](README.md) - Project overview
- [CORE_FEATURES.md](CORE_FEATURES.md) - Feature documentation
- [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) - Architecture decisions
- [TECHNICAL_SPECIFICATIONS.md](TECHNICAL_SPECIFICATIONS.md) - Technical details
- [NAVIGATION_AND_USER_GUIDE.md](NAVIGATION_AND_USER_GUIDE.md) - User guide

### Quick Links
- **Frontend Code:** `app/` directory
- **Backend Code:** `backend/connector/` directory
- **API Tests:** `test-files-api.html`
- **Integration Tests:** `integration-test-ports.sh`

### Getting Help

1. Check the [Troubleshooting](#troubleshooting) section
2. Review relevant documentation file
3. Check Python/Node.js error messages carefully
4. Verify system requirements are met
5. Try the automated setup script first

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Both terminals show no errors
- [ ] Frontend loads at `http://localhost:3000`
- [ ] Backend API accessible at `http://localhost:8001/api/`
- [ ] Can log in with demo credentials
- [ ] Can see demo database connections
- [ ] Can create a new connection
- [ ] Can test a connection successfully
- [ ] Can view extracted data in the grid
- [ ] No browser console errors (F12)
- [ ] No terminal errors

If all items pass, your setup is complete! 🎉

---

**Ready to get started?** [Go back to README.md](README.md)
