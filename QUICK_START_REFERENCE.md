# 📊 Setup Status & Quick Reference

**Generated:** April 14, 2026 | **Status:** ✅ Ready for Development

---

## 🎯 Current Project State

| Component | Status | Location |
|-----------|--------|----------|
| **Documentation** | ✅ Updated | See [SETUP.md](SETUP.md) |
| **Setup Scripts** | ✅ Created | See [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) |
| **Docker Config** | ✅ Fixed | docker-compose.yml (version key removed) |
| **Next.js Config** | ✅ Optimized | next.config.ts (build optimization) |
| **Dockerfile** | ✅ Optimized | Dockerfile.frontend (memory settings) |
| **Backend** | ✅ Ready | backend/ directory |
| **Frontend** | ✅ Ready | app/ directory |

---

## ⚡ Quick Start (2 Options)

### Option A: Local Development (Fastest - Recommended for Dev)
```bash
# 1. Run one command to set everything up
./quick-start.sh

# 2. After setup, open 2 terminal windows:

# Terminal 1 - Frontend
npm run dev
# Opens: http://localhost:3000

# Terminal 2 - Backend
cd backend && source .venv/bin/activate && python manage.py runserver
# Opens: http://localhost:8000
```

**⏱️ Setup time:** 5-10 minutes  
**💾 Resources:** ~2GB RAM  
**👥 Best for:** Active development, debugging

---

### Option B: Docker (All-in-One - Recommended for Testing)
```bash
# 1. Run one command to build and start everything
./docker-setup.sh

# 2. Everything starts automatically!
# Opens: http://localhost:3001 (frontend)
# Opens: http://localhost:8001 (backend)
```

**⏱️ Setup time:** 10-20 minutes  
**💾 Resources:** 4-6GB RAM (Docker)  
**👥 Best for:** Testing, CI/CD, team setup

---

## 🔍 Verify Your Setup

Before starting, check if everything is installed:

```bash
./verify-setup.sh
```

This checks:
- ✓ Node.js, npm, Python, pip installed
- ✓ All dependencies installed
- ✓ Docker configured correctly
- ✓ Ports available
- ✓ Disk space sufficient

---

## 📁 Project Structure

```
data-connector-platform/
├── app/                          # Next.js Frontend (React)
│   ├── components/               # React components
│   ├── api/                      # API routes
│   └── layout.tsx                # Main layout
├── backend/                      # Django Backend (Python)
│   ├── connector/                # Main app
│   ├── manage.py                 # Django CLI
│   └── requirements.txt           # Python dependencies
├── tests/                        # Integration tests
├── docker-compose.yml            # Docker services
├── Dockerfile.frontend           # Frontend container
├── Dockerfile.backend            # Backend container
└── SETUP.md                      # Detailed setup guide
```

---

## 🗄️ Database Connections

All databases run in Docker (even for local development):

| Database | Host | Port | User | Password | Database |
|----------|------|------|------|----------|----------|
| **PostgreSQL** | localhost | 5433 | user | password | dataconnector |
| **MySQL** | localhost | 3307 | user | password | testdb |
| **MongoDB** | localhost | 27018 | (none) | (none) | test |
| **ClickHouse** | localhost | 8124 | (default) | (none) | default |

**Connection from backend services:**
```
PostgreSQL:  postgresql://user:password@db:5432/dataconnector
MySQL:       mysql://user:password@mysql:3306/testdb
MongoDB:     mongodb://mongo:27017/test
ClickHouse:  http://clickhouse:8123
```

---

## 🚀 Available Commands

### Frontend Commands
```bash
npm run dev              # Start dev server (http://localhost:3000)
npm run build            # Build for production
npm start                # Start production server
npm run lint             # Run ESLint
```

### Backend Commands
```bash
cd backend
source .venv/bin/activate    # Activate virtual environment

python manage.py runserver   # Start dev server (http://localhost:8000)
python manage.py migrate     # Run database migrations
python manage.py createsuperuser  # Create admin user
python manage.py test        # Run backend tests
python manage.py shell       # Django interactive shell
```

### Docker Commands
```bash
docker-compose ps                    # Show running services
docker-compose logs -f backend       # View backend logs
docker-compose exec backend bash     # Shell into container
docker-compose down                  # Stop all services
docker-compose down -v               # Stop and remove volumes
docker-compose up -d                 # Start services in background
```

---

## 🐛 Troubleshooting Quick Reference

### Issue: SIGBUS Error During Docker Build
```bash
# Solution: The docker-setup.sh script handles this automatically
./docker-setup.sh
```

### Issue: Module Not Found / Dependencies Missing
```bash
# Frontend
npm install

# Backend
cd backend && source .venv/bin/activate && pip install -r requirements.txt
```

### Issue: Port Already in Use
```bash
# Find what's using the port
lsof -i :3000    # Check port 3000
lsof -i :8000    # Check port 8000

# Kill the process
kill -9 [PID]

# Or use different ports
npm run dev -- -p 3001
python manage.py runserver 8001
```

### Issue: Docker Not Running
```bash
# Linux
sudo systemctl start docker

# macOS/Windows
# Open Docker Desktop application

# Verify
docker ps
```

