# ✅ CODE FIXES IMPLEMENTATION GUIDE

**Status:** Ready to Implement  
**Difficulty:** Low to Medium  
**Estimated Time:** 15-20 minutes  

---

## 📋 FIXES AT A GLANCE

| Fix # | Issue | File | Lines | Difficulty |
|-------|-------|------|-------|------------|
| 1 | API URL Hardcoding | app/lib/api.ts | 3 | 🟢 Easy |
| 2 | Duplicate API_URL | app/page.tsx | 15 | 🟢 Easy |
| 3 | CORS Config | backend/settings.py | 145-158 | 🟡 Medium |
| 4 | Media Volume | docker-compose.yml | 35-40 | 🟢 Easy |
| 5 | Frontend Env Vars | docker-compose.yml | 5-13 | 🟢 Easy |
| 6 | ConnectionForm Defaults | app/components/ConnectionForm.tsx | 15-17 | 🟡 Medium |

---

## ✅ FIX #1: Make API URL Environment-Aware

### Current Code
```typescript
// app/lib/api.ts (Line 3)
export const API_URL = 'http://localhost:8001/api';
```

### Fixed Code
```typescript
// app/lib/api.ts (Line 3)
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api';

export { API_URL };
```

### Explanation
- Uses `NEXT_PUBLIC_` prefix so Next.js makes it available to browser
- Falls back to localhost:8001 if environment variable not set
- In Docker, `NEXT_PUBLIC_API_URL` will be set to `http://backend:8000/api`

### Implementation Steps

```bash
# 1. Open the file
cd /path/to/data-connector-platform

# 2. Edit app/lib/api.ts
# Find line 3: export const API_URL = 'http://localhost:8001/api';
# Replace with above code

# 3. Verify the change
grep -n "NEXT_PUBLIC_API_URL" app/lib/api.ts
# Should output: 1:const API_URL = process.env.NEXT_PUBLIC_API_URL || ...
```

---

## ✅ FIX #2: Remove Duplicate API_URL from page.tsx

### Current Code
```typescript
// app/page.tsx (Line 15)
const API_URL = 'http://localhost:8001/api';
```

### Fixed Code
```typescript
// app/page.tsx (Line 15)
import { API_URL } from './lib/api';
// Delete the const API_URL line
```

### Explanation
- Removes hardcoded duplicate
- Imports from api.ts which now uses environment variable
- Single source of truth for API_URL

### Implementation Steps

```bash
# 1. Open app/page.tsx
# 2. Find line 15: const API_URL = 'http://localhost:8001/api';
# 3. Add import at top: import { API_URL } from './lib/api';
# 4. Delete line 15 entirely

# 5. Verify the file imports API_URL correctly
head -20 app/page.tsx | grep -i "api"
```

---

## ✅ FIX #3: Update Backend CORS Settings

### Current Code
```python
# backend/backend/settings.py (Lines 145-158)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]
```

### Fixed Code
```python
# backend/backend/settings.py (Lines 145-180)
import os

# Detect Docker environment
IS_DOCKER = os.getenv('DOCKER_ENV') == '1'

if IS_DOCKER:
    # Docker environment - use service names
    CORS_ALLOWED_ORIGINS = [
        "http://frontend:3000",   # Frontend service in Docker
        "http://backend:8000",    # Backend service in Docker
        "http://localhost:3001",  # Allow host access too
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://frontend:3000",
        "http://backend:8000",
        "http://localhost:3001",
    ]
else:
    # Local development
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]

CORS_ALLOW_CREDENTIALS = True
```

### Explanation
- Checks `DOCKER_ENV` environment variable set by docker-compose
- In Docker: Uses service names (`frontend:3000`, `backend:8000`)
- Locally: Uses localhost as before
- Allows CORS requests from correct origins

### Implementation Steps

