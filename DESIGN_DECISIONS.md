# ✅ Design Decisions & Architecture Rationale

**Status:** 🟢 **DOCUMENTED** | April 14, 2026

This document explains the key architectural decisions made during development, the alternatives considered, and why specific approaches were chosen.

---

## 🏛️ Architecture Overview: Why Monorepo with Separate Frontend & Backend?

### Decision: Monorepo Structure (Next.js Frontend + Django Backend)

**What We Chose:**
```
data-connector-platform/
├── app/                    # Next.js Frontend (React)
├── backend/                # Django REST Backend
├── docker-compose.yml      # Orchestration
└── docs/                   # Documentation
```

**Why This Approach?**

| Aspect | Monorepo | Separate Repos |
|--------|----------|----------------|
| **Development Speed** | ✅ Single clone, single setup | ❌ Complex multi-repo setup |
| **Consistency** | ✅ Shared version control | ❌ Version mismatch risks |
| **Deployment** | ✅ Single docker-compose up | ❌ Multiple deployments |
| **Communication** | ✅ Easier API/UI alignment | ❌ Coordination overhead |
| **Learning** | ✅ Full-stack in one place | ❌ Knowledge scattered |

**Alternative Considered:** Microservices with separate deployment pipelines
- **Why Not:** Adds complexity, operational overhead, and slower development cycle for a single-application assessment
- **When to Use:** At scale with 10+ independent services

---

## 🔐 Authentication: Session-Based with CSRF Tokens

### Decision: Django Session Authentication (Not JWT)

**What We Chose:**
```python
# Settings.py
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF Protection
    'django.contrib.sessions.middleware.SessionMiddleware',  # Sessions
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Auth
]
```

**Why Session-Based?**

| Feature | Sessions | JWT |
|---------|----------|-----|
| **Server-Side Validation** | ✅ Can revoke instantly | ❌ Can't revoke until expiry |
| **CSRF Protection** | ✅ Built-in middleware | ⚠️ Requires custom handling |
| **Development Speed** | ✅ Django provides defaults | ❌ Manual implementation |
| **Scalability** | ⚠️ Requires sticky sessions | ✅ Stateless |
| **Assessment Context** | ✅ Proper security demo | ❌ Overkill for single server |

**Implementation Details:**
```python
# auth.py - Session validation
def login(request):
    if authenticate(username, password):
        auth_login(request, user)  # Creates session cookie
        request.session['user_id'] = user.id
        return response  # Sets HttpOnly cookie
```

**Why HttpOnly Cookies?**
- ✅ XSS-safe (JavaScript can't access)
- ✅ Browser-managed security
- ✅ CSRF tokens protect state-changing operations
- ✅ Industry standard (OWASP recommended)

**When JWT is Better:**
- Multi-domain/multi-app scenarios
- Mobile apps without cookie support
- Microservices needing stateless auth
- Real-time applications (WebSockets)

---

## 🗄️ Database: SQLite for Development, Extensible Design

### Decision: SQLite for Demo + Pluggable Architecture

**What We Chose:**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',  # Single-file database
    }
}
```

**Why SQLite for Demo?**

| Aspect | SQLite | PostgreSQL |
|--------|--------|-----------|
| **Setup** | ✅ Zero config (file-based) | ❌ Separate service needed |
| **Development** | ✅ Batteries included | ⚠️ Extra complexity |
| **Portability** | ✅ Single file to share | ❌ Database dump needed |
| **Performance** | ✅ Fast enough for demo | ⚠️ Overkill for 1 user |
| **Concurrency** | ⚠️ Limited (demo only) | ✅ Handles 1000+ connections |

**Extensibility to Production:**
```python
# Easy switch to PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'production_db',
        'USER': 'prod_user',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '5432',
    }
}
```

**Design Principle:** The application doesn't know or care about the underlying database. Django ORM abstracts it away.

---

## 🔌 Multi-Database Connectors: Strategy Pattern

### Decision: Abstract Base Class + Concrete Implementations

**What We Chose:**
```python
# connectors.py
class BaseConnector(ABC):
    """Abstract interface for all database connectors"""
    
    @abstractmethod
    def connect(self):
        """Establish connection"""
        pass
    
    @abstractmethod
    def fetch_batch(self, table_name, skip, limit):
        """Fetch batch of records"""
        pass
    
    @abstractmethod
    def close(self):
        """Close connection"""
        pass

