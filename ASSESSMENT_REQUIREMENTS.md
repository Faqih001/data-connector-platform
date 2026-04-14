# Full-Stack Developer Assessment - Project Requirements

**Submission Deadline:** Tuesday, 14 April 2026, 5:00 PM  
**Submit To:** recruitment@actserv-africa.com  
**Subject:** Completed Technical Assessment

---

## 📋 Project Overview

### Objective
Build a data connector web application that:
- Connects to multiple databases
- Extracts and edits data in batches
- Sends processed data to a backend
- Stores results securely (Database + File)
- Uses containerized infrastructure

### Use Case
A full-stack solution enabling users to:
1. Connect to external data sources
2. Extract data in configurable batches
3. Edit data interactively in a grid
4. Submit processed data back to the backend
5. Retrieve stored results for auditing

---

## 🎯 Core Requirements

### 1. Multi-Database Connector System
Build a system that allows connections to multiple database types:

**Supported Databases:**
- PostgreSQL
- MySQL
- MongoDB
- ClickHouse

**Requirements:**
- Connection configuration model (store credentials securely)
- Connector abstraction layer (extensible for new DB types)
- Connection testing/validation before use
- Support for custom connection parameters

### 2. Batch Data Extraction
- Pull data from any configured source
- Batch size must be configurable (e.g., 100, 500, 1000 rows)
- Handle large datasets efficiently
- Support pagination/partial extraction
- Proper error handling for extraction failures

### 3. Interactive Data Grid
- Display extracted data in an editable grid
- Features required:
  - Inline editing of cell values
  - Row update tracking
  - Basic data validation
  - Column visibility/sorting
  - Batch operations (select multiple rows)

### 4. Data Submission & Processing
- Modified data must be submitted back to backend
- Backend responsibilities:
  - Validate incoming data
  - Process and structure records
  - Handle submission errors gracefully
  - Return confirmation/errors to frontend

### 5. Dual Storage System
When data is submitted, store in **TWO locations**:

**A. Database Storage**
- Save structured records in application database
- Track submission metadata (who, when, what)
- Enable querying and filtering of submitted data

**B. File Storage**
- Save as JSON or CSV format
- File must include:
  - Timestamp of submission
  - Source database metadata
  - Source connection details
  - User who submitted
  - Original and modified values (audit trail)

### 6. Permission & Access Control

**Role-Based Access (RBAC):**

| Role | File Access |
|------|------------|
| **Admin** | Full access to all files and connections |
| **User** | Can only access own files + files explicitly shared with them |

**Features:**
- User authentication system
- Role assignment mechanism
- File sharing/permission management
- Audit logging of access

---

## 🛠️ Technology Stack Requirements

**MANDATORY:**

| Layer | Technology | Requirement |
|-------|-----------|------------|
| **Frontend** | Next.js | Latest stable version |
| **Backend** | Django REST Framework (DRF) | RESTful API design |
| **Containerization** | Docker + Docker Compose | Production-ready setup |
| **Database (App)** | PostgreSQL / SQLite | Store submissions + files |
| **Database (Source)** | PostgreSQL, MySQL, MongoDB, ClickHouse | Connectors must support all |

---

## 📦 Deliverables

### 1. GitHub Repository
- Code repository with complete source code
- Proper .gitignore (exclude credentials, .venv, node_modules, etc.)
- Clear commit history with meaningful messages
- README with setup instructions

### 2. Application Demo Recording
- Screen recording of working application on local development device
- Must demonstrate:
  - ✓ Creating database connections (all 4 types)
  - ✓ Extracting data with configurable batch sizes
  - ✓ Editing data in the grid
  - ✓ Submitting data and seeing storage (DB + file)
  - ✓ Accessing files with proper permissions
  - ✓ Docker container startup

### 3. Design Documentation
- Document design decisions explaining:
  - Why certain approaches were chosen
  - Architecture patterns used
  - Trade-offs considered
  - How extensibility is achieved
  - How RBAC is implemented
  - File organization rationale

### 4. Unit Tests
- Test coverage for critical components:
  - Database connector logic
  - Data extraction functions
  - Data validation
  - Permission/access control
  - API endpoints
- Minimum 70% code coverage recommended
- Include test execution instructions

---

## ✅ Evaluation Criteria

Your submission will be evaluated on:

1. **Functionality** (30%)
   - All features working as specified
   - No crashes or HTTP errors
   - Proper error handling

2. **Code Quality** (25%)
   - Clean, readable code
   - Proper separation of concerns
   - Design patterns applied
   - Consistency across codebase

3. **Documentation** (20%)
   - Design decisions clearly explained
   - Setup instructions clear
   - Code comments where needed
   - Architecture diagrams helpful

4. **Testing** (15%)
   - Unit tests present and meaningful
   - Test coverage adequate
   - Edge cases handled

5. **UI/UX** (10%)
   - Intuitive user interface
   - Responsive design
   - Clear feedback messages
   - Professional appearance

---

## 📋 Submission Checklist

Before submitting, verify:

- [ ] GitHub repository created and accessible
- [ ] All source code committed (no secrets exposed)
- [ ] README.md has setup and run instructions
- [ ] Application demo recording uploaded (MP4/WebM)
- [ ] Design documentation file included
- [ ] Unit tests written and passing
- [ ] Docker Compose file working (`docker-compose up`)
- [ ] All 4 database connectors functional
- [ ] RBAC system implemented and tested
- [ ] File storage (JSON/CSV) working
- [ ] Database storage working
- [ ] Error handling implemented
- [ ] No console errors or warnings

---

## 🤝 Questions & Support

For clarifications, contact recruitment team:
- **Email:** recruitment@actserv-africa.com
- **Subject:** [Assessment Question] Your question here

---

## 📝 Assessment Details Reference

| Item | Details |
|------|---------|
| Assessment Type | Full-Stack Development |
| Position | Full Stack Developer |
| Submission Email | recruitment@actserv-africa.com |
| Deadline | 14 April 2026, 5:00 PM |
| Expected Duration | 2-3 weeks typical |
| Resources | Use any documentation, libraries, frameworks you prefer |

---

**Good luck with your assessment! 🚀**
