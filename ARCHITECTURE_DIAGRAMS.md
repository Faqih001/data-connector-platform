# 🏗️ ARCHITECTURE & DATA FLOW DIAGRAMS

**Purpose:** Visual representation of port issues, API communication, and data flow  
**Audience:** Developers and architects  
**Format:** ASCII diagrams and flow charts

---

## 📊 ISSUE 1: API COMMUNICATION FLOW

### Current Flow (BROKEN in Docker)

```
LOCAL DEVELOPMENT (WORKS ✅):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────┐
│ Host Machine                                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  Browser Window                                 │
│  ┌──────────────────────┐                       │
│  │ http://localhost:3000│                       │
│  │                      │                       │
│  │ fetch(               │                       │
│  │'http://localhost:    │                       │
│  │    8001/api')        │                       │
│  └──────────┬───────────┘                       │
│             │                                   │
│             │ (Goes through host OS)           │
│             ↓                                   │
│  ┌─────────────────────────────┐                │
│  │ Port 8001 → Kernel Routes   │                │
│  │            → localhost:8001  │                │
│  │            → 127.0.0.1:8001  │                │
│  │ ✅ Backend listening here!   │                │
│  └─────────────────────────────┘                │
│             │                                   │
│             ↓                                   │
│  ┌─────────────────────────────┐                │
│  │ Django Backend              │                │
│  │ manage.py runserver 0.0.0.0 │                │
│  │ Listening on :8000          │                │
│  │ Mapped to :8001 externally  │                │
│  └─────────────────────────────┘                │
│                                                 │
└─────────────────────────────────────────────────┘


DOCKER ENVIRONMENT - BEFORE FIX (BROKEN ❌):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        Docker Bridge Network (app-network)
    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║  ┌──────────────────────────────────────┐ ║
    ║  │ Frontend Container                   │ ║
    ║  │ http://frontend:3000                 │ ║
    ║  │                                      │ ║
    ║  │ fetch(                               │ ║
    ║  │ 'http://localhost:8001/api')         │ ║
    ║  │                                      │ ║
    ║  │ Problem: localhost in container      │ ║
    ║  │ resolves to 127.0.0.1 in container  │ ║
    ║  │                                      │ ║
    ║  │ Container looks at its own network:  │ ║
    ║  │ No port 8001 listening! ❌           │ ║
    ║  │                                      │ ║
    ║  │ ┌──────────────────────────────────┐ │ ║
    ║  │ │ Connection refused error!        │ │ ║
    ║  │ │ http://localhost:8001/api        │ │ ║
    ║  │ │ Socket not found                 │ │ ║
    ║  │ └──────────────────────────────────┘ │ ║
    ║  └──────────────────────────────────────┘ ║
    ║                                            ║
    ║  ┌──────────────────────────────────────┐ ║
    ║  │ Backend Container                    │ ║
    ║  │ Service: backend                     │ ║
    ║  │ Port 8000 listening                  │ ║
    ║  │ (But frontend can't reach it!)       │ ║
    ║  └──────────────────────────────────────┘ ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
           ↑
           │
           └─ COMMUNICATION BLOCKED!


DOCKER ENVIRONMENT - AFTER FIX (WORKS ✅):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        Docker Bridge Network (app-network)
    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║  ┌──────────────────────────────────────┐ ║
    ║  │ Frontend Container                   │ ║
    ║  │ http://frontend:3000                 │ ║
    ║  │                                      │ ║
    ║  │ fetch(                               │ ║
    ║  │ 'http://backend:8000/api')           │ ║
    ║  │  (From NEXT_PUBLIC_API_URL env var) │ ║
    ║  │                                      │ ║
    ║  │ Docker DNS resolves 'backend'       │ ║
    ║  │ to backend service ✅                │ ║
    ║  └──────────────────────────────────────┘ ║
    ║           │                                ║
    ║           │ Service name resolution        ║
    ║           ↓                                ║
    ║  ┌──────────────────────────────────────┐ ║
    ║  │ Backend Container                    │ ║
    ║  │ Service: backend:8000                │ ║
    ║  │ ✅ CONNECTED!                        │ ║
    ║  │                                      │ ║
    ║  │ Response headers:                    │ ║
    ║  │ Access-Control-Allow-Origin:         │ ║
    ║  │ http://frontend:3000 ✅ (CORS OK)    │ ║
    ║  └──────────────────────────────────────┘ ║
    ║           │                                ║
    ║           ↓                                ║
    ║  ┌──────────────────────────────────────┐ ║
    ║  │ Database Services                    │ ║
    ║  │ - db:5432 (PostgreSQL)               │ ║
    ║  │ - mysql:3306 (MySQL)                 │ ║
    ║  │ - mongo:27017 (MongoDB)              │ ║
    ║  │ - clickhouse:8123 (ClickHouse)      │ ║
    ║  └──────────────────────────────────────┘ ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
```