class PostgresConnector(BaseConnector):
    def connect(self):
        self.conn = psycopg2.connect(...)
    # ... implementations

class MySQLConnector(BaseConnector):
    def connect(self):
        self.conn = mysql.connector.connect(...)
    # ... implementations

# Factory Pattern
def get_connector(db_type: str) -> BaseConnector:
    connectors = {
        'postgresql': PostgresConnector,
        'mysql': MySQLConnector,
        'mongodb': MongoConnector,
        'clickhouse': ClickHouseConnector,
    }
    return connectors[db_type]()
```

**Why Strategy Pattern + Factory?**

| Aspect | Chosen Approach | Hard-Coded IF/ELSE |
|--------|-----------------|-------------------|
| **Extensibility** | ✅ Add new type: 1 class + 1 line | ❌ Modify core logic |
| **Testing** | ✅ Mock each connector independently | ❌ Can't isolate DB logic |
| **Maintenance** | ✅ Changes isolated to connector | ❌ Changes affect everything |
| **Open/Closed Principle** | ✅ Open for extension, closed for modification | ❌ Violates principle |

**Alternative Considered:** Single unified connector with if/elif for each DB type
- **Why Not:** Violates SOLID principles, becomes unmaintainable at scale
- **Problem with Old Approach:**
  ```python
  # ❌ BAD - Violates Open/Closed Principle
  def fetch_data(db_type):
      if db_type == 'postgresql':
          conn = psycopg2.connect(...)
      elif db_type == 'mysql':
          conn = mysql.connector.connect(...)
      elif db_type == 'mongodb':
          conn = MongoClient(...)
      # ... 50 more lines of if/elif
  ```

**When This Pattern Shines:**
- Supporting multiple implementations of same interface
- Easy testing via mocks
- Future database additions require no core changes
- Code is self-documenting

---

## 📊 Frontend: Next.js with React Hooks (Not Redux/Zustand)

### Decision: React Hooks + Context API (Not Global State Manager)

**What We Chose:**
```typescript
// app/components/FileViewer.tsx
const [files, setFiles] = useState<StoredFile[]>([]);
const [filterFromDate, setFilterFromDate] = useState('');
const [sortOrder, setSortOrder] = useState('desc');

// Fetch and filter locally
const filteredFiles = files.filter(f => 
  f.extracted_at >= filterFromDate && ...
);
```

**Why Not Redux/Zustand?**

| Aspect | Hooks | Redux | Zustand |
|--------|-------|-------|---------|
| **Setup Time** | ✅ Zero config | ❌ 30+ min setup | ⚠️ 10 min setup |
| **Bundle Size** | ✅ ~0KB added | ❌ +40KB | ⚠️ +2KB |
| **Boilerplate** | ✅ Minimal | ❌ Actions/Reducers/Selectors | ⚠️ Some boilerplate |
| **Assessment Scope** | ✅ Perfect fit | ❌ Overkill | ⚠️ Overkill |
| **Learning Curve** | ✅ React basics | ❌ Steep | ⚠️ Medium |

**When to Add State Manager:**
```
Application Size:  < 5 pages      ->  Hooks (Current)
                   5-15 pages     ->  Context API
                   15+ pages      ->  Zustand
                   50+ pages      ->  Redux
Performance Need:  < 100ms re-render -> Hooks OK
                   Need < 16ms        -> Zustand/Redux
```

**Design Principle:** Start simple, upgrade complexity only when needed.

---

## 📝 Data Grid: TanStack React Table (Not AG Grid or Handsontable)

### Decision: TanStack React Table (Headless, Unstyled)

**What We Chose:**
```typescript
import { createColumnHelper, flexRender } from '@tanstack/react-table';