```bash
# 1. Open backend/backend/settings.py
# 2. Find line 1 - verify imports
# 3. Check if 'import os' exists - it should already be there

# 4. Find the CORS_ALLOWED_ORIGINS section around line 145
# 5. Replace entire section with fixed code above

# 6. Verify changes
grep -n "IS_DOCKER\|CORS_ALLOWED_ORIGINS" backend/backend/settings.py
```

---

## ✅ FIX #4: Add Media Volume to Docker Compose

### Current Code
```yaml
# docker-compose.yml
services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3001:3000"
    depends_on:
      - backend
    networks:
      - app-network

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8001:8000"
    # ... rest of config

networks:
  app-network:
    driver: bridge
```

### Fixed Code
```yaml
# docker-compose.yml
services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3001:3000"
    depends_on:
      - backend
    networks:
      - app-network

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
      - backend-media:/app/media      # ← ADD THIS LINE
    ports:
      - "8001:8000"
    # ... rest of config

  # ... other services ...

volumes:
  backend-media:                       # ← ADD THIS SECTION

networks:
  app-network:
    driver: bridge
```

### Explanation
- Defines named volume `backend-media` that persists between container restarts
- Mounts it at `/app/media` in backend container
- Media files now survive container restart
- Files accessible from backend service

### Implementation Steps

```bash
# 1. Open docker-compose.yml
# 2. Find backend service volumes section
# 3. Add: - backend-media:/app/media

# 4. At end of file, before 'networks:', add:
# volumes:
#   backend-media:

# 5. Verify syntax (must be valid YAML)
docker-compose config > /dev/null
# Should succeed without errors

# 6. Restart containers to apply changes
docker-compose down -v
docker-compose up -d
```

---

## ✅ FIX #5: Add Environment Variables to Frontend

### Current Code
```yaml
# docker-compose.yml
frontend:
  build:
    context: .
    dockerfile: Dockerfile.frontend
  ports:
    - "3001:3000"
  depends_on:
    - backend
  networks:
    - app-network
```

### Fixed Code
```yaml
# docker-compose.yml
frontend:
  build:
    context: .
    dockerfile: Dockerfile.frontend
  ports:
    - "3001:3000"
  environment:                                          # ← ADD SECTION
    - NEXT_PUBLIC_API_URL=http://backend:8000/api      # ← ADD THIS
    - NEXT_PUBLIC_IS_DOCKER=true                        # ← ADD THIS
  depends_on:
    - backend
  networks:
    - app-network
```

### Explanation
- `NEXT_PUBLIC_API_URL`: Frontend knows backend is at `http://backend:8000/api`
- `NEXT_PUBLIC_IS_DOCKER`: Frontend detects it's running in Docker
- Used by environment-aware code in ConnectionForm

### Implementation Steps

```bash
# 1. Open docker-compose.yml
# 2. Find 'frontend:' service section
# 3. Add 'environment:' section with two lines

# 4. Verify indentation (YAML is strict about spaces)
docker-compose config > /dev/null
# Should succeed

# 5. Rebuild and restart
docker-compose down
docker-compose up -d
```

---

## ✅ FIX #6: Update ConnectionForm Default Host

### Current Code
```typescript
// app/components/ConnectionForm.tsx (Lines 15-17)
const DEFAULT_PORTS = {
  postgresql: 5432,
  mysql: 3306,
  mongodb: 27017,
  clickhouse: 9000,
} as const;

const DEFAULT_HOST = 'localhost';
```

### Fixed Code
```typescript
// app/components/ConnectionForm.tsx (Lines 15-26)
// Detect if running in Docker
const IS_DOCKER = typeof process !== 'undefined' && 
  process.env.NEXT_PUBLIC_IS_DOCKER === 'true';

// Default host depends on environment
const DEFAULT_HOST = IS_DOCKER ? 'db' : 'localhost';

// Default ports - container ports are used regardless
const DEFAULT_PORTS = {
  postgresql: 5432,
  mysql: 3306,
  mongodb: 27017,
  clickhouse: 9000,
} as const;
```