---

## 🔐 ISSUE 2: CORS POLICY BLOCKING

### CORS Error Sequence (BEFORE FIX)

```
Frontend (in Docker)                Backend (in Docker)
─────────────────────────           ──────────────────

fetch('http://backend:8000/api')
        │
        ├─ Request Headers:
        │  Origin: http://frontend:3000
        │  Content-Type: application/json
        │  (credentials: include)
        │
        └────→ [HTTP Request]

                            Backend receives:
                            - Request from: http://frontend:3000
                            - Check CORS config...
                            - Allowed origins: [
                            -   "http://localhost:3000",  ← Nope
                            -   "http://127.0.0.1:3000",  ← Nope
                            -   "http://localhost:3001",  ← Nope
                            -   "http://127.0.0.1:3001"   ← Nope
                            - ]
                            - http://frontend:3000 NOT in list
                            ❌ CORS VIOLATION

                            Response Headers:
                            - Access-Control-Allow-Origin: 
                              http://localhost:3001
                            - (Browser rejects this)

        ←────── [HTTP Response]
        │
        └─ Browser CORS Check:
           Request origin: http://frontend:3000
           Allowed origin: http://localhost:3001
           ❌ MISMATCH!
           
           Console Error:
           CORS policy: The value of the
           'Access-Control-Allow-Origin' header
           in the response must not be the
           wildcard '*' when the request's
           credentials mode is 'include'.


FIXED CORS FLOW (AFTER FIX)
──────────────────────────

Frontend (in Docker)                Backend (in Docker)
─────────────────────────           ──────────────────

fetch('http://backend:8000/api')
        │
        ├─ Request Headers:
        │  Origin: http://frontend:3000
        │
        └────→ [HTTP Request]

                            Backend checks:
                            IS_DOCKER = os.getenv('DOCKER_ENV')
                            ✅ True (set in docker-compose)
                            
                            Use Docker CORS config:
                            - Allowed origins: [
                            -   "http://frontend:3000", ✅ Match!
                            -   "http://backend:8000",
                            -   "http://localhost:3001"
                            - ]

                            Response Headers:
                            - Access-Control-Allow-Origin:
                              http://frontend:3000 ✅
                            - Access-Control-Allow-Credentials:
                              true

        ←────── [HTTP Response] ✅ SUCCESS!
        │
        └─ Browser CORS Check:
           Request origin: http://frontend:3000
           Allowed origin: http://frontend:3000
           ✅ MATCH!
           
           Response processed successfully
           Data available in JavaScript
```

---

## 💾 ISSUE 3: MEDIA FILE PERSISTENCE

### Data Storage Flow

