# 🚀 Setup Scripts Guide

This document explains the setup scripts available for the Data Connector Platform.

## Available Scripts

### 1. **verify-setup.sh** - Setup Verification
**Purpose:** Check if your system has all prerequisites installed and properly configured.

**When to use:**
- Before starting any setup
- To diagnose why setup is failing
- To verify all dependencies are installed

**How to run:**
```bash
./verify-setup.sh
```

**What it checks:**
- ✓ Node.js, npm, Python, pip, Docker installed
- ✓ Frontend dependencies (Next.js, React)
- ✓ Backend dependencies (Django, database drivers)
- ✓ Docker configuration (docker-compose.yml, Dockerfiles)
- ✓ Configuration files present
- ✓ Port availability
- ✓ Disk space available

**Example output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ All checks passed! Your setup is ready.
```

---

### 2. **quick-start.sh** - Path A: Local Development (Recommended for Dev)
**Purpose:** Automated setup for local development with frontend and backend running locally.

**When to use:**
- You want to develop locally (fastest iteration)
- You want to debug without Docker overhead
- You have limited Docker resources

**How to run:**
```bash
./quick-start.sh
```

**What it does:**
1. ✓ Verifies Node.js, Python, npm installed
2. ✓ Installs frontend dependencies (`npm install`)
3. ✓ Builds Next.js application (`npm run build`)
4. ✓ Creates Python virtual environment
5. ✓ Installs backend dependencies
6. ✓ Starts database services in Docker (optional)
7. ✓ Runs Django migrations

**After setup, you need to start services manually:**

Terminal 1 - Frontend:
```bash
npm run dev
```

Terminal 2 - Backend:
```bash
cd backend
source .venv/bin/activate
python manage.py runserver
```

**Setup time:** ~5-10 minutes
**Advantages:**
- Faster development iteration
- Easier debugging (see full logs)
- Lower memory/CPU usage
- Better IDE integration (test debugger)

**Disadvantages:**
- Requires local Node.js and Python
- Need to manage 2-3 terminal windows
- Database still runs in Docker (requires Docker)

---

### 3. **docker-setup.sh** - Path B: Docker Setup (Recommended for Testing/CI)
**Purpose:** Complete automated Docker setup for the entire stack in containers.

**When to use:**
- You want production-like testing environment
- You want everything in one command
- You're setting up for CI/CD
- You want isolated environments

**How to run:**
```bash
./docker-setup.sh
```

**What it does:**
1. ✓ Verifies Docker and Docker Compose installed
2. ✓ Checks Docker memory allocation (recommends 6-8GB)
3. ✓ Pre-builds frontend locally (avoids SIGBUS errors)
4. ✓ Cleans up previous containers
5. ✓ Builds all Docker images
6. ✓ Starts all services
7. ✓ Runs database migrations
8. ✓ Performs health checks

**After setup, everything is running automatically:**

Access at:
- Frontend: http://localhost:3001
- Backend: http://localhost:8001
- PostgreSQL: localhost:5433

**Setup time:** ~10-20 minutes (depends on Docker build time)

**Advantages:**
- Everything in one place
- Easy to tear down/restart
- Production-like environment
- No local Python/Node.js needed
- Good for team setups (consistent environment)

**Disadvantages:**
- Requires Docker (4-6GB RAM recommended)
- Slower development iteration
- Harder to debug
- More resource intensive

---

## Quick Decision Guide

### Choosing Your Setup Path

| Question | Answer | Use Script |
|----------|--------|-----------|
| **I want to develop locally** | Yes | `quick-start.sh` |
| **I want everything automated** | Yes | `docker-setup.sh` |
| **I have limited memory** | Yes | `quick-start.sh` |
| **I want production-like testing** | Yes | `docker-setup.sh` |
| **I'm new to this project** | Yes | `quick-start.sh` |
| **I want to run CI/CD tests** | Yes | `docker-setup.sh` |
| **I'm debugging issues** | Yes | `verify-setup.sh` |
| **I just cloned the repo** | Yes | `verify-setup.sh` |

---

## Step-by-Step Usage

### First Time Setup

1. **Run verification:**
   ```bash
   ./verify-setup.sh
   ```
   Look for any ❌ errors and fix them.

2. **Choose your path:**
   - **For development:** `./quick-start.sh`
   - **For testing/CI:** `./docker-setup.sh`

3. **Start development:**
   - **Path A:** Open 2-3 terminals and run services
   - **Path B:** Everything is already running

### After Initial Setup

**Path A (Local Development):**
```bash
# Terminal 1
npm run dev