const columnHelper = createColumnHelper<FileData>();
const columns = [
  columnHelper.accessor('id', {
    header: 'ID',
    cell: info => <input value={info.getValue()} />
  }),
];
```

**Why TanStack (Headless)?**

| Aspect | TanStack | AG Grid | Handsontable |
|--------|----------|---------|-------------|
| **Bundle Size** | ✅ ~14KB | ❌ ~1MB | ❌ ~400KB |
| **Price** | ✅ Free MIT | ⚠️ $$ for enterprise | ⚠️ $$$$ |
| **Customization** | ✅ Complete | ⚠️ Limited | ⚠️ Limited |
| **Learning** | ✅ React pattern | ❌ New paradigm | ❌ New paradigm |
| **Features for CRUD** | ✅ Sufficient | ✅ Overkill | ✅ Overkill |

**Architecture Decision:**
```typescript
// ✅ Headless approach = complete UI control
const table = useReactTable({
  data: gridData,
  columns: columns,
  getCoreRowModel: getCoreRowModel(),
  // Provides sorting, pagination, filtering logic
  // We build UI however we want
})

// Render with our Tailwind classes
<table className="border-collapse border">
  {/* Custom styling, not locked into component theme */}
</table>
```

**Alternative:** Use pre-styled component like AG Grid
- **Why Not:** Bundle bloat, licensing complexity, limited customization
- **Cost-Benefit:** TanStack adds ~50 lines of code but saves 950KB

---

## 🔐 Password Encryption at Rest

### Decision: AES-256 Encryption in Database

**What We Chose:**
```python
# crypto.py
from cryptography.fernet import Fernet

class PasswordManager:
    @staticmethod
    def encrypt(password: str) -> str:
        cipher = Fernet(settings.ENCRYPTION_KEY)
        return cipher.encrypt(password.encode()).decode()
    
    @staticmethod
    def decrypt(encrypted: str) -> str:
        cipher = Fernet(settings.ENCRYPTION_KEY)
        return cipher.decrypt(encrypted.encode()).decode()

# models.py
class DatabaseConnection(models.Model):
    password = models.TextField()  # Encrypted
    
    @property
    def decrypted_password(self):
        return PasswordManager.decrypt(self.password)
```

**Why Store Encrypted Passwords?**

| Scenario | Plain Text | Hashed (bcrypt) | Encrypted (Fernet) |
|----------|-----------|-----------------|-------------------|
| **Need to retrieve?** | ✅ Yes | ❌ Can't retrieve | ✅ Yes |
| **Reverse-engineering** | ❌ Trivial | ✅ Impossible | ✅ Computationally hard |
| **Database compromise** | ❌ Exposed | ✅ Safe | ⚠️ At-risk (if key stolen) |
| **DB credentials use case** | N/A | N/A | ✅ Perfect fit |

**Security Measures Taken:**
1. ✅ Key stored in environment variable (not in code)
2. ✅ Never logged or printed
3. ✅ Only decrypted when needed for connection
4. ✅ HTTPS for all API communication
5. ✅ Database access logs for audit

**Not Hashing Passwords?** 
- Hashing is one-way (can't retrieve to use as credential)
- We NEED the original password to connect to external DBs
- Encryption allows retrieval while keeping encrypted at rest

---

## 📂 File Storage: Database + File System

### Decision: Dual Storage (DB Metadata + File System)

**What We Chose:**
```python
# models.py
class StoredFile(models.Model):
    user = models.ForeignKey(User)
    filepath = models.FileField(upload_to='extractions/')
    extracted_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    base_filename = models.CharField()
    table_name = models.CharField()
    connection_name = models.CharField()

# File system
/media/
  extraction_postgresql_users_admin_20260414_120000.json
  extraction_mysql_orders_john_20260414_121530.json
```

**Why Both DB and Files?**

| Aspect | DB Only | File Only | Both (Chosen) |
|--------|---------|-----------|--------------|
| **Search/Filter** | ✅ SQL queries | ❌ Read all files | ✅ SQL queries |
| **Large Files** | ❌ Bloats DB | ✅ Efficient | ✅ Reference only |
| **Audit Trail** | ✅ Queries logged | ⚠️ Manual tracking | ✅ Full audit |
| **Performance** | ⚠️ Slower for large data | ✅ Fast retrieval | ✅ Best of both |
| **Backup** | ✅ Single database | ⚠️ Separate files | ✅ Standard approach |

**Query Example - Why This Matters:**
```python
# ✅ This is instant (using DB index on extracted_at)
files = StoredFile.objects.filter(
    extracted_at__gte=from_date,
    extracted_at__lte=to_date,
    table_name='users'
).order_by('-extracted_at')

