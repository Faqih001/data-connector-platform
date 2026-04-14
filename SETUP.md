# 📖 Complete Setup & Development Guide

**Comprehensive guide to setting up and running the Data Connector Platform**

> **For Everyone**: Whether you're a beginner or experienced developer, start with the **Quick Setup** section below.

---

## ⚡ QUICK SETUP (Recommended for Everyone)

### Linux/macOS Users:

First, make the setup script executable:
```bash
cd /home/amir/Desktop/projects/data-connector-platform
chmod +x setup.sh
```

Then run it:
```bash
bash setup.sh
```

### Windows Users:
1. Open **Command Prompt** or **PowerShell** as Administrator
2. Navigate to the project folder
3. Run: `setup.bat`

**That's it!** The script will automatically:
- Install all dependencies
- Set up the database
- Create admin and demo users
- Populate sample data

---

## 🚀 Manual Quick Start (3 Minutes)

### Prerequisites
- **Node.js 18+** (JavaScript runtime)
- **Python 3.8+** (Backend runtime)
- **Git** (Version control)
- **Command Prompt/Terminal** (For running commands)

### Install & Run
```bash
# 1. Clone/navigate to project
cd /path/to/data-connector-platform

# 2. Install dependencies
npm install
cd backend && pip install -r requirements.txt && cd ..

# 3. Setup database (one-time)
cd backend && python manage.py migrate && cd ..

# 4. Terminal 1: Start Backend
npm run backend

# 5. Terminal 2: Start Frontend
npm run frontend

# 6. Open browser
# http://localhost:3000
```

✅ **Done!** Application is running with automatic port detection.

---

## � BEGINNER'S GUIDE (Step-by-Step for Non-Technical Users)

### What You Need to Install First

Before running the setup script, you need to install three tools:

#### 1️⃣ **Node.js** (JavaScript & npm)
- **What it is**: Runtime for the frontend application
- **Download**: https://nodejs.org/ (Choose **LTS version**)
- **Installation**:
  - **Windows**: Click the installer and follow prompts. Keep all defaults.
  - **Linux/macOS**: Follow the instructions on the website or use:
    ```bash
    # macOS with Homebrew
    brew install node
    
    # Linux (Ubuntu/Debian)
    sudo apt update && sudo apt install nodejs npm
    ```
- **Verify**: Open Terminal/Command Prompt and run:
  ```
  node --version
  npm --version
  ```
  You should see version numbers (e.g., v18.17.0)

#### 2️⃣ **Python** (Backend runtime)
- **What it is**: Runtime for the backend application
- **Download**: https://www.python.org/ (Choose version 3.8 or higher)
- **Installation**:
  - **Windows**: Click installer, **IMPORTANT: Check "Add Python to PATH"**, then click Install
  - **Linux/macOS**: Usually pre-installed. Run:
    ```bash
    python3 --version
    ```
- **Verify**: Open Terminal/Command Prompt and run:
  ```
  python --version
  ```
  You should see version 3.8+

#### 3️⃣ **Git** (Optional but recommended)
- **Download**: https://git-scm.com/
- **Used for**: Version control and pulling code updates

### Running the Automated Setup ✨

Once you have Node.js and Python installed:

**Windows Users:**
1. Press `Win + R`, type `cmd`, press Enter
2. Copy and paste this command:
   ```
   cd C:\Users\YourUsername\Desktop\data-connector-platform
   setup.bat
   ```
3. Wait for it to finish (5-10 minutes depending on internet speed)

**Linux/macOS Users:**
1. Open Terminal
2. Copy and paste this command:
   ```bash
   cd ~/Desktop/data-connector-platform
   bash setup.sh
   ```
3. Wait for it to finish

### After Setup Completes ✅

The script will show you login credentials. **Write them down!**

Example:
```
Demo Credentials:
  User: admin / Password: admin123
  User: john_sales / Password: john123
```

---

## �📋 Detailed Setup

### Verify Prerequisites