```
FILE STORAGE COMPARISON:

Local Development (WORKS):
───────────────────────

┌─────────────────────────────────────────────────┐
│ Host Machine (/path/to/project)                │
├─────────────────────────────────────────────────┤
│                                                 │
│  User: Extract data from MySQL                 │
│  ↓                                              │
│  Backend process                                │
│  ↓                                              │
│  Save: /app/media/extraction_mysql_001.json    │
│  ↓                                              │
│  Volume mapped: ./backend → /app (in container)│
│  ↓                                              │
│  Actual disk location:                          │
│  ./backend/media/extraction_mysql_001.json     │
│  ↓                                              │
│  🎯 On host filesystem → Persistent!            │
│  ↓                                              │
│  Even if container stops: Files still there ✅  │
│                                                 │
└─────────────────────────────────────────────────┘


Docker (BEFORE FIX - BROKEN):
──────────────────────────

┌──────────────────────────────────┐
│ Container Filesystem             │
│ (Ephemeral - deleted on restart) │
├──────────────────────────────────┤
│                                  │
│  /app/media/                     │
│  ├─ extraction_mysql_001.json   │
│  ├─ extraction_pg_002.json       │
│  └─ extraction_ch_003.json       │
│                                  │
│  Container stops/restarts        │
│          ↓                        │
│  ❌ Container filesystem DELETED  │
│  ❌ All files GONE               │
│  ❌ Database still has references│
│  ❌ Links return 404 Not Found   │
│                                  │
└──────────────────────────────────┘


Docker (AFTER FIX - WORKS):
──────────────────────────

┌──────────────────────────────────┐   ┌──────────────────────┐
│ Container Filesystem             │   │ Docker Named Volume  │
│ (Ephemeral)                      │   │ (Persistent)         │
├──────────────────────────────────┤   ├──────────────────────┤
│                                  │   │                      │
│  /app                            │   │ backend-media volume │
│  ├─ manage.py                    │   │ ├─ extraction_001   │
│  ├─ connector/                   │   │ ├─ extraction_002   │
│  ├─ backend/                     │   │ └─ extraction_003   │
│  └─ /app/media ──┐               │   │                      │
│  [deleted]      └──→ MOUNTED TO ─┼─→ │ extraction_*.json   │
│                                  │   │ (Persists on disk)  │
│  Container stops                 │   │                      │
│          ↓                        │   │ Container restarts  │
│  Container filesystem deleted    │   │          ↓           │
│  Container restarted             │   │ Volume re-mounts    │
│          ↓                        │   │ Files still there! ✅
│  New container started           │   │                      │
│  /app/media re-mounted ←─────────┼─→ │ All data intact ✅   │
│  FROM the volume!                │   │                      │
│                                  │   │                      │
└──────────────────────────────────┘   └──────────────────────┘

         ↓ API Call
  GET /media/extraction_001.json
         ↓
  ✅ File found (from volume)
  ✅ Downloaded successfully
```

---

## 🔀 ISSUE 4: PORT MAPPING - INTERNAL VS EXTERNAL

### Port Routing Diagram

```
HOW PORT MAPPINGS WORK:

docker-compose.yml:
  backend:
    ports:
      - "8001:8000"
        ↑    ↑
     Host  Container
     Port  Port


REQUEST FROM HOST MACHINE:
──────────────────────────

┌─────────────────────────────────────────┐
│ Host Machine (Your Computer)            │
├─────────────────────────────────────────┤
│                                         │
│ Browser: http://localhost:8001/api      │
│            │                            │
│            ↓                            │
│ OS Kernel Routes:                       │
│ localhost:8001 → 127.0.0.1:8001         │
│                                         │
│ Docker Daemon intercepts:               │
│ 0.0.0.0:8001 → container:8000           │
│                                         │
│ ✅ Backend listening on :8000 inside   │
│                                         │
└─────────────────────────────────────────┘


REQUEST FROM INSIDE DOCKER CONTAINER:
─────────────────────────────────────

┌──────────────────────────────────────────┐
│ Docker Bridge Network                    │
├──────────────────────────────────────────┤
│                                          │
│ ┌────────────────────────────────────┐  │
│ │ Frontend Container (IP: 172.18.0.2)│  │
│ │                                    │  │
│ │ ❌ WRONG:                          │  │
│ │ fetch('http://localhost:8001')    │  │
│ │           │                        │  │
│ │           ↓                        │  │
│ │ Container DNS: localhost = self   │  │
│ │ Routes to 127.0.0.1:8001 IN       │  │
│ │ CONTAINER, not the host!          │  │
│ │ ❌ FAILS - No service there       │  │
│ │                                    │  │
│ │ ✅ CORRECT:                        │  │
│ │ fetch('http://backend:8000')      │  │
│ │           │                        │  │
│ │           ↓                        │  │
│ │ Docker DNS: backend = service     │  │
│ │ Routes through bridge to:         │  │
│ │ backend container:8000            │  │
│ │ ✅ SUCCESS!                        │  │
│ └────────────────────────────────────┘  │
│           ↓ (via bridge)                 │
│ ┌────────────────────────────────────┐  │
│ │ Backend Container (IP: 172.18.0.3) │  │
│ │ Listening on 0.0.0.0:8000          │  │
│ │ ✅ Request received                 │  │
│ └────────────────────────────────────┘  │
│                                          │
└──────────────────────────────────────────┘


PORT MAPPING REFERENCE TABLE:
────────────────────────────

Service          Host:Container    Access From...
             Port Mapping       Host Machine      Container
─────────────────────────────────────────────────────────────
Frontend     3001:3000          localhost:3001    frontend:3000
Backend      8001:8000          localhost:8001/api backend:8000/api
PostgreSQL   5433:5432          localhost:5433    db:5432
MySQL        3307:3306          localhost:3307    mysql:3306
MongoDB      27018:27017        localhost:27018   mongo:27017
ClickHouse   8124:8123          localhost:8124    clickhouse:8123

KEY RULE:
┌──────────────────────────────────────────────────┐
│ Use LEFT number (host port)  = From Host Machine│
│ Use RIGHT number (container port) = Inside Docker│
│ Use SERVICE NAME (not localhost) = Inside Docker │
└──────────────────────────────────────────────────┘
```