# ❌ File-only approach: Read 1000 files, parse JSON, filter in memory
```

---

## 🎨 UI Components: Tailwind CSS (Not Styled Components or Bootstrap)

### Decision: Tailwind CSS for Styling

**What We Chose:**
```tsx
// Components with Tailwind utilities
<button className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700">
  Submit
</button>
```

**Why Tailwind?**

| Aspect | Tailwind | Styled-Components | Bootstrap |
|--------|----------|------------------|-----------|
| **Bundle Size** | ✅ ~14KB (PurgeCSS) | ⚠️ +15KB | ⚠️ +50KB |
| **Design System** | ✅ Consistent spacing | ⚠️ Custom theme | ⚠️ Opinionated |
| **Customization** | ✅ Easy config | ✅ Full control | ❌ Hard to override |
| **Learning** | ✅ CSS knowledge | ⚠️ Styled component paradigm | ⚠️ Class naming |
| **Component Reuse** | ⚠️ Classes repeated | ✅ Component abstraction | ⚠️ HTML structure |

**How We Mitigated CSS Bloat:**
```js
// next.config.ts with PurgeCSS
content: [
  './app/**/*.{js,ts,jsx,tsx}',
  './components/**/*.{js,ts,jsx,tsx}',
],
// Only includes used classes in production build
```

---

## 🚀 Deployment: Docker Compose (Not Kubernetes)

### Decision: Docker Compose for Single-Machine Deployment

**What We Chose:**
```yaml
# docker-compose.yml
services:
  frontend:
    build: .
    ports: ["3000:3000"]
  backend:
    build: ./backend
    ports: ["8001:8001"]
  db:
    image: postgres:15
    ports: ["5432:5432"]
```

**Why Docker Compose?**

| Aspect | Compose | Kubernetes | Bare Metal |
|--------|---------|-----------|-----------|
| **Setup Time** | ✅ 5 minutes | ❌ 2+ hours | ⚠️ 1 hour |
| **Learning Curve** | ✅ Simple YAML | ❌ Steep (Go knowledge) | ⚠️ Manual config |
| **Scaling** | ⚠️ Single machine | ✅ 1000+ nodes | ❌ Manual management |
| **Assessment Demo** | ✅ Perfect fit | ❌ Overkill | ⚠️ Messy setup |
| **Production** | ⚠️ Add reverse proxy | ✅ Built-in | ❌ Complex |

**Upgrade Path to Kubernetes:**
```yaml
# Docker Compose (current)
docker-compose up

# Auto-convertible to Kubernetes
kompose convert  # Generates K8s manifests
```

**Design Principle:** Start simple, upgrade when you have the problem to solve.

---

## 🧪 Testing Strategy: Unit Tests (Not E2E)

### Decision: Comprehensive Unit Tests + Some Integration Tests

**What We Chose:**
```
Test Coverage:
├── Unit Tests (80%)
│   ├── Model tests
│   ├── Serializer tests
│   ├── View tests
│   └── Connector tests
├── Integration Tests (15%)
│   ├── Full API workflow
│   └── Database migration tests
└── Manual E2E (5%)
    └── User actions via UI
```

**Why Unit-Focused?**

| Type | Unit | Integration | E2E |
|------|------|-------------|-----|
| **Speed** | ✅ ms | ⚠️ seconds | ❌ minutes |
| **Flakiness** | ✅ Stable | ⚠️ Can fail | ❌ Often fails |
| **Coverage** | ✅ 100% possible | ⚠️ 60-70% | ⚠️ 30-40% |
| **Debugging** | ✅ Fast | ⚠️ Longer | ❌ Very slow |
| **Maintenance** | ✅ Easy | ⚠️ Moderate | ❌ Brittle |
| **Cost** | ✅ Free | ⚠️ Cloud resources | ❌ Expensive |

**Test Pyramid Philosophy:**
```
        /\
       /E2E\         (Manual UI clicks - 5%)
      /------\
     /Integration\ (DB + API interaction - 15%)
    /----------\
   /   Units    \   (Mocking, isolated - 80%)
  /-------------\