```bash
node --version    # Should be 18.0.0+
npm --version     # Should be 9.0.0+
python --version  # Should be 3.8+
pip --version
```

### First-Time Setup

```bash
# Navigate to project
cd /path/to/data-connector-platform

# Install Node dependencies
npm install

# Setup Python environment
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Create/update database
python manage.py migrate
python manage.py makemigrations connector  # If needed

# Return to root
cd ..
```

### Start Services (2 Terminals Required)

**Terminal 1: Backend Server**
```bash
npm run backend
# Output: ✓ Starting Django backend on port 8000...
```

**Terminal 2: Frontend Server**
```bash
npm run frontend  
# Output: ✓ Starting Next.js frontend on port 3000...
```

### Access Application
Open browser to: **http://localhost:3000**

---

## 🔧 Port Management

### How Port Detection Works
The `port-detector.js` utility automatically finds available ports:
- **Backend**: Scans ports 8000-8009 (Django)
- **Frontend**: Scans ports 3000-3009 (Next.js)
- **Multiple Instances**: Supports running multiple copies by selecting different ports in range

### Check Current Port Usage

**Linux/macOS:**
```bash
lsof -i :8001   # Check backend port
lsof -i :3000   # Check frontend port
```

**Windows (PowerShell):**
```powershell
Get-NetTCPConnection -LocalPort 8001
Get-NetTCPConnection -LocalPort 3000
```

### Kill Process on Port

**Linux/macOS:**
```bash
kill -9 $(lsof -t -i :8001)
kill -9 $(lsof -t -i :3000)
```

**Windows (PowerShell as Admin):**
```powershell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8001).OwningProcess -Force
Stop-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess -Force
```

### Manual Port Selection

**Backend on specific port:**
```bash
cd backend
python manage.py runserver 0.0.0.0:8002
```

**Frontend on custom port:**
```bash
npm run dev -- -p 3001
```

---

## 🐳 Docker Setup (Alternative)

If you prefer containerization:

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Services available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8001

---

## 🔍 Verification

### Backend Health Check
```bash
curl http://localhost:8001/api/connections/
# Should return: 200 OK (possibly with empty list)
```

### Frontend Health Check
```bash
curl http://localhost:3000
# Should return: HTML content
```

### Database Check
```bash
cd backend
python manage.py shell
```

```python
from connector.models import Connection
Connection.objects.count()  # Should return a number
```

---

## ⚠️ Troubleshooting Guide

### ✅ First Check: Is Everything Running?

Run these commands in separate terminals to verify:

**Terminal 1 - Backend Health:**
```bash
curl http://localhost:8001/api/connections/
```
Expected: Should see JSON data in response (not an error)

**Terminal 2 - Frontend Health:**
```bash
curl http://localhost:3000
```
Expected: Should see HTML content

**Browser:**
- Open http://localhost:3000
- You should see the login screen

---

### ❌ Issue 1: Cannot complete setup
**Error**: `Command not found` or `No such file`

**Solution - Windows:**
- Make sure Node.js and Python are installed
- Restart Command Prompt after installing
- Run `node --version` to verify Node.js is installed
- Run `python --version` to verify Python is installed

**Solution - Linux/macOS:**
```bash
# Check if Node.js is installed
which node
# Check if Python is installed
which python3
```

If not found, install using package manager:
```bash
# macOS
brew install node python3

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install nodejs npm python3 python3-pip
```

---

### ❌ Issue 2: "Address already in use" or "Port 8001 already in use"

**Explanation**: Another application is using the same port.

**Solution - Windows (PowerShell):**
```powershell
# Find process using port 8001
Get-NetTCPConnection -LocalPort 8001 | Select OwningProcess

# Kill the process (replace 1234 with the PID from above)
Stop-Process -Id 1234 -Force
```

**Solution - Linux/macOS:**
```bash
# Find process using port 8001
lsof -i :8001

# Kill the process (replace 1234 with PID from above)
kill -9 1234

# Or use this shortcut:
kill -9 $(lsof -t -i :8001)
```