### Explanation
- Checks `NEXT_PUBLIC_IS_DOCKER` environment variable
- In Docker: Defaults to 'db' (PostgreSQL service name)
- Locally: Defaults to 'localhost'
- Users can override manually if needed

### Implementation Steps

```bash
# 1. Open app/components/ConnectionForm.tsx
# 2. Find lines 15-17 with DEFAULT_PORTS and DEFAULT_HOST
# 3. Replace with fixed code above

# 4. Verify file syntax
npm run build
# Should compile without errors

# 5. Test locally
npm run dev
# Form should still show correct defaults
```

### Note on Port Numbers
The port numbers (5432, 3306, etc.) are **container internal ports**, not external ports:
- When running locally and connecting to Docker database: Use 5433 (host port mapped to 5432)
- When running in Docker container connecting to another container: Use 5432 (internal port)
- The ConnectionForm shows internal ports (5432) which is correct for Docker connections
- For local connections, users would connect to 5433 (or change in connection string)

---

## 🧪 VERIFICATION CHECKLIST

After implementing all fixes, verify each one:

### ✅ Verify Fix #1: API URL Environment Variable
```bash
# 1. Check app/lib/api.ts
grep -n "NEXT_PUBLIC_API_URL" app/lib/api.ts
# Should show: const API_URL = process.env.NEXT_PUBLIC_API_URL || ...

# 2. Check compiled code
npm run build
# Should succeed

# 3. Run locally
npm run dev
# Check console in DevTools: All API calls should go to http://localhost:8001/api
```

### ✅ Verify Fix #2: No Duplicate API_URL
```bash
# Check page.tsx doesn't have duplicate
grep -c "const API_URL" app/page.tsx
# Should output: 0 (not found)

grep "import.*API_URL" app/page.tsx
# Should output: import statement from api.ts
```

### ✅ Verify Fix #3: CORS Configuration
```bash
# Check backend/settings.py has IS_DOCKER check
grep -n "IS_DOCKER\|os.getenv.*DOCKER" backend/backend/settings.py
# Should show the docker detection code

# Test locally
python manage.py check
# Should show: System check identified no issues

# Test CORS (if running)
curl -X GET http://localhost:8000/api/ \
  -H "Origin: http://localhost:3001" \
  -v
# Should NOT have CORS error
```

### ✅ Verify Fix #4: Media Volume
```bash
# Check docker-compose.yml has volume
grep -n "backend-media" docker-compose.yml
# Should show 2 lines: one in backend volumes, one in top-level volumes

# Verify syntax
docker-compose config > /dev/null
# Should succeed

# After running Docker, verify volume exists
docker volume ls | grep backend-media
# Should show: app_backend-media
```

### ✅ Verify Fix #5: Frontend Environment Variables
```bash
# Check docker-compose.yml has environment section
grep -n "NEXT_PUBLIC_API_URL\|NEXT_PUBLIC_IS_DOCKER" docker-compose.yml
# Should show both variables

# Verify syntax
docker-compose config > /dev/null
# Should succeed
```

### ✅ Verify Fix #6: ConnectionForm Defaults
```bash
# Check ConnectionForm has Docker detection
grep -n "IS_DOCKER\|NEXT_PUBLIC_IS_DOCKER" app/components/ConnectionForm.tsx
# Should show the detection code

# Verify syntax
npm run build
# Should succeed
```


# 2. Start frontend
npm run dev
# Should open: http://localhost:3000
# Check DevTools Network: Requests to http://localhost:8001/api

# 3. In separate terminal, start backend
cd backend
source .venv/bin/activate
python manage.py runserver
# Should show: Starting development server at http://127.0.0.1:8000/

# 4. In browser, try creating a connection
# Should succeed - Connection form shows default: postgresql, localhost:5432
```

### Step 2: Test Docker Deployment

```bash
# 1. Restart Docker with new configuration
docker-compose down -v
docker-compose up -d

# 2. Wait for services to start
sleep 20