```

---

## 🔄 API Design: REST (Not GraphQL)

### Decision: RESTful API with Standard Endpoints

**What We Chose:**
```
GET    /api/connections/              # List all
POST   /api/connections/              # Create
GET    /api/connections/<id>/         # Retrieve
PUT    /api/connections/<id>/         # Update
DELETE /api/connections/<id>/         # Delete
POST   /api/connections/<id>/extract/ # Custom action
```

**Why REST (Not GraphQL)?**

| Aspect | REST | GraphQL |
|--------|------|---------|
| **Simplicity** | ✅ Standard patterns | ❌ Query language |
| **Caching** | ✅ HTTP caching built-in | ⚠️ Complex setup |
| **Learning** | ✅ Everyone knows | ❌ New paradigm |
| **Overfetching** | ⚠️ Possible | ✅ Solved |
| **Setup Time** | ✅ Minutes | ❌ Hours |
| **For Assessment** | ✅ Perfect fit | ❌ Overkill |

**When GraphQL is Better:**
- Mobile apps needing bandwidth optimization
- Complex querying from multiple sources
- Rapidly changing API requirements
- 10+ different client types

---

## 📋 Summary Table: Key Decisions

| Component | Choice | Why | Alternative |
|-----------|--------|-----|-------------|
| **Structure** | Monorepo | Single setup | Multi-repo |
| **Auth** | Sessions + CSRF | Instant revocation | JWT |
| **DB (Demo)** | SQLite | Zero config | PostgreSQL |
| **DB (Prod)** | Extensible via ORM | Easy swap | Hard-coded |
| **Connectors** | Strategy Pattern | Easy to extend | If/elif |
| **Frontend State** | Hooks | Minimal overhead | Redux |
| **Data Grid** | TanStack | Complete control | AG Grid |
| **Pw Storage** | Encrypted | Need retrieval | Hashed |
| **Files** | DB + Files | Best of both | DB only |
| **Styling** | Tailwind | Small bundle | Bootstrap |
| **Deployment** | Compose | Simple setup | Kubernetes |
| **Testing** | Unit-focused | Fast feedback | E2E-focused |
| **API** | REST | Standard patterns | GraphQL |

---

## 🎯 Design Principles Applied

### 1. **SOLID Principles**
- Single Responsibility: Each connector handles one DB type
- Open/Closed: New features via extension, not modification
- Liskov Substitution: All connectors implement BaseConnector interface
- Interface Segregation: Small, focused interfaces
- Dependency Inversion: Depend on abstractions, not concrete classes

### 2. **DRY (Don't Repeat Yourself)**
- Shared authentication middleware
- Common API response format
- Reusable React components
- Database query utilities

### 3. **KISS (Keep It Simple, Stupid)**
- Monorepo over microservices
- Hooks over Redux
- REST over GraphQL
- SQLite over complex setup

### 4. **Scalability**
- Database abstraction layer
- Connector factory pattern
- File storage separation
- Component composition

### 5. **Security**
- Password encryption at rest
- CSRF token validation
- HttpOnly session cookies
- Environment variable secrets
- SQL injection prevention via ORM

---

## 🔍 When to Reconsider These Decisions

| Decision | Reconsider When |
|----------|-----------------|
| **Monorepo** | > 5 teams or separate deployment cycles |
| **Sessions** | Multiple domains or mobile-first apps |
| **SQLite** | > 100 concurrent users |
| **AWS Simple** | Need multi-region or advanced features |
| **Hooks** | App grows to 50+ components with shared state |
| **REST** | Need bandwidth optimization or complex querying |
| **TanStack** | Need enterprise features (Excel export, etc.) |
| **Docker Compose** | Need orchestration across machines |
| **Tailwind** | Design system changes frequently |

---

This decision log helps understand not just **what** was built, but **why** - making it easier to maintain, extend, and justify architectural choices.