---

## 📡 COMPLETE REQUEST FLOW

### Successful Request Flow (After All Fixes)

```
USER CLICKS "Create Connection" IN DOCKER
═══════════════════════════════════════════

1. UI EVENT
   ┌─────────────────────────────────┐
   │ ConnectionForm.tsx              │
   │ User fills:                     │
   │ - Name: "My PostgreSQL"         │
   │ - Type: PostgreSQL              │
   │ - Host: db (from IS_DOCKER)    │
   │ - Port: 5432 (container port)   │
   │ - User: admin                   │
   │ - Pass: ****                    │
   │                                 │
   │ onClick: onSubmit()             │
   └────────────┬────────────────────┘
                │

2. API CALL
   ┌─────────────────────────────────┐
   │ app/lib/api.ts                  │
   │ createConnection()              │
   │                                 │
   │ Fetch URL:                      │
   │ ${API_URL}/connections/         │
   │ (API_URL from NEXT_PUBLIC_...) │
   │ = http://backend:8000/api ✅    │
   │                                 │
   │ Headers:                        │
   │ - Origin: http://frontend:3000 │
   │ - X-CSRFToken: [token]         │
   │ - Content-Type: application/json│
   └────────────┬────────────────────┘
                │
                ↓ (Through bridge network)

3. CORS CHECK (Django Backend)
   ┌─────────────────────────────────┐
   │ backend/backend/settings.py     │
   │                                 │
   │ IS_DOCKER = True                │
   │ CORS_ALLOWED_ORIGINS = [        │
   │   "http://frontend:3000" ✅     │
   │   "http://backend:8000"         │
   │   "http://localhost:3001"       │
   │ ]                               │
   │                                 │
   │ Check: Request origin in list?  │
   │ http://frontend:3000 ✅ YES!    │
   └────────────┬────────────────────┘
                │

4. REQUEST PROCESSING
   ┌─────────────────────────────────┐
   │ backend/connector/views.py      │
   │ @api_view(['POST'])             │
   │ def create_connection(request): │
   │                                 │
   │ - Parse request body            │
   │ - Validate data                 │
   │ - Encrypt password              │
   │ - Save to database              │
   │ - Return connection ID          │
   └────────────┬────────────────────┘
                │

5. RESPONSE
   ┌─────────────────────────────────┐
   │ Response Headers:               │
   │ - Access-Control-Allow-Origin:  │
   │   http://frontend:3000 ✅       │
   │ - Access-Control-Allow-Cred:    │
   │   true                          │
   │ - Content-Type:                 │
   │   application/json              │
   │                                 │
   │ Response Body:                  │
   │ {                               │
   │   "id": 42,                     │
   │   "name": "My PostgreSQL",      │
   │   "db_type": "postgresql",      │
   │   "host": "db",                 │
   │   "port": 5432,                 │
   │   "created_at": "..."           │
   │ }                               │
   └────────────┬────────────────────┘
                │
                ↓ (Back through bridge network)

6. BROWSER PROCESSING
   ┌─────────────────────────────────┐
   │ Frontend (app/page.tsx)         │
   │                                 │
   │ - Receive response              │
   │ - Parse JSON                    │
   │ - Check CORS headers ✅         │
   │ - Update state: setConnections  │
   │ - Re-render with new connection │
   │                                 │
   │ ✅ UI shows: "Connection saved" │
   └─────────────────────────────────┘


THEN USER CLICKS "Extract Data"
════════════════════════════════

1. Extract Data Request
   fetch(`${API_URL}/connections/42/extract_data/`, {
     POST: { table_name: "campaigns" }
   })
   = http://backend:8000/api/connections/42/extract_data/

2. Backend connects to database
   connector = PostgresConnector(connection_details)
   connector.connect()
   
   In connectors.py:
   host = translate_docker_host('db', 'postgresql', 5432)
   = 'db' (because DOCKER_ENV=1)
   
   psycopg2.connect(
     host='db',        ← Docker service name ✅
     port=5432,        ← Container port ✅
     user='admin',
     database='mydb'
   )

3. Data is extracted and saved
   filepath = /app/media/extraction_pg_001.json
   (mounted to backend-media volume ✅ persists)

4. Response with file URL
   {
     "data": [...rows...],
     "file_url": "/media/extraction_pg_001.json"
   }

5. Download works even after restart!
   GET /media/extraction_pg_001.json
   └─ Served from backend-media volume
   └─ File exists even after container restart ✅
```