**Alternative Solution - Use a different port:**
```bash
cd backend
python manage.py runserver 0.0.0.0:8002
```
Then update `app/lib/api.ts` to use port 8002.

---

### ❌ Issue 3: "ModuleNotFoundError" or "pip install fails"

**Error Example:**
```
ModuleNotFoundError: No module named 'django'
```

**Solution:**
```bash
# Navigate to backend
cd backend

# Activate virtual environment
# Linux/macOS:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

---

### ❌ Issue 4: "django.db.utils.OperationalError"

**Explanation**: Database migrations were not run.

**Solution:**
```bash
cd backend

# Activate virtual environment first
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate.bat  # Windows

# Run migrations
python manage.py migrate

# Create superuser if needed
python manage.py createsuperuser
```

---

### ❌ Issue 5: Frontend shows "Failed to fetch" or CORS errors

**Error in Browser Console:**
```
Failed to fetch from http://localhost:8001/api/...
```

**Checklist:**
1. ✅ Is backend running on port 8001? (Check Terminal 1)
2. ✅ Is the API URL correct in `app/lib/api.ts`?
3. ✅ Are CORS settings configured?

**Solution:**
```bash
# Verify backend is running
curl http://localhost:8001/api/connections/

# Check that it returns JSON, not an error

# If using different port, update app/lib/api.ts:
# Change: const API_URL = 'http://localhost:8001/api';
# To:     const API_URL = 'http://localhost:YOUR_PORT/api';
```

**Check CORS in `backend/backend/settings.py`:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]
```

---

### ❌ Issue 6: Login not working

**Error**: 
- "Invalid username or password" (even with correct credentials)
- Login button does nothing

**Solution - Check Demo Users:**
```bash
cd backend
source .venv/bin/activate  # Linux/macOS

# Recreate demo users
python setup_demo_users.py

# Or create manually
python manage.py shell
# Then in Python shell:
# >>> from django.contrib.auth.models import User
# >>> User.objects.create_user('admin', email='admin@example.com', password='admin123')
# >>> exit()
```

**Credentials to use:**
```
Username: admin
Password: admin123
```

---

### ❌ Issue 7: npm install fails

**Error**: 
```
ERESOLVE could not resolve dependency peer
npm ERR! peer dep missing
```

**Solution:**
```bash
npm install --legacy-peer-deps
```

---

### ❌ Issue 8: Backend won't start

**Error Examples:**
```
No such file or directory: 'manage.py'
ModuleNotFoundError: No module named 'django'
```

**Checklist:**
```bash
# Verify you're in the correct directory
pwd
# Should show: .../data-connector-platform/backend

# NOT: .../data-connector-platform/backend/backend

cd backend  # If not in backend directory

# Verify virtual environment is activated
# Linux/macOS: Should see (.venv) at start of terminal line
# Windows: Same, or run:

source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate.bat  # Windows

# Then try again
python manage.py runserver 0.0.0.0:8001
```

---

### ❌ Issue 9: TypeScript errors or build fails

**Error:**
```
Type errors even though code looks correct
```

**Solution:**
```bash
# Navigate to project root
cd /path/to/data-connector-platform

# Clear cache and reinstall
rm -rf .next node_modules package-lock.json
npm install
npm run build
```

---

### ❌ Issue 10: Virtual environment not working

**Symptoms:**
```
ModuleNotFoundError when importing packages
python/python3 version is wrong
```

**Solution - Linux/macOS:**
```bash
cd backend

# Remove old venv
rm -rf .venv

# Create fresh virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install packages
pip install -r requirements.txt

# Verify
which python  # Should show .venv path
python --version
```

**Solution - Windows:**
```bash
cd backend

# Remove old venv
rmdir /s .venv

# Create fresh virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate.bat

# Install packages
pip install -r requirements.txt

# Verify
python --version
```

---

### ❌ Issue 11: Can't find database file

**Error:**
```
django.db.utils.DatabaseError: database disk image is malformed
```

