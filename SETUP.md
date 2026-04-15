# 📋 Data Connector Platform - Setup Guide

**Last Updated:** 14 April, 2026 | **Status:** ✅ Production Ready

Complete setup instructions for the Data Connector Platform with step-by-step procedures, database configuration, Docker setup, and troubleshooting.

---

## 📑 Table of Contents

1. [System Requirements & Verification](#system-requirements-and-verification)
2. [Prerequisites Check](#prerequisites-check)
3. [Quick Start (Automated)](#quick-start-automated)
4. [Manual Setup (Sequential Steps)](#manual-setup-sequential-steps)
5. [Database Setup & Verification](#database-setup-and-verification)
6. [Starting the Application](#starting-the-application)
7. [Docker Setup (Start, Restart, Troubleshoot)](#docker-setup-start-restart-troubleshoot)
8. [Demo Credentials](#demo-credentials)
9. [Development Tips](#development-tips)
10. [Troubleshooting](#troubleshooting)
11. [Verification Checklist](#verification-checklist)

---

## 🖥️ System Requirements and Verification

### Minimum Requirements
- **Node.js:** v16 or higher
- **Python:** v3.8 or higher
- **npm:** v7 or higher
- **pip:** v21 or higher
- **Docker & Docker Compose:** (optional, for Docker setup)

### Recommended Requirements
- **Node.js:** v18 LTS or higher
- **Python:** v3.10 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 500MB minimum

### Supported Platforms
- ✅ Linux (Ubuntu 20.04+, Debian 11+)
- ✅ macOS (10.15+)
- ✅ Windows 10/11 (with WSL2 recommended)

---

## ✅ Prerequisites Check

### Step 1: Verify Required Tools Are Installed

Run these commands to verify your system:

```bash
# Check Node.js
node --version    # Should be v16 or higher
npm --version     # Should be v7 or higher

# Check Python
python3 --version # Should be v3.8 or higher
pip3 --version    # Should be v21 or higher

# (Optional) Check Docker
docker --version  # Only needed for Docker setup
docker-compose --version
```

**Expected Output Examples:**
```
v18.17.0          # Node.js
9.6.4             # npm
Python 3.10.12    # Python 3
pip 23.0.1        # pip
```

### Step 2: If Tools Are Missing

#### On Ubuntu/Debian:
```bash
# Update package manager
sudo apt update

# Install Node.js & npm
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs npm

# Install Python & pip
sudo apt install -y python3 python3-pip python3-venv

# (Optional) Install Docker
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
```

#### On macOS (with Homebrew):
```bash
# Install Node.js & npm
brew install node

# Install Python & pip
brew install python3

# (Optional) Install Docker
brew install docker
brew install --cask docker
```

#### On Windows (with Chocolatey):
```powershell
# Open PowerShell as Administrator

# Install Node.js & npm
choco install nodejs

# Install Python & pip
choco install python

# (Optional) Install Docker
choco install docker-desktop
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

## 🐳 Docker Setup (Start, Restart, Troubleshoot)

### Quick Docker commands (run these first)

```bash
# Build and start containers (detached)
docker-compose up -d

# View live logs for all services
docker-compose logs -f

# Stop and remove containers
docker-compose down

# Restart services
docker-compose restart

# Rebuild images (no cache) and start fresh
docker-compose build --no-cache
docker-compose up -d
```

### Docker Prerequisites

- ✅ Docker installed (`docker --version`)
- ✅ Docker Compose installed (`docker-compose --version`)
- ✅ Ports 3000 and 8001 available
- ✅ At least 2GB RAM allocated to Docker

### Quick Start with Docker

```bash
# Navigate to project root
cd /path/to/data-connector-platform

# Build and start all services
setup.bat

# View logs
```

# Wait for services to be ready (30-60 seconds)
```

Services will be available at:
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8001
- **Admin Panel:** http://localhost:8001/admin/

### Docker Commands Reference

#### Starting & Stopping

**Start services:**
```bash
# Start in detached mode (background)


# Start and view logs
---
```

**Stop services:**
```bash

```

**Stop and remove containers:**
```bash
## 📖 Manual Setup (Sequential Steps)
```

#### Restarting Services

**Restart all services:**
```bash

```

**Restart specific service:**
```bash
# Restart only backend
Follow these steps **in order** for a complete manual setup. This is best if you want control over each step or if the automated setup doesn't work.

# Restart only frontend

```

**Soft restart (stop → start):**
```bash
### Step 1: Navigate to Project Directory

```

**Hard restart (rebuild containers):**
```bash
# Stop everything
```bash

# Rebuild images
cd /path/to/data-connector-platform

# Start everything
```
```

#### Viewing Logs

**View all logs:**
```bash

```

**View specific service logs:**
```bash
# Backend logs
### Step 2: Install Node.js Frontend Dependencies

# Frontend logs

```

**View last 50 lines:**
```bash
```bash
```

#### Building Images

**Build all images:**
```bash
# Install all npm packages
```

**Rebuild without cache (fresh build):**
```bash
npm install
```

**Build specific service:**
```bash
# Build only backend


# Build only frontend
# This installs Next.js, React, TypeScript, and frontend dependencies
```

### Docker Troubleshooting

#### Issue: "Port 3000 is already allocated"

**Solution:**
```bash
# Find and stop container using port 3000
```


# Or use different port in docker-compose.yml
# Change: ports: - "3000:3000" to "3001:3000"
```

#### Issue: "Port 8001 is already allocated"

**Solution:**
```bash
# Find process using port 8001
lsof -i :8001
kill -9 <PID>

# Or modify docker-compose.yml port mapping
```

#### Issue: "Cannot connect to Docker daemon"

**Solution (Linux):**
```bash
# Start Docker service
sudo systemctl start docker

# Add current user to docker group
sudo usermod -aG docker $USER

# Apply new group membership
newgrp docker

# Verify Docker is running
**Expected:** No errors, `node_modules/` folder created
```

#### Issue: "Out of disk space" or "No space left on device"

**Solution:**
```bash
# Remove unused Docker images and containers


# More aggressive cleanup (remove all unused resources)
### Step 3: Set Up Python Virtual Environment

# Check Docker disk usage

```

#### Issue: "Container exits immediately" or "keeps restarting"

**Solution:**
```bash
# Check logs to see error
Navigate to the backend folder and create a virtual environment:


# Rebuild containers
#### Option A: Using venv (Recommended)
```bash
cd backend

# Verify logs again

```

#### Issue: "Backend container can't connect to external database"

**Solution:**
```bash
# Use host network (Linux only)
# In docker-compose.yml, add to backend service:
# network_mode: "host"

# Or update database host from "localhost" to "host.docker.internal" (Mac/Windows)
# Or use Docker network to expose databases
```

#### Issue: "Cannot run docker-compose: command not found"

**Solution:**
```bash
# Check if installed
# Create virtual environment

# If not found, install
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
python3 -m venv .venv
```

#### Full Reset (Nuclear Option)

```bash
# Stop and remove all containers and volumes


# Remove dangling images
# Activate virtual environment

# Rebuild everything from scratch
# On Linux/macOS:

# Start fresh
source .venv/bin/activate

# Watch logs

```

---

## ✅ Prerequisites Check
# On Windows:
# .venv\Scripts\activate

# Verify activation (you should see (.venv) in your prompt)
```

#### Option B: Using conda
```bash
# Create conda environment
conda create -n data-connector python=3.10

# Activate it
conda activate data-connector

# Navigate to backend
cd backend
```

**Verify:** Your terminal should show `(.venv)` or `(data-connector)` prefix

### Step 4: Install Python Dependencies

```bash
# Make sure you're in backend/ directory with virtual env activated
cd backend
source .venv/bin/activate  # or conda activate data-connector

# Install all Python packages
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected:** Django, djangorestframework, cryptography, and other packages installed

### Step 5: Set Up Test Database Connections

The platform needs to connect to external databases for testing. You can either:
- **Option A:** Use existing databases you have
- **Option B:** Create new test databases (see section below)

#### Create Test Databases (If Not Installed)

The platform uses 4 database types for connections. Create a script or manually set up:

**PostgreSQL Test Database:**
```bash
# Using PostgreSQL client
psql -U postgres

# In PostgreSQL shell:
CREATE DATABASE test_postgresql;
CREATE USER test_user WITH PASSWORD 'test_password';
GRANT ALL PRIVILEGES ON DATABASE test_postgresql TO test_user;
\q
```

**MySQL Test Database:**
```bash
# Using MySQL client
mysql -u root -p

# In MySQL shell:
CREATE DATABASE test_mysql;
CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'test_password';
GRANT ALL PRIVILEGES ON test_mysql.* TO 'test_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**MongoDB Test Database:**
```bash
# MongoDB doesn't require pre-creation
# Connection to mongodb://localhost:27017/test_mongodb works automatically
# Just verify mongod is running:
mongosh --eval "db.version()"
```

**ClickHouse Test Database:**
```bash
# Using ClickHouse client
clickhouse-client

# In ClickHouse shell:
CREATE DATABASE test_clickhouse;
EXIT;
```

#### Verify Databases Are Running

```bash
# PostgreSQL
psql -U test_user -d test_postgresql -h localhost -c "SELECT 1;"

# MySQL
mysql -u test_user -p test_password -h localhost -e "SELECT 1;"

# MongoDB
mongosh --eval "db.runCommand('ping')"

# ClickHouse
clickhouse-client --query "SELECT 1;"
```

### Start & Debug Commands for Supported Databases

This section shows both host (systemd) commands and Docker Compose container commands. Run Docker commands from the project root where `docker-compose.yml` lives. Replace `<service_name>` with the actual service name from your `docker-compose.yml` (common names: `postgres`, `mysql`, `mongo`, `clickhouse`).

A. Host (systemd) — run these on the host (requires sudo)

- PostgreSQL (systemd)

```bash
# Start
sudo systemctl start postgresql

# Check status
sudo systemctl status postgresql

# Logs
sudo journalctl -u postgresql -n 200 --no-pager

# Run Postgres CLI
psql -U postgres -h localhost
```

- MySQL / MariaDB (systemd)

```bash
# Start
sudo systemctl start mysql

# Check status
sudo systemctl status mysql

# Logs
sudo journalctl -u mysql -n 200 --no-pager

# Run MySQL CLI
mysql -u root -p
```

- MongoDB (systemd)

```bash
# Start
sudo systemctl start mongod

# Check status
sudo systemctl status mongod

# Logs
sudo journalctl -u mongod -n 200 --no-pager

# Run Mongo shell
mongosh
```

- ClickHouse (systemd)

```bash
# Start
sudo systemctl start clickhouse-server

# Check status
sudo systemctl status clickhouse-server

# Logs
sudo journalctl -u clickhouse-server -n 200 --no-pager

# Run ClickHouse client
clickhouse-client --query "SELECT 1"
```

B. Docker Compose (containers) — run these from project root

```bash
# Start a single DB service (detached)
docker-compose up -d <service_name>

# Start all services
docker-compose up -d

# Check container status
docker-compose ps | grep <service_name>

# Follow logs for a service
docker-compose logs -f <service_name>

# Exec into a running service (bash or sh)
docker-compose exec <service_name> bash || docker-compose exec <service_name> sh

# If you need the container id and want to use docker directly
docker ps --filter "name=<service_name>" --format "{{.ID}}  {{.Names}}"
docker exec -it <container_id> bash
```

Examples: run DB client inside the container

```bash
# PostgreSQL (inside container)
docker-compose exec postgres psql -U postgres -h localhost -d postgres

# MySQL (inside container)
docker-compose exec mysql mysql -u root -p

# MongoDB (inside container)
docker-compose exec mongo mongosh

# ClickHouse (inside container)
docker-compose exec clickhouse clickhouse-client --query "SELECT 1"
```

### Step 6: Initialize Application Database (SQLite)

```bash
# Make sure you're in backend/ with virtual env activated
cd backend
source .venv/bin/activate

# Run Django migrations
python manage.py migrate

# This creates db.sqlite3 with all tables
```

**Expected:** `backend/db.sqlite3` file created, no errors

### Step 7: Create Demo Users

```bash
# Still in backend/ with virtual env activated
python setup_demo_users.py

# Creates 4 demo users:
# - admin / admin123
# - john_sales / john123
# - sarah_analytics / sarah456
# - mike_reporting / mike789
```

**Expected:** 4 users created successfully

### Step 8: Populate Demo Data (Optional)

```bash
# Still in backend/ with virtual env activated
python populate_demo_data.py

# Creates sample connections and test data
```

**Expected:** Demo connections and data created (optional, can be skipped)

---

## 🗄️ Database Setup and Verification

### Prerequisites Before Starting

✅ Verify you have completed:
- [x] System requirements installed
- [x] Node.js dependencies installed (`npm install`)
- [x] Python virtual environment created and activated
- [x] Python dependencies installed (`pip install -r requirements.txt`)
- [x] Application database initialized (`python manage.py migrate`)
- [x] Demo users created (`python setup_demo_users.py`)

### Method 1: Using npm Scripts (Recommended)

Open **two terminal windows** in the project root:

**Terminal 1 - Backend:**
```bash
npm run backend
```

**Terminal 2 - Frontend:**
```bash
npm run frontend
```

Both services will start automatically.

### Method 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
source .venv/bin/activate    # or conda activate data-connector
python manage.py runserver 8001
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

### Method 3: Using start script

```bash
bash start_backend.sh    # Terminal 1
bash run_frontend.sh     # Terminal 2
```

### Application URLs

Once both are running, access:

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend** | http://localhost:3000 | Main web application |
| **API** | http://localhost:8001/api/ | REST API endpoints |
| **Admin Panel** | http://localhost:8001/admin/ | Django admin (admin/admin123) |
| **Connections API** | http://localhost:8001/api/connections/ | Browse connections |
| **Files API** | http://localhost:8001/api/files/ | Browse files |

### First Access

1. Open http://localhost:3000 in your browser
2. You should see the login page
3. Use one of the demo credentials (see below)
4. You'll be redirected to the dashboard

### Terminal Output

**Backend should show:**
```
Starting development server at http://127.0.0.1:8001/
Quit the server with CONTROL-C.
```

**Frontend should show:**
```
▲ Next.js 14.0.0
- Local:        http://localhost:3000
```

---

## 👤 Demo Credentials

Four demo users are pre-configured with different roles:

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| `admin` | `admin123` | Administrator | Full access to all features, user management |
| `john_sales` | `john123` | Sales | Create connections, extract data |
| `sarah_analytics` | `sarah456` | Analytics | View analytics, read-only access |
| `mike_reporting` | `mike789` | Reporting | Generate reports, view dashboards |

### First Time Login

1. Navigate to http://localhost:3000
2. Enter username and password from table above
3. Click **"Sign In"**
4. You'll be redirected to the dashboard

### Resetting User Passwords

**Reset admin user to default password:**
```bash
cd backend
source .venv/bin/activate
python reset_admin.py
# Resets admin password to: admin123
```

**Create a new admin user:**
```bash
cd backend
source .venv/bin/activate
python manage.py createsuperuser
# Follow the prompts
```

**Reset specific user via Django shell:**
```bash
cd backend
source .venv/bin/activate
python manage.py shell

# In the shell:
from django.contrib.auth.models import User
user = User.objects.get(username='john_sales')
user.set_password('new_password')
user.save()
exit()
```

---

## 🐳 Docker Setup (Start, Restart, Troubleshoot)

### Docker Prerequisites

- ✅ Docker installed (`docker --version`)
- ✅ Docker Compose installed (`docker-compose --version`)
- ✅ Ports 3000 and 8001 available
- ✅ At least 2GB RAM allocated to Docker

### Quick Start with Docker

```bash
# Navigate to project root
cd /path/to/data-connector-platform

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Wait for services to be ready (30-60 seconds)
```

Services will be available at:
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8001
- **Admin Panel:** http://localhost:8001/admin/

### Docker Commands Reference

#### Starting & Stopping

**Start services:**
```bash
# Start in detached mode (background)
docker-compose up -d

# Start and view logs
docker-compose up
```

**Stop services:**
```bash
docker-compose stop
```

**Stop and remove containers:**
```bash
docker-compose down
```

#### Restarting Services

**Restart all services:**
```bash
docker-compose restart
```

**Restart specific service:**
```bash
# Restart only backend
docker-compose restart backend

# Restart only frontend
docker-compose restart frontend
```

**Soft restart (stop → start):**
```bash
docker-compose stop
docker-compose start
```

**Hard restart (rebuild containers):**
```bash
# Stop everything
docker-compose down

# Rebuild images
docker-compose build

# Start everything
docker-compose up -d
```

#### Viewing Logs

**View all logs:**
```bash
docker-compose logs -f
```

**View specific service logs:**
```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend
```

**View last 50 lines:**
```bash
docker-compose logs -f --tail=50
```

#### Building Images

**Build all images:**
```bash
docker-compose build
```

**Rebuild without cache (fresh build):**
```bash
docker-compose build --no-cache
```

**Build specific service:**
```bash
# Build only backend
docker-compose build backend

# Build only frontend
docker-compose build frontend
```

### Docker Troubleshooting

#### Issue: "Port 3000 is already allocated"

**Solution:**
```bash
# Find and stop container using port 3000
docker ps
docker stop <container-id>

# Or use different port in docker-compose.yml
# Change: ports: - "3000:3000" to "3001:3000"
```

#### Issue: "Port 8001 is already allocated"

**Solution:**
```bash
# Find process using port 8001
lsof -i :8001
kill -9 <PID>

# Or modify docker-compose.yml port mapping
```

#### Issue: "Cannot connect to Docker daemon"

**Solution (Linux):**
```bash
# Start Docker service
sudo systemctl start docker

# Add current user to docker group
sudo usermod -aG docker $USER

# Apply new group membership
newgrp docker

# Verify Docker is running
docker ps
```

#### Issue: "Out of disk space" or "No space left on device"

**Solution:**
```bash
# Remove unused Docker images and containers
docker system prune

# More aggressive cleanup (remove all unused resources)
docker system prune -a

# Check Docker disk usage
docker system df
```

#### Issue: "Container exits immediately" or "keeps restarting"

**Solution:**
```bash
# Check logs to see error
docker-compose logs backend
docker-compose logs frontend

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Verify logs again
docker-compose logs -f
```

#### Issue: "Backend container can't connect to external database"

**Solution:**
```bash
# Use host network (Linux only)
# In docker-compose.yml, add to backend service:
# network_mode: "host"

# Or update database host from "localhost" to "host.docker.internal" (Mac/Windows)
# Or use Docker network to expose databases
```

#### Issue: "Cannot run docker-compose: command not found"

**Solution:**
```bash
# Check if installed
docker-compose --version

# If not found, install
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker-compose --version
```

#### Full Reset (Nuclear Option)

```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Remove dangling images
docker image prune -f

# Rebuild everything from scratch
docker-compose build --no-cache

# Start fresh
docker-compose up -d

# Watch logs
docker-compose logs -f
```

---

## 💡 Development Tips

### Project Structure Overview

```
data-connector-platform/
├── app/                       # Next.js frontend (TypeScript/React)
│   ├── api/                   # Backend API routes
│   ├── components/            # React components
│   │   ├── ConnectionForm.tsx
│   │   ├── DataGrid.tsx
│   │   ├── FileViewer.tsx
│   │   ├── Modal.tsx
│   │   └── Toast.tsx
│   ├── lib/                   # Utility functions & API client
│   └── page.tsx               # Main application page
├── backend/                   # Django backend (Python)
│   ├── connector/             # Main Django app
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API views
│   │   ├── serializers.py     # REST serializers
│   │   ├── urls.py            # URL routing
│   │   └── migrations/        # Database migrations
│   ├── backend/               # Django configuration
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # URL routing
│   │   └── wsgi.py            # Production config
│   ├── manage.py              # Django CLI
│   └── requirements.txt       # Python dependencies
├── public/                    # Static assets
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile.backend         # Backend Docker image
├── Dockerfile.frontend        # Frontend Docker image
├── package.json               # Node.js dependencies
├── tsconfig.json              # TypeScript configuration
├── next.config.ts             # Next.js configuration
├── .eslintrc.config.mjs       # ESLint configuration
└── README.md                  # Project documentation
```

### Useful npm Commands

```bash
# Install dependencies
npm install

# Start frontend development
npm run dev

# Start backend server
npm run backend

# Build frontend for production
npm run build

# Start production build
npm start

# Run linting
npm run lint

# Run linting with fix
npm run lint:fix
```

### Useful Django Commands

```bash
cd backend
source .venv/bin/activate

# Run migrations
python manage.py migrate

# Create new migrations
python manage.py makemigrations

# Start development server
python manage.py runserver 8001

# Start on different port
python manage.py runserver 8002

# Open interactive shell
python manage.py shell

# Create new admin user
python manage.py createsuperuser

# Run tests
python manage.py test

# Run specific test
python manage.py test connector.tests

# Clear database
python manage.py flush

# Export data
python manage.py dumpdata > backup.json

# Import data
python manage.py loaddata backup.json
```

### VSCode Extensions (Recommended)

```
Extensions to install for best development experience:
- ES7+ React/Redux/React-Native snippets (dsznajder.es7-react-js-snippets)
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Django (batisteo.vscode-django)
- Tailwind CSS IntelliSense (bradlc.vscode-tailwindcss)
- TypeScript Vue Plugin (Vue.volar)
- REST Client (humao.rest-client)
- Thunder Client (rangav.vscode-thunder-client)
- SQLite (alexcvzz.vscode-sqlite)
```

### Running Integration Tests

```bash
# Test that ports are available
bash integration-test-ports.sh

# Test API endpoints manually
open test-files-api.html  # or use your browser

# Run Django tests
cd backend
python manage.py test

# Run specific test module
python manage.py test connector.test_views
```

### Environment Variables

Create `.env` file in project root if needed:

```bash
# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8001
DEBUG=false

# Backend (in backend/.env)
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

---

## 🔧 Troubleshooting

### General Issues

#### Issue: "npm: command not found"

**Solution:**
```bash
# Verify Node.js is installed
node --version

# If not installed, install from https://nodejs.org/
# Or using package manager (see Prerequisites Check section)
```

#### Issue: "python3: command not found"

**Solution:**
```bash
# Verify Python is installed
python3 --version

# If not installed, install from https://www.python.org/
# Or using package manager (see Prerequisites Check section)

# Note: On some systems, use 'python' instead of 'python3'
python --version
```

### Frontend Issues (Port 3000)

#### Issue: "Port 3000 is already in use"

**Find and kill process:**
```bash
# On Linux/macOS
lsof -i :3000
kill -9 <PID>

# On Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port
npm run dev -- --port 3001
```

#### Issue: "npm ERR! Cannot find module 'next'"

**Solution:**
```bash
# Clear and reinstall dependencies
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Try again
npm run dev
```

#### Issue: "Failed to compile" or TypeScript errors

**Solution:**
```bash
# Check TypeScript configuration
cat tsconfig.json

# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
npm install

# Try again
npm run dev

# Check specific file errors
npm run lint
```

### Backend Issues (Port 8001)

#### Issue: "Port 8001 is already in use"

**Find and kill process:**
```bash
# On Linux/macOS
lsof -i :8001
kill -9 <PID>

# On Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Or use different port
cd backend && python manage.py runserver 8002
```

#### Issue: "ModuleNotFoundError: No module named 'django'"

**Solution:**
```bash
# Ensure you're in backend directory
cd backend

# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate      # Windows

# Reinstall requirements
pip install -r requirements.txt

# Verify Django is installed
python -m django --version
```

#### Issue: "django.db.utils.OperationalError: no such table"

**Solution:**
```bash
cd backend
source .venv/bin/activate

# Run migrations
python manage.py migrate

# Create demo data
python setup_demo_users.py
```

#### Issue: "CSRF token missing or incorrect"

**Solution:**
```bash
# This is expected for API POST requests
# Include header in requests:
-H "X-CSRFToken: <token>"

# Or use:
-H "X-Requested-With: XMLHttpRequest"
```

### Database Connection Issues

#### Issue: "Connection test fails" or "Cannot connect to database"

**Check connectivity first:**
```bash
# PostgreSQL
psql -h localhost -U username -d database

# MySQL
mysql -h localhost -u username -p database

# MongoDB
mongosh "mongodb://host:port/database"

# ClickHouse
clickhouse-client -h localhost --port 9000 -d database
```

**If connection test fails in app:**
1. ✅ Verify host and port are correct
2. ✅ Verify database credentials are accurate
3. ✅ Verify database server is running
4. ✅ Verify firewall isn't blocking connection
5. ✅ Check network connectivity to database server
6. ✅ Verify database and user exist

**Test from backend:**
```bash
cd backend
source .venv/bin/activate
python manage.py shell

# In Python shell
from connector.models import Connection
c = Connection(
    name='Test',
    db_type='postgresql',
    host='localhost',
    port=5432,
    username='user',
    password='pass',
    database_name='db'
)
c.test_connection()  # Returns True/False
```

#### Issue: "database is locked" (SQLite)

**Solution:**
```bash
# Multiple processes accessing database
# Kill all Django processes
pkill -f "manage.py"

# Remove lock files
rm backend/db.sqlite3-journal

# Try again
python manage.py runserver
```

#### Issue: "Access denied for user" (MySQL)

**Solution:**
```bash
# Check MySQL user permissions
mysql -u root -p
SHOW GRANTS FOR 'username'@'localhost';

# Fix permissions
GRANT ALL PRIVILEGES ON database.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
```

### API & Integration Issues

#### Issue: "CORS error" in browser console

**Solution:**
```bash
# Backend is configured to allow frontend
# Make sure backend is running on port 8001
# Frontend on port 3000

# If using different ports, update:
# backend/backend/settings.py - CORS_ALLOWED_ORIGINS

cd backend
# Edit settings.py and add your frontend URL:
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://yourdomain.com'
]
```

#### Issue: "API returns 500 Internal Server Error"

**Check backend logs:**
```bash
# Backend terminal should show error
# Also check:
cd backend
python manage.py shell
# Test the function causing error
```

#### Issue: "File download fails"

**Solution:**
```bash
# Check file exists at path
ls backend/media/

# Ensure permissions are correct
chmod 644 backend/media/*

# Check disk space
df -h

# Restart backend
python manage.py runserver 8001
```

### Performance Issues

#### Issue: "Application is slow" or "high memory usage"

**Solution:**
```bash
# Check running processes
ps aux | grep python
ps aux | grep node

# Monitor resource usage
top              # Linux/macOS
taskmgr          # Windows

# Restart services (fresh start)
docker-compose restart

# Or manually:
# Kill frontend: Ctrl+C in npm terminal
# Kill backend: Ctrl+C in backend terminal
# Restart both
```

#### Issue: "Frontend takes long time to load"

**Solution:**
```bash
# Clear Next.js cache
rm -rf .next

# Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)

# Rebuild frontend
npm run build

# Check network tab in DevTools (F12)
```

### Container Issues (Docker)

See **Docker Troubleshooting** section in [Docker Setup](#docker-setup-start-restart-troubleshoot) above for complete Docker troubleshooting guidance.

---

## 🗄️ Database Configuration

### Supported External Databases

The platform supports connections to:
- ✅ **PostgreSQL** (v10+)
- ✅ **MySQL** (v5.7+)
- ✅ **MongoDB** (v3.6+)
- ✅ **ClickHouse** (v20+)

### Application Database (SQLite)

The Django backend uses SQLite by default for storing:
- User accounts
- Saved connections  
- Extracted file metadata
- Access logs

**Database file location:** `backend/db.sqlite3`

### Adding External Database Connections

1. Log in to http://localhost:3000
2. Click **"Add Connection"** button in left panel
3. Fill in connection details:

**PostgreSQL Example:**
```
Name: My PostgreSQL
Database Type: PostgreSQL
Host: localhost (or IP)
Port: 5432
Username: postgres
Password: your_password
Database: test_postgresql
```

4. Click **"Test Connection"** to verify connectivity
5. Click **"Save Connection"** if test succeeds

### Resetting Application Database

```bash
cd backend
source .venv/bin/activate

# Remove existing database
rm db.sqlite3

# Recreate database schema
python manage.py migrate

# Recreate demo users
python setup_demo_users.py

# Populate demo data (optional)
python populate_demo_data.py
```

---

## ✅ Verification Checklist

After setup is complete, verify everything works by checking:

### Prerequisites
- [ ] Node.js v16+ installed (`node --version`)
- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] npm v7+ installed (`npm --version`)
- [ ] pip 21+ installed (`pip --version`)

### Installation
- [ ] Project cloned/downloaded
- [ ] `npm install` completed successfully
- [ ] Python virtual environment created (.venv or conda)
- [ ] `pip install -r requirements.txt` completed successfully

### Database Setup
- [ ] Django migrations ran (`python manage.py migrate`)
- [ ] Demo users created (`python setup_demo_users.py`)
- [ ] Test databases accessible (PostgreSQL, MySQL, MongoDB, ClickHouse)

### Application Running
- [ ] Backend starts without errors (`npm run backend` or `python manage.py runserver 8001`)
- [ ] Frontend starts without errors (`npm run frontend` or `npm run dev`)
- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend accessible at http://localhost:8001
- [ ] Admin panel accessible at http://localhost:8001/admin/

### Authentication & Access
- [ ] Can log in with admin credentials (admin / admin123)
- [ ] Can log in with john_sales credentials (john_sales / john123)
- [ ] Can log in with other demo users
- [ ] Dashboard loads after login
- [ ] No authentication errors in console

### Core Functionality
- [ ] Can view demo connections in left panel
- [ ] Can click "Add Connection" button
- [ ] Connection form displays with all fields
- [ ] Can test connection to database
- [ ] Can create new connection
- [ ] Can view files in storage
- [ ] Can download files
- [ ] Can share files with other users

### API & Integration
- [ ] API accessible at http://localhost:8001/api/
- [ ] Connections API at http://localhost:8001/api/connections/ (HTTP 200)
- [ ] Files API at http://localhost:8001/api/files/ (HTTP 200)
- [ ] Can make API GET requests using curl or Postman
- [ ] JSON responses properly formatted

### Error Checking
- [ ] No errors in browser console (F12)
- [ ] No errors in backend terminal
- [ ] No errors in frontend terminal
- [ ] No database errors in logs
- [ ] No network errors (check Network tab in DevTools)

### Docker (If Using)
- [ ] Docker services start (`docker-compose up -d`)
- [ ] Both containers running (`docker-compose ps`)
- [ ] No errors in Docker logs (`docker-compose logs`)
- [ ] Frontend accessible via Docker at http://localhost:3000
- [ ] Backend accessible via Docker at http://localhost:8001

### Performance & Resources
- [ ] Application loads in reasonable time (<3 seconds)
- [ ] Frontend responsive to user input
- [ ] Backend API responds quickly (<1 second)
- [ ] No excessive CPU/memory usage
- [ ] File downloads complete successfully

**If all items pass ✅ then your setup is complete and ready for use!** 🎉

---

## 📞 Support & Quick Reference

### Common Commands Quick Reference

```bash
# Setup & Installation
npm install                          # Install frontend dependencies
cd backend && pip install -r requirements.txt  # Install backend dependencies
python manage.py migrate             # Initialize database
python setup_demo_users.py           # Create demo users

# Running Application
npm run dev                          # Start frontend
npm run backend                      # Start backend
npm run build                        # Build for production

# Docker
docker-compose up -d                 # Start all services
docker-compose down                  # Stop all services
docker-compose logs -f               # View logs
docker-compose restart               # Restart services

# Database
python manage.py shell               # Interactive shell
python manage.py createsuperuser     # Create admin user
python manage.py migrate             # Run migrations
rm db.sqlite3 && python manage.py migrate  # Reset database

# Troubleshooting
lsof -i :3000                        # Check port 3000
lsof -i :8001                        # Check port 8001
pkill -f "manage.py"                 # Kill Django processes
```

### Important Files & Directories

| Path | Purpose |
|------|---------|
| `backend/db.sqlite3` | Application database (create/reset if missing) |
| `backend/.venv/` | Python virtual environment |
| `.env` | Environment variables (if needed) |
| `docker-compose.yml` | Docker configuration |
| `package.json` | Node.js dependencies |
| `requirements.txt` | Python dependencies |

### Default Ports

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8001 | http://localhost:8001 |
| Django Admin | 8001 | http://localhost:8001/admin/ |

### Documentation Files

- **README.md** - Project overview and features
- **CORE_FEATURES.md** - Feature documentation
- **TECHNICAL_SPECIFICATIONS.md** - API documentation
- **DESIGN_DECISIONS.md** - Architecture decisions
- **NAVIGATION_AND_USER_GUIDE.md** - User guide with screenshots
- **SETUP.md** - This file (setup instructions)

### Getting Help

1. **Check this Troubleshooting section first** - Most issues are covered
2. **Verify prerequisites** - Run version checks from Prerequisites Check section
3. **Check terminal output** - Read error messages carefully
4. **Review relevant documentation** - See Documentation Files above
5. **Try automated setup** - Run `bash setup.sh` (Linux/macOS) or `setup.bat` (Windows)

### First Time Setup Checklist (Quick Version)

```bash
# 1. Prerequisites (verify versions)
node --version && npm --version && python3 --version

# 2. Install dependencies
npm install
cd backend && pip install -r requirements.txt

# 3. Setup database
cd backend && python manage.py migrate && python setup_demo_users.py

# 4. Start services (open 2 terminals)
# Terminal 1:
npm run backend

# Terminal 2 (new terminal window):
npm run frontend

# 5. Access application
# Open http://localhost:3000 in browser
# Login with: admin / admin123
```

---

**Last Updated:** 14 April, 2026 | **Version:** 3.0 | **Status:** ✅ Production Ready

Ready to get started? Open http://localhost:3000 after completing setup! 🚀