---

## 📈 DATA FLOW: END-TO-END

```
USER PERSPECTIVE (What they see):

┌─────────────────────────────────────────────────┐
│ Step 1: Open http://localhost:3001              │
│ ┌──────────────────────────────────────────────┐│
│ │ [Data Connector Platform]                   ││
│ │ ┌─ Connections ┌─ Extract Data ┌─ Files ──┐││
│ │                                             ││
│ │ Step 2: Create Connection                   ││
│ │ Database Type: PostgreSQL ▼                 ││
│ │ Host: db [filled from DOCKER]               ││
│ │ Port: 5432 [correct container port]         ││
│ │ Username: admin                             ││
│ │ Password: ****                              ││
│ │ Database: campaigns                         ││
│ │ [Create Connection]                         ││
│ │                                             ││
│ │ ✅ Connection created!                      ││
│ │                                             ││
│ │ Step 3: Extract Data                        ││
│ │ Connection: My PostgreSQL ▼                 ││
│ │ Table: campaigns ▼                          ││
│ │ [Extract Data]                              ││
│ │                                             ││
│ │ ✅ Data extracted and saved!                ││
│ │ extraction_pg_campaigns_01.json             ││
│ │                                             ││
│ │ Step 4: Download File                       ││
│ │ [Download] extraction_pg_campaigns_01.json  ││
│ │                                             ││
│ │ ✅ File downloaded successfully!            ││
│ │                                             ││
│ └──────────────────────────────────────────────┘│
│                                                 │
│ Step 5: Restart containers                      │
│ $ docker-compose restart                        │
│                                                 │
│ Step 6: Files still available!                  │
│ Open http://localhost:3001/files                │
│ extraction_pg_campaigns_01.json ✅              │
│ [Download] ← Still works after restart!        │
│                                                 │
└─────────────────────────────────────────────────┘


SYSTEM PERSPECTIVE (What happens behind the scenes):

┌─────────────────────────────────────────────────────────┐
│ BEFORE FIXES (BROKEN):                                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Browser → http://localhost:8001/api                    │
│  ❌ "Failed to fetch"                                  │
│  (Connection refused, wrong port)                      │
│                                                         │
│ Files → /app/media (ephemeral)                         │
│  ❌ Lost on restart                                    │
│                                                         │
│ CORS → localhost:3001 only                             │
│  ❌ Blocked from http://frontend:3000                 │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ AFTER FIXES (WORKING):                                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Browser → http://backend:8000/api (service name)       │
│  ✅ Request reaches backend                            │
│  ✅ Response includes CORS header                      │
│  ✅ Data available in JavaScript                       │
│                                                         │
│ Files → /app/media (mounted volume)                    │
│  ✅ Persisted on disk                                  │
│  ✅ Available after restart                            │
│                                                         │
│ CORS → frontend:3000 allowed                           │
│  ✅ Request accepted                                   │
│  ✅ CORS headers validated                             │
│  ✅ Response processed                                 │
│                                                         │
│ DB Connection → service names                          │
│  ✅ db:5432 resolves via Docker DNS                   │
│  ✅ Connection succeeds                                │
│  ✅ Data extracted                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 ENVIRONMENT-SPECIFIC DIFFERENCES

### Local vs Docker Configuration

```
┌────────────────────────────┬────────────────────────────┐
│ LOCAL DEVELOPMENT          │ DOCKER DEPLOYMENT          │
├────────────────────────────┼────────────────────────────┤
│                            │                            │
│ Frontend                   │ Frontend                   │
│ - URL: localhost:3000      │ - URL: localhost:3001      │
│ - Internal: Not applicable │ - Internal: frontend:3000  │
│                            │                            │
│ Backend                    │ Backend                    │
│ - URL: localhost:8000      │ - URL: localhost:8001 host │
│ - Internal: Not applicable │ - Internal: backend:8000   │
│                            │                            │
│ API from Frontend          │ API from Frontend          │
│ - http://localhost:8001    │ - http://backend:8000      │
│ - (external + internal)    │ - (internal only)          │
│ - NEXT_PUBLIC_API_URL:     │ - NEXT_PUBLIC_API_URL:     │
│   localhost:8001           │   backend:8000             │
│                            │                            │
│ Database Host              │ Database Host              │
│ - localhost (form default) │ - db (form default)        │
│ - Port: 5433 (host mapping)│ - Port: 5432 (internal)    │
│                            │                            │
│ CORS_ALLOWED_ORIGINS       │ CORS_ALLOWED_ORIGINS       │
│ - localhost:3000           │ - frontend:3000            │
│ - localhost:3001           │ - backend:8000             │
│ - 127.0.0.1:*              │ - localhost:3001 (host)    │
│                            │                            │
│ Media Files                │ Media Files                │
│ - ./backend/media/         │ - backend-media volume     │
│ - On host filesystem       │ - Docker named volume      │
│ - Persists automatically   │ - Persists across restarts │
│                            │                            │
│ DOCKER_ENV                 │ DOCKER_ENV                 │
│ - Not set (undefined)      │ - Set to "1"               │
│ - Code uses localhost      │ - Code uses service names  │
│                            │                            │
└────────────────────────────┴────────────────────────────┘
```

---

## ✨ VISUAL SUMMARY

```
THE PROBLEM IN ONE PICTURE:

