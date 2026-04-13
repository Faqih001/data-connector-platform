# 📖 Setup & Development Guide

**Complete guide to setting up and running the Data Connector Platform**

---

## 🚀 Quick Start (3 Minutes)

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Git

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

## 📋 Detailed Setup

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

## ⚠️ Common Issues & Solutions

### Issue 1: Port Already in Use
**Error:** `Address already in use` or `EADDRINUSE`

**Solution:**
```bash
# Kill process on port
lsof -i :8000 | awk 'NR!=1 {print $2}' | xargs kill -9

# Or use different port
npm run dev -- -p 3001
```

### Issue 2: Module Not Found
**Error:** `ModuleNotFoundError: No module named 'xxx'`

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue 3: Database Error
**Error:** `django.db.utils.OperationalError`

**Solution:**
```bash
cd backend
python manage.py migrate
```

### Issue 4: CORS/Connection Errors
**Error in Frontend:** `Failed to fetch from http://localhost:8000`

**Solutions:**

1. **Check backend is running** - Look at Terminal 1 output (default: port 8001)
2. **Update API URL** in `app/lib/api.ts` if on different port:
   ```typescript
   const API_BASE_URL = 'http://localhost:8002'; // If on different port
   ```
3. **Check CORS settings** in `backend/backend/settings.py`:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://localhost:3001",
       "http://127.0.0.1:3000",
   ]
   ```

### Issue 5: npm install Fails
**Error:** `ERESOLVE could not resolve dependency peer`

**Solution:**
```bash
npm install --legacy-peer-deps
```

### Issue 6: Python Virtual Environment Not Activated
**Symptoms:** Module import errors, wrong Python version

**Solution:**
```bash
cd backend
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows
```

### Issue 7: TypeScript Errors
**Error:** Type errors even though code looks correct

**Solution:**
```bash
rm -rf .next node_modules
npm install
npm run build
```

### Issue 8: Backend Won't Start

**Check directory:** Make sure you're in `/backend/` not `/backend/backend/`
```bash
pwd
# Should show: .../data-connector-platform/backend
# NOT: .../data-connector-platform/backend/backend

# Correct location:
cd /home/amir/Desktop/projects/data-connector-platform/backend
python manage.py runserver 0.0.0.0:8000
```

---

## 🛠️ Development Tips

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