**Solution:**
```bash
cd backend

# Backup current database (optional)
mv db.sqlite3 db.sqlite3.backup

# Create new database
python manage.py migrate

# Recreate users
python reset_admin.py
python setup_demo_users.py
```

---

### ✅ Getting Full Help

If your issue isn't listed:

1. **Check Browser Console** (Press F12)
   - Look for red error messages
   - Copy the exact error text

2. **Check Terminal Output**
   - Look for red or ERROR messages
   - Copy the exact error text

3. **Run Diagnostics:**
   ```bash
   # Check Node version
   node --version
   
   # Check Python version
   python --version
   
   # Check port usage
   lsof -i :8001    # Linux/macOS
   netstat -ano     # Windows
   
   # Check file permissions
   ls -la backend/db.sqlite3  # Linux/macOS
   ```



---

## 🎯 Running the Application

### After Setup is Complete

You have two options:

#### Option 1: Automated (Recommended)
```bash
npm run backend    # Terminal 1
npm run frontend   # Terminal 2
```

The scripts will automatically find available ports.

#### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend

# Activate virtual environment
source .venv/bin/activate        # Linux/macOS
# OR
.venv\Scripts\activate.bat       # Windows

# Start server
python manage.py runserver 0.0.0.0:8001
```

**Terminal 2 - Frontend:**
```bash
npm run dev
# Frontend starts at http://localhost:3000
```

### 🔐 Demo Login Credentials

Use these to test the application:

| Username | Password | Account Type |
|----------|----------|--------------|
| `admin` | `admin123` | Admin (Full Access) |
| `john_sales` | `john123` | Sales User |
| `sarah_analytics` | `sarah456` | Analytics User |
| `mike_reporting` | `mike789` | Reporting User |

### ✅ Verify Everything Works

1. **Backend is running:**
   ```bash
   curl http://localhost:8001/api/connections/
   ```
   Should see: `[]` or list of connections (not an error)

2. **Frontend is running:**
   - Open http://localhost:3000
   - You should see the login page

3. **Login works:**
   - Enter username: `admin`
   - Enter password: `admin123`
   - Click Login
   - You should see the Data Connector Platform

---

## � Understanding the Setup Process

### What the Setup Scripts Do

**setup.sh (Linux/macOS) and setup.bat (Windows) both:**

1. **Check Prerequisites** ✅
   - Verifies Node.js is installed
   - Verifies Python is installed

2. **Install Frontend Dependencies** 📦
   - Runs `npm install`
   - Installs all JavaScript libraries listed in package.json

3. **Setup Python Environment** 🐍
   - Creates `.venv` directory (isolated Python environment)
   - Prevents conflicts between different Python projects on your computer

4. **Install Backend Dependencies** 📦
   - Runs `pip install -r requirements.txt`
   - Installs Django, DRF, and other Python libraries

5. **Create/Update Database** 💾
   - Runs `python manage.py migrate`
   - Creates SQLite database (db.sqlite3)
   - Sets up all required tables

6. **Create Admin User** 👨‍💼
   - Runs `reset_admin.py`
   - Creates user: `admin` / password: `admin123`

7. **Create Demo Users** 👥
   - Runs `setup_demo_users.py`
   - Creates test accounts for trying features

8. **Populate Sample Data** 📊
   - Runs `populate_demo_data.py`
   - Adds sample database connections and test data

### Key Files and Scripts

| File | Purpose |
|------|---------|
| `setup.sh` | Automated setup for Linux/macOS |
| `setup.bat` | Automated setup for Windows |
| `reset_admin.py` | Creates admin user |
| `setup_demo_users.py` | Creates demo users for testing |
| `populate_demo_data.py` | Adds sample data to test |
| `package.json` | Lists all JavaScript dependencies |
| `requirements.txt` | Lists all Python dependencies |
| `db.sqlite3` | Database file (created during setup) |
| `.venv/` | Virtual environment directory (created during setup) |

---

## �🛠️ Development Tips

### Frontend Development

**Hot Reloading:** Changes automatically reload in browser
```bash
npm run dev
# Changes to files trigger instant reload
```

**Browser DevTools:**
- Press `F12` to open Developer Tools
- **Console**: Logs and JavaScript errors
- **Network**: See API calls to backend
- **Application**: Check cookies and storage

**Debug Frontend:**
```typescript
// Add logs in components
console.log('Debug:', variable);
console.table(array); // For arrays
```

### Backend Development

**Hot Reloading:** Restart backend to see changes
```bash
# Ctrl+C to stop, then restart
cd backend
python manage.py runserver 0.0.0.0:8000
```

**Python Debugging:**
```python
# In views or models
import pdb; pdb.set_trace()