┌─────────────────────────────────────────────────────┐
│ LocalHost Confusion in Docker                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Frontend Container                                 │
│  ┌─────────────────────────────────────────────┐   │
│  │ fetch('http://localhost:8001')              │   │
│  │         │                                   │   │
│  │         └─ Inside container:                │   │
│  │            localhost = 127.0.0.1 = SELF     │   │
│  │                                             │   │
│  │  ❌ Container doesn't have port 8001        │   │
│  │  ❌ Connection refused                      │   │
│  │                                             │   │
│  │  ✅ Should be:                              │   │
│  │  fetch('http://backend:8000')               │   │
│  │          └─ Service name resolves via DNS   │   │
│  │             to backend container            │   │
│  │                                             │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘


THE SOLUTION IN ONE PICTURE:

┌──────────────────────────────────────────────────────┐
│ Environment-Aware Configuration                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  DOCKER_ENV=1 ──┬─→ Backend: Use service names      │
│                 │              - CORS: frontend:3000│
│                 │              - DB host: db:5432   │
│                 │                                   │
│                 └─→ Frontend: Use service names     │
│                                - API_URL: backend:8000
│                                - Form defaults: db
│                                                      │
│  DOCKER_ENV unset ─→ Local Dev: Use localhost       │
│                     - CORS: localhost:3001          │
│                     - DB host: localhost            │
│                     - API_URL: localhost:8001       │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 📚 See Also

- **PORTS_DEBUGGING_REPORT.md** - Detailed technical analysis
- **IMPLEMENTATION_GUIDE.md** - Code fix instructions
- **QUICK_REFERENCE.md** - Quick lookup guide