# 3. Check logs
docker-compose logs frontend
# Should see: Ready in X.XXs

docker-compose logs backend
# Should see: Starting development server at 0.0.0.0:8000

# 4. Open browser to http://localhost:3001
# Should load without errors

# 5. Try creating a connection
# Form should show: postgresql, db:5432 (or localhost:5432)
```

### Step 3: Test API Communication

```bash
# From host machine:
curl -X GET http://localhost:8001/api/connections/ \
  -H "Content-Type: application/json"
# Should return: [] (empty list) or list of connections

# From frontend container:
docker-compose exec frontend curl http://backend:8000/api/connections/
# Should return same response

# Check frontend container can reach backend
docker-compose exec frontend ping -c 2 backend
# Should show: replies from backend
```

### Step 4: Test Media File Persistence

```bash
# 1. Create a connection and extract data (using UI)
# Files should appear in: backend/media/

# 2. Restart containers
docker-compose restart backend

# 3. Check files still exist
docker-compose exec backend ls -la /app/media/
# Files should still be there ✅

# 4. Or with full restart
docker-compose down
docker-compose up -d
sleep 15

# 5. Check files still exist
docker-compose exec backend ls -la /app/media/
# Files should still be there ✅
```

---

## 🆘 TROUBLESHOOTING

### Issue: CORS Error Still Appears

**Symptom:** `CORS policy: ...` error in DevTools console

**Solution:**
1. Verify `DOCKER_ENV=1` is set: `docker-compose exec backend env | grep DOCKER_ENV`
2. Check CORS config was updated: `grep -n "IS_DOCKER" backend/backend/settings.py`
3. Restart backend: `docker-compose restart backend`
4. Check logs: `docker-compose logs backend | grep -i cors`

### Issue: API URL Still Hardcoded

**Symptom:** Frontend still connects to localhost:8001 instead of backend:8000

**Solution:**
1. Verify env var set: `docker-compose config | grep NEXT_PUBLIC_API_URL`
2. Check code was updated: `grep -n "NEXT_PUBLIC_API_URL" app/lib/api.ts`
3. Rebuild frontend: `docker-compose build frontend --no-cache`
4. Restart: `docker-compose down && docker-compose up -d`

### Issue: Media Files Lost After Restart

**Symptom:** Files in media folder disappear after container restart

**Solution:**
1. Verify volume added: `grep -n "backend-media" docker-compose.yml`
2. Check volume exists: `docker volume ls | grep backend-media`
3. Remove old containers: `docker-compose down -v`
4. Recreate with volume: `docker-compose up -d`

### Issue: Cannot Connect to Database from Docker

**Symptom:** `Failed to connect to db`

**Solution:**
1. Check database service is running: `docker-compose ps | grep db`
2. Test connection from backend: `docker-compose exec backend psql -h db -U user -d dataconnector -c "SELECT 1"`
3. Verify `translate_docker_host` function is working: `docker-compose logs backend | grep -i "connect"`

---

## 📝 IMPLEMENTATION SUMMARY

| Component | Current | Fixed | Impact |
|-----------|---------|-------|--------|
| API URL | Hardcoded | Environment variable | ✅ Works in any environment |
| CORS | Localhost only | Docker-aware | ✅ Works in Docker |
| Media | Ephemeral | Persisted volume | ✅ Data survives restart |
| Frontend Env | None | NEXT_PUBLIC_* vars | ✅ Docker detection |
| DB Defaults | localhost | Service-aware | ✅ Works in Docker |
| Env Files | Missing | Created | ✅ Configuration clarity |

---

## 🎯 NEXT: Run Fixes

Proceed to implement fixes in this order:

1. **Fix #1-2 (5 min):** Update API URLs
2. **Fix #3 (5 min):** Update CORS settings
3. **Fix #4-5 (5 min):** Docker compose changes
4. **Fix #6 (5 min):** ConnectionForm defaults
5. **Test (10 min):** Run verification checklist

**Total Time:** ~30 minutes (including testing)