# Then interact in terminal
(pdb) print(variable)
(pdb) continue
```

**Database Shell:**
```bash
cd backend
python manage.py shell
```

```python
from connector.models import Connection
conn = Connection.objects.first()
print(conn)
```

### API Testing

**Using curl:**
```bash
# Get connections
curl http://localhost:8000/api/connections/

# Submit data
curl -X POST http://localhost:8000/api/submit/ \
  -H "Content-Type: application/json" \
  -d '{"connection_id": 1}'
```

**Using Postman:**
- Import API endpoints from backend
- Test each endpoint

---

## 💾 Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (backend/.env)
```
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=localhost:3000,localhost:3001
```

---

## 🧪 Testing

### Frontend Tests
```bash
npm test
npm test -- --watch
```

### Backend Tests
```bash
cd backend
python manage.py test
python manage.py test connector.tests -v 2
```

### API Tests
```bash
# Test endpoints
curl http://localhost:8000/api/connections/
curl -X POST http://localhost:8000/api/submit/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## 📊 Project Structure

```
data-connector-platform/
├── app/                      # Frontend (Next.js)
│   ├── api/                 # API routes
│   ├── components/          # React components
│   ├── page.tsx             # Main page
│   └── types.ts             # TypeScript types
├── backend/                 # Backend (Django)
│   ├── connector/           # Main Django app
│   │   ├── models.py        # Database models
│   │   ├── views.py         # API views
│   │   ├── serializers.py   # Data serialization
│   │   └── migrations/      # Database migrations
│   ├── manage.py            # Django CLI
│   └── requirements.txt     # Python dependencies
├── port-detector.js         # Automatic port detection
├── package.json             # Node.js configuration
└── docker-compose.yml       # Docker configuration
```

---

## 🔐 Security Checklist

- [ ] Database migrated without errors
- [ ] Secret key different between environments
- [ ] DEBUG=False before production
- [ ] CORS configured for production domain
- [ ] Database credentials secured
- [ ] Environment variables not committed to git

---

## 📚 Additional Resources

- **Next.js:** https://nextjs.org/docs
- **Django:** https://docs.djangoproject.com/
- **React:** https://react.dev
- **Python:** https://www.python.org/doc/
- **Node.js:** https://nodejs.org/docs/

---

## ✅ Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `npm install && cd backend && pip install -r requirements.txt && cd ..` |
| Migrate database | `cd backend && python manage.py migrate && cd ..` |
| Run backend | `npm run backend` |
| Run frontend | `npm run frontend` |
| Build frontend | `npm run build` |
| Test API | `curl http://localhost:8000/api/connections/` |
| Access app | `http://localhost:3000` |
| Stop services | `Ctrl+C` |
| Check port usage | `lsof -i :8001` (Linux/macOS) |
| Kill process | `kill -9 <PID>` (Linux/macOS) |

---

## 🆘 Getting Help

1. **Check logs** - Terminal output shows most errors
2. **Browser console** - Press F12 to see frontend errors
3. **Search documentation** - Most issues covered in Common Issues section
4. **Database shell** - Test database queries directly
5. **API testing** - Use curl to test endpoints

---

## 🧪 Testing the API

### Using Browser Developer Tools

1. Press `F12` to open Developer Tools
2. Go to **Network** tab
3. Make requests in the app and see them
4. Check responses to verify API works

### Testing Endpoints with curl