# Terminal 2
cd backend && source .venv/bin/activate && python manage.py runserver

# Terminal 3 (optional)
docker-compose logs -f db
```

**Path B (Docker):**
```bash
# Everything is running, just open browser
# Or check logs:
docker-compose logs -f backend
```

---

## Common Issues & Solutions

### Issue: "SIGBUS" Error During Docker Build

**Solution:** Use `docker-setup.sh` instead of manual `docker-compose build`
- The script pre-builds frontend locally to avoid this
- Or increase Docker memory to 6-8GB

```bash
./docker-setup.sh  # Handles SIGBUS automatically
```

### Issue: "Python not found"

**Solution:** Install Python first
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv

# macOS
brew install python3
```

Then run verification:
```bash
./verify-setup.sh
```

### Issue: "Docker not running"

**Solution:** Start Docker daemon
```bash
# Linux
sudo systemctl start docker

# macOS/Windows
# Open Docker Desktop application
```

Verify:
```bash
docker ps
```

### Issue: Port Already in Use

**Solution:** Check what's using the port
```bash
# Check port 3000
lsof -i :3000

# Kill process
kill -9 [PID]
```

Or use different ports:
```bash
# Frontend on 3001
npm run dev -- -p 3001

# Backend on 8001
python manage.py runserver 8001
```

---

## Manual Alternative to Scripts

If you prefer to set up manually without scripts, follow [SETUP.md](SETUP.md):

```bash
# Path A - Manual Local Setup
npm install
npm run build
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Path B - Manual Docker Setup
docker-compose up -d
docker-compose exec backend python manage.py migrate
```

---

## Next Steps After Setup

### Development
- See [NAVIGATION_AND_USER_GUIDE.md](NAVIGATION_AND_USER_GUIDE.md) for using the app
- See [README.md](README.md) for project overview
- See [TECHNICAL_SPECIFICATIONS.md](TECHNICAL_SPECIFICATIONS.md) for technical details

### Testing
- Backend tests: `python manage.py test`
- Integration tests: `cd tests && python test_all_databases.py`
- Frontend tests: (add with `npm test`)

### Deployment
- See [SETUP.md](SETUP.md) Troubleshooting section
- See Docker setup for production considerations

---

## Support & Troubleshooting

### Getting Help

1. **Run verification:**
   ```bash
   ./verify-setup.sh
   ```
   This will identify missing prerequisites.

2. **Check logs:**
   ```bash
   # Frontend logs
   npm run dev  # Look at console output
   
   # Backend logs
   python manage.py runserver  # Look at console output
   
   # Docker logs
   docker-compose logs -f [service-name]
   ```

3. **Read documentation:**
   - [SETUP.md](SETUP.md) - Detailed setup instructions and troubleshooting
   - [README.md](README.md) - Project overview
   - [TECHNICAL_SPECIFICATIONS.md](TECHNICAL_SPECIFICATIONS.md) - Architecture and design

4. **Common Issues:**
   - See [SETUP.md - Troubleshooting Guide](SETUP.md#troubleshooting-guide)

---

## Environment Variables

### Frontend (.env.local)
Create `.env.local` in project root if needed:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
Create `.env` in backend directory if needed:
```
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5433/dataconnector
```

---

## Performance Tips

### For Path A (Local Development)
- Use 1-2 terminal windows
- Frontend build takes ~5-10 seconds
- Backend startup is instant
- Hot reload works for both frontend and backend

### For Path B (Docker)
- Increase Docker memory to 6-8GB for faster builds
- First build takes 10-20 minutes, subsequent builds are faster
- Use `docker-compose logs -f backend` for real-time logs
- Services may take 10-15 seconds to start

---

**Happy coding! 🎉**

For more details, see [SETUP.md](SETUP.md)