### Issue: Python Virtual Environment Issues
```bash
# Recreate virtual environment
cd backend
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**For more issues, see [SETUP.md - Troubleshooting](SETUP.md#troubleshooting-guide)**

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [SETUP.md](SETUP.md) | Complete setup instructions & troubleshooting |
| [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) | Guide to setup scripts |
| [README.md](README.md) | Project overview & features |
| [NAVIGATION_AND_USER_GUIDE.md](NAVIGATION_AND_USER_GUIDE.md) | How to use the application |
| [TECHNICAL_SPECIFICATIONS.md](TECHNICAL_SPECIFICATIONS.md) | Architecture & design |
| [CORE_FEATURES.md](CORE_FEATURES.md) | Features overview |

---

## 📋 Setup Checklist

After running setup scripts, verify:

- [ ] **Frontend loads:** http://localhost:3000 or 3001
- [ ] **Backend API responds:** http://localhost:8000/api or 8001/api
- [ ] **Database connections:** Can see data in connected databases
- [ ] **Admin panel works:** http://localhost:8000/admin (if superuser created)
- [ ] **No console errors:** Check browser DevTools (F12)
- [ ] **No Django errors:** Check terminal output for backend errors

---

## 🎓 Development Workflow

### For Local Development (Path A)

1. **Start services:**
   ```bash
   # Terminal 1
   npm run dev
   
   # Terminal 2
   cd backend && source .venv/bin/activate && python manage.py runserver
   ```

2. **Edit code:**
   - Frontend: Edit files in `app/` directory
   - Backend: Edit files in `backend/` directory
   - Changes auto-reload in development

3. **Test changes:**
   - Frontend: Refresh browser (http://localhost:3000)
   - Backend: Auto-reloads on save
   - Databases: Use `docker-compose exec db` to connect

### For Docker Development (Path B)

1. **Services run automatically:**
   - Frontend: http://localhost:3001
   - Backend: http://localhost:8001

2. **Edit code:**
   - Frontend & Backend: Edit files locally
   - Changes require Docker rebuild (slower)

3. **Rebuild after changes:**
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```

---

## 🔒 Demo User Credentials

### Fresh Start Approach
The system starts with **NO pre-populated connections or files**. Users create connections and extract data as needed.

### Demo Users (All same credentials for any user role)
```
👤 admin          / admin123      (Full system access)
👤 john_sales     / john123       (Sales user)
👤 sarah_analytics / sarah456     (Analytics user)
👤 mike_reporting / mike789       (Reporting user)
```

### Workflow
1. Log in with any demo user
2. Create database connection (PostgreSQL, MySQL, MongoDB, ClickHouse)
3. Extract data from tables
4. Stored files auto-generate and appear in Stored Files section
5. Extracted data auto-populates the Extracted Data section
6. Files > 24h old are automatically cleaned up

### Database Credentials (for connections within app)
- **PostgreSQL:** user/password
- **MySQL:** user/password
- **MongoDB:** No authentication (default)
- **ClickHouse:** default/no password

**Note:** Change demo credentials in production!

---

## 💡 Tips & Best Practices

### Performance
- For local dev: Use Path A (faster iteration)
- For testing: Use Path B (more realistic)
- Increase Docker memory to 6GB+ if using Path B

### Debugging
- Frontend: Use browser DevTools (F12)
- Backend: Check terminal output for errors
- Django: Use `python manage.py shell` for debugging
- Docker: Use `docker-compose logs -f [service]`

### Testing
```bash
# Run Django tests
cd backend && python manage.py test

# Run integration tests
cd tests && python test_all_databases.py

# Check specific database
python test_mysql.py
```

### Git
```bash
# Good commit messages
git add .
git commit -m "feat: add user authentication"

# Check status
git status
git log --oneline
```

---

## 🆘 Need Help?

1. **Check verification:**
   ```bash
   ./verify-setup.sh
   ```

2. **Read documentation:**
   - Full setup: [SETUP.md](SETUP.md)
   - Scripts guide: [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md)
   - Troubleshooting: [SETUP.md#troubleshooting-guide](SETUP.md#troubleshooting-guide)

3. **View logs:**
   ```bash
   # Frontend
   npm run dev  # Check console output
   
   # Backend
   python manage.py runserver  # Check console output
   
   # Docker
   docker-compose logs -f
   ```

4. **Common issues:**
   - Python not installed? Install Python 3.8+
   - Docker issues? Check Docker Desktop/daemon is running
   - Port conflicts? Use different port numbers
   - Build fails? Run `docker system prune -a` then retry

---

## 🚀 Next Steps

1. **Choose setup path:**
   - [ ] Path A: Local development (`./quick-start.sh`)
   - [ ] Path B: Docker setup (`./docker-setup.sh`)

2. **Verify setup:**
   ```bash
   ./verify-setup.sh
   ```

3. **Start development:**
   - See instructions above for your chosen path

4. **Explore the app:**
   - See [NAVIGATION_AND_USER_GUIDE.md](NAVIGATION_AND_USER_GUIDE.md)

5. **Read about implementation:**
   - See [TECHNICAL_SPECIFICATIONS.md](TECHNICAL_SPECIFICATIONS.md)

---

**Status: ✅ Ready to use!**

Last Updated: April 14, 2026  
For issues or questions, see SETUP.md or SCRIPTS_GUIDE.md