```bash
# Get all connections
curl http://localhost:8001/api/connections/

# Get all files
curl http://localhost:8001/api/files/

# Test login (replace credentials)
curl -X POST http://localhost:8001/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Get current user
curl http://localhost:8001/api/user/
```

### Using the HTML Tester

Open your browser and navigate to:
```
file:///home/amir/Desktop/projects/data-connector-platform/test-files-api.html
```

This provides a visual interface to test all API endpoints!

---

## ❓ FAQ

### Q: How do I change my login password?
**A:** 
```bash
cd backend
source .venv/bin/activate  # Linux/macOS
python manage.py changepassword admin
```

### Q: How do I reset the database to a clean state?
**A:**
```bash
cd backend
rm db.sqlite3
python manage.py migrate
python reset_admin.py
python setup_demo_users.py
```

### Q: Can I use a different database instead of SQLite?
**A:** Yes! Update `backend/backend/settings.py` and install the appropriate driver. But SQLite is recommended for development.

### Q: How do I add a new user manually?
**A:**
```bash
cd backend
source .venv/bin/activate  # Linux/macOS
python manage.py shell
# Then in Python shell:
# >>> from django.contrib.auth.models import User
# >>> User.objects.create_user('username', email='user@example.com', password='password123')
# >>> exit()
```

### Q: Where are uploaded files stored?
**A:** In `backend/media/` directory

### Q: How do I backup my database?
**A:**
```bash
cd backend
cp db.sqlite3 db.sqlite3.backup
```

### Q: Can I run the frontend and backend on different machines?
**A:** Yes! Update `app/lib/api.ts` to point to the backend's IP address instead of localhost.

---

## 📊 Project Architecture

```
├── Frontend (Next.js + React)
│   ├── app/
│   │   ├── page.tsx                    # Main page with login and UI
│   │   ├── components/                 # React components
│   │   ├── api/                        # API route handlers
│   │   └── lib/api.ts                  # API client functions
│   ├── package.json                    # JavaScript dependencies
│   └── next.config.ts
│
├── Backend (Django + DRF)
│   ├── connector/
│   │   ├── models.py                   # Database models
│   │   ├── views.py                    # API endpoints
│   │   ├── serializers.py              # Data serialization
│   │   ├── auth.py                     # Authentication helpers
│   │   └── migrations/                 # Database schema changes
│   ├── backend/
│   │   ├── settings.py                 # Django configuration
│   │   ├── urls.py                     # URL routing
│   │   └── wsgi.py                     # WSGI server config
│   ├── manage.py                       # Django CLI
│   ├── requirements.txt                # Python dependencies
│   ├── db.sqlite3                      # Database (created during setup)
│   └── .venv/                          # Virtual environment (created during setup)
│
├── Configuration
│   ├── docker-compose.yml              # Docker services
│   ├── Dockerfile.backend              # Backend container
│   ├── Dockerfile.frontend             # Frontend container
│   └── .gitignore
│
└── Documentation
    ├── SETUP.md (this file)
    ├── README.md
    └── REQUIREMENTS_ACHIEVEMENT_REPORT.md
```

---

## 🚀 Next Steps After Setup

1. **Explore the UI**
   - Try creating a database connection
   - Test extracting data from a table
   - View files and manage data

2. **Run Tests** (Optional)
   ```bash
   cd backend
   python manage.py test connector
   ```

3. **Check API Documentation**
   - Visit http://localhost:8001/api/
   - See the browsable API interface
   - Try different endpoints

4. **Deploy** (Optional)
   - See DOCUMENTATION_INDEX.md for deployment guides
   - Can deploy to Heroku, AWS, Azure, etc.

---

## ✨ Success Checklist

After setup, verify:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Browser displays application
- [ ] No errors in browser console (F12)
- [ ] No errors in terminal
- [ ] Create connection form working
- [ ] Can view stored connections

**If all ✅, you're ready to use the application!**

---

**Version:** 1.0  
**Last Updated:** April 13, 2026  
**Status:** Current & Maintained
