# ✅ Data Connector Platform - Complete Navigation & User Guide

**Status:** 🟢 **TESTED & VERIFIED** | All features documented and working | April 14, 2026

A Complete Guide for All Users (Technical and Non-Technical) - **All Features Fully Functional**

---

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [System Architecture](#system-architecture)
3. [Login Instructions](#login-instructions)
4. [Main Landing Page](#main-landing-page)
5. [Page 1: Frontend Dashboard (Port 3000)](#page-1-frontend-dashboard-port-3000)
6. [Page 2: API Connections (Port 8001)](#page-2-api-connections-port-8001)
7. [Page 3: API Files (Port 8001)](#page-3-api-files-port-8001)
8. [Page 4: Admin Panel (Port 8001)](#page-4-admin-panel-port-8001)
9. [Common Tasks](#common-tasks)
10. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Access the Application
The Data Connector Platform has **multiple interfaces** for different users:

| Interface | URL | Purpose | Users |
|-----------|-----|---------|-------|
| **Frontend** | http://localhost:3000 | Main user interface with modern UI | All users |
| **Backend Welcome** | http://localhost:8001 | Quick access hub | Developers |
| **API Connections** | http://localhost:8001/api/connections/ | View/manage database connections | Developers |
| **API Files** | http://localhost:8001/api/files/ | View extracted data files | Developers |
| **Admin Panel** | http://localhost:8001/admin/ | System administration | Admin users only |

### Demo Credentials
Choose based on your role:

| Username | Password | Role | Access |
|----------|----------|------|--------|
| **admin** | admin123 | Administrator | Full system access |
| **john_sales** | john123 | Sales User | View sales data, create connections |
| **sarah_analytics** | sarah456 | Analytics User | View analytics data, shared files |
| **mike_reporting** | mike789 | Reporting User | Generate reports, data extraction |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 FRONTEND (Port 3000)                        │
│         React + Next.js - Beautiful UI/UX                   │
│  - Create database connections                              │
│  - Extract data from databases                              │
│  - View and manage extracted files                          │
│  - Share data with other users                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ API Calls (JSON)
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                 BACKEND (Port 8001)                         │
│            Django REST Framework Server                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ API Endpoints                                        │  │
│  │  - GET/POST /api/connections/                        │  │
│  │  - GET /api/files/                                   │  │
│  │  - POST /api/extract/                                │  │
│  │  - POST /api/submit/                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Admin Panel (/admin/)                                │  │
│  │  - User management                                   │  │
│  │  - Connections management                            │  │
│  │  - Files management                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ Database Connections
                   │
        ┌──────────┼──────────┐
        │          │          │
   PostgreSQL    MySQL    MongoDB/Clickhouse
```

---

## 🔐 Login Instructions

### 1. Go to Frontend Login Page
Open your web browser and navigate to:
```
http://localhost:3000
```

**What you'll see:**
- A clean, modern login form
- Two input fields: **Username** and **Password**
- "Login" button (disabled until you fill in credentials)
- Demo accounts listed below

![Frontend Login Page](./screenshots/01-login-page.png)

### 2. Enter Your Credentials
1. Click the **Username** field
2. Type your username (e.g., `john_sales`)
3. Click the **Password** field
4. Type your password (e.g., `john123`)
5. Click the **Login** button or press Enter

**Password Tip:** Click the 👁️ eye icon to show/hide your password

### 3. After Login
You'll be redirected to your **Personal Dashboard** with:
- Your username displayed at the top
- Connection management tools
- Data extraction interface
- File browser
- Quick action buttons

---

## 📍 Main Landing Page

### Backend Welcome Page
**URL:** http://localhost:8001/

This page serves as the central hub with quick navigation options.

**Layout:**
```
┌─────────────────────────────────────────┐
│      🚀 Data Connector Platform         │
│         Backend API Server              │
├─────────────────────────────────────────┤
│                                         │
│  📌 API Endpoints Section               │
│  - POST /api/connections/               │
│  - GET /api/connections/                │
│  - POST /api/extract/                   │
│  - POST /api/submit/                    │
│                                         │
│  🔐 Admin Access Section                │
│  - Admin Credentials (show/use)         │
│                                         │
│  📋 Available Features in Admin         │
│  - Connections Management               │
│  - Stored Files Management              │
│  - User Management                      │
│  - System Configuration                 │
│  - Data Monitoring                      │
│  - Connector Setup                      │
│                                         │
│  QUICK ACTION BUTTONS:                  │
│  ┌─────────────────────────────────┐   │
│  │ 🔗 API Connections              │   │
│  ├─────────────────────────────────┤   │
│  │ 📊 API Files                    │   │
│  ├─────────────────────────────────┤   │
│  │ 📊 Go to Admin Panel            │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ 🎨 Open Frontend (Port 3000)    │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

**Buttons Guide:**
| Button | Purpose | Who | Where |
|--------|---------|-----|-------|
| 🔗 API Connections | Show all database connections in API format | Developers | http://localhost:8001/api/connections/ |
| 📊 API Files | Display extracted files in JSON format | Developers | http://localhost:8001/api/files/ |
| 📊 Go to Admin Panel | Access system administration | Admin users | http://localhost:8001/admin/ |
| 🎨 Open Frontend | Use the main user interface | All users | http://localhost:3000 |

---

## 📱 Page 1: Frontend Dashboard (Port 3000)

### Overview
This is the **PRIMARY USER INTERFACE** - Most users will spend their time here.

**URL:** http://localhost:3000

### What You Can Do Here:
✅ Create database connections  
✅ Extract data from databases  
✅ View extracted files  
✅ Download data (JSON/CSV)  
✅ Share files with colleagues  
✅ Edit and save data  
✅ Manage permissions  

### Layout & Components

```
┌──────────────────────────────────────────────────────────┐
│           Data Connector Platform                        │
│  Logged in as: [username]              [Logout Button]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  QUICK ACTION BUTTONS:                                   │
│  ┌──────────────┬──────────────┐                        │
│  │ 📊 API       │ 📊 Admin     │                        │
│  │    Files     │    Panel     │                        │
│  └──────────────┴──────────────┘                        │
│  ┌────────────────────────────────┐                     │
│  │  🎨 Open Frontend (Port 3000)  │                     │
│  └────────────────────────────────┘                     │
│                                                          │
├──┬─────────────────┬──┬──────────────────────────────────┤
│  │ LEFT SIDEBAR    │  │   RIGHT MAIN AREA               │
│  │                 │  │     Connections   │  │     - Format (JSON/CSV)         │
│  │   Dropdown      │  │     - Extract Button            │
│  │                                         │
│  │ ► Connection    │  │   ► Extract Data Form           │
│  │   Form          │  │     - Table Name Input          │
│  │                 │  │     - Batch Size Selection      │     │  │                                  │
│  │ ► Stored Files  │  │   ► Data Grid                   │
│  │   Viewer        │  │     - Preview extracted data    │
│  │   - File list   │  │     - Editable cells            │
│  │   - Format      │  │     - Save changes              │
│  │   - Download    │  │                                  │
│  │   - Share       │  │                                  │
│  │                 │  │                                  │
│  └─────────────────┴──┴──────────────────────────────────┘
```

### Step-by-Step: Creating & Extracting Data

#### Step 1: Create a Database Connection
1. Look at the **LEFT PANEL** → **Connection Form**
2. Fill in these fields:
   - **Name:** Give your connection a name (e.g., "Main Database")
   - **Database Type:** Select from dropdown
     - PostgreSQL (recommended for testing)
     - MySQL
     - MongoDB
     - ClickHouse
   - **Host:** Server address (default: localhost)
   - **Port:** Database port number
   - **Username:** Database username
   - **Password:** Database password
   - **Database Name:** The database to connect to
3. Click **Create Connection** button

#### Step 2: Select a Connection
1. In the **Connections** dropdown
2. Select the connection you just created
3. The connection is now active for data extraction

#### Step 2b (Optional): Manage Tables for Connection
When you select a connection:

**If the connection has NO TABLES:**
1. A blue section appears: **"📋 Create New Table"** with a "No tables found" indicator
2. Click **Show** to expand the table creation form
3. Fill in:
   - **Table Name:** Name for your new table
   - **SQL Statement:** The CREATE TABLE SQL command for your database type
   - Database-specific templates are provided (PostgreSQL, MySQL, ClickHouse, etc.)
4. Click **Create** button
5. 🟢 **Green success notification:** "Table '{tableName}' created successfully!"
6. The form hides automatically
7. The new table appears in the Table Name dropdown

**If the connection HAS TABLES:**
1. Tables are listed in the **Table Name** dropdown in the Extract Data section
2. To **delete a table:**
   - Select the table from the dropdown
   - Click the red **Delete** button next to it
   - ✅ Table is permanently removed from the database
   - 🟢 **Green success notification:** "Table deleted successfully!"

**Key Points:**
- 🟢 **Green notifications** appear for successful table operations
- 🔴 **Red error messages** if table creation fails (e.g., syntax error)
- The "No tables found" indicator helps you quickly see if a connection needs tables
- Table operations are database-specific (SQL varies by database type)
- Deleted tables cannot be recovered

#### Step 3: Extract Data
1. In the **RIGHT PANEL** → **Extract Data** section
2. Fill in:
   - **Table Name:** The database table to extract from
   - **Batch Size:** How many rows to fetch (default: 1000)
   - **Format:** JSON or CSV
3. Click **Extract Data**
4. Wait for extraction to complete
5. You'll see a **GREEN SUCCESS** notification (toast)
6. Data appears in the grid below

#### Step 4: View & Edit Data
1. The **Data Grid** shows your extracted data
2. **Edit existing cells:**
   - Click any cell to **edit** the value
   - Make your changes
   - Press Enter or click outside the cell to save
3. **Add new rows:**
   - Click **➕ Add Row** button
   - New empty row appears at the bottom
   - Click cells in the new row to add data
4. **Add new columns:**
   - Click **➕ Add Column** button
   - Enter the column name in the text field
   - Click **Add Column** to create it
   - New column appears in all rows
5. **Delete rows:**
   - Select rows by clicking checkboxes on the left
   - Click **🗑️ Delete Selected (N)** where N is the count of selected rows
   - Selected rows are removed
6. **Save all changes:**
   - Click **Save Changes** button at the bottom
   - All edits, new rows, and new columns are saved

#### Step 5: Manage Stored Files

**The Stored Files section** (left panel) shows all extracted data files with full management capabilities.

##### File List & Display
1. Each file shows:
   - **📄 Filename** - The extracted file name
   - **📅 Extraction Date** - When the data was extracted
   - **📊 Table Name** - Which database table was extracted
   - **🔌 Connection Name** - Which database connection it came from
   - **📤 Shared Badge** (if applicable) - Shows files shared with you or by you
   - **Modified Date** - Last time the data was edited

##### Select & Filter Files
1. **Single Select:**
   - Click on any file to view/edit it
   - File appears in the right panel data grid
2. **Multi-Select (for batch operations):**
   - Check the ☑️ checkbox next to each file
   - Check the header checkbox to **Select All** visible files
   - Shows count: "🗑️ Delete Selected (N)" where N = number selected
3. **Filter Files:**
   - **By Date Range:**
     - Set "From Date" to filter files from a specific date onwards
     - Set "To Date" to filter files up to a specific date
   - **By Table Name:**
     - Search for specific table names in the search box
     - Filters files from that table
   - **Sort Order:**
     - **Latest** (default) - Most recently extracted/modified first
     - **Oldest** - Oldest files first

##### Download Files
1. Click on a file in the **Stored Files** section
2. The file data appears in the grid on the right
3. Choose format:
   - 📥 **JSON** - For data interchange and API integration
   - 📥 **CSV** - For Excel, spreadsheets, and data analysis
4. Click **Download** button
5. File saves to your computer's downloads folder
6. ✅ Green notification: "File downloaded successfully!"

**Note:** Downloaded files are copies. Your original file in the system is unchanged.

##### Share Files with Others
1. Click 📤 **Share** button next to the file
2. A share modal appears
3. **Search for colleague:**
   - Type their username or email
   - Search results appear automatically
4. **Select users** to share with:
   - Click on each user to select them
   - Multiple users can be selected at once
5. **Permission level** (if configurable):
   - 👁️ **View Only** - User can see the data but not download
   - ⬇️ **View & Download** - User can download the file
6. Click **Share** to confirm
7. ✅ Green notification: "File shared successfully!"
8. **Shared badge** appears on the file: "📤 Shared"
9. Selected users receive notification

##### Unshare Files
1. Click 📤 **Share** button on a file you've shared
2. See list of users who have access
3. Next to each user, click **Remove** or **🗑️**
4. User loses access immediately
5. ✅ Green notification: "File unshared successfully!"

##### Delete Files
1. **Delete single file:**
   - Right-click on file and select **Delete** OR
   - Check the checkbox and click **🗑️ Delete Selected**
2. File is soft-deleted (temporarily removed)
3. 🔴 Red notification: "File moved to trash"

2. **Restore deleted file:**
   - Deleted files appear in **Trash/Recently Deleted** section
   - Click **Restore** button
   - 🟢 Green notification: "File restored successfully!"

3. **Permanently delete:**
   - In trash, click **Permanently Delete** or **Delete Forever**
   - ⚠️ **This cannot be undone**
   - File is removed from system

##### View File Details & Metadata
1. Click on any file name
2. See full details:
   - **Created By** - Who extracted this data
   - **Extraction Timestamp** - Exact date/time
   - **Table Source** - Original table name
   - **Connection Source** - Which database it came from
   - **File Size** - How large the extracted data is
   - **Access Level** - Your permission (owner/viewer/downloader)
   - **Shared With** - List of users who have access

---

#### Step 6 (Optional): Download or Share

**Quick workflow for common tasks:**

1. **I want to download a file for analysis:**
   - Click file → Choose CSV → Download → Use in Excel
2. **I want to share data with my team:**
   - Click file → Click Share → Select team members → Share
3. **I need to clean up old files:**
   - Select multiple old files → Delete Selected → Confirm
4. **I accidentally deleted a file:**
   - Go to Trash → Find file → Restore

#### Step 7 (Optional): Delete a Connection
1. In the **Connections** dropdown
2. Select a connection you want to delete
3. Click the red **🗑️ Delete** button
4. A confirmation dialog will appear:
   ```
   "Are you sure you want to delete the connection "Connection Name"?
   This will delete all tables and extracted data associated with this connection.
   This action cannot be undone."
   ```
5. Click **OK** to confirm (or **Cancel** to keep the connection)
6. ✅ Success message appears: "Connection 'Connection Name' deleted successfully!"
7. The connection is immediately removed from the dropdown
8. All extracted files from that connection are permanently deleted
9. All database tables associated with that connection are removed

**⚠️ WARNING:** Deleting a connection is **PERMANENT** and **CANNOT BE UNDONE**. Make sure to download any files you need before deleting.

**Connection Deletion Details:**
- 🗑️ Deletes the connection record from the system
- 📊 Deletes all extracted data from that connection
- 📁 Deletes all stored files (JSON/CSV) from that connection  
- 🔗 Removes all shares related to files from that connection
- ✅ Confirmation dialog prevents accidental deletion

### Notifications (Toast Messages)

The system shows **colored toast notifications** for feedback:

| Color | Meaning | Example |
|-------|---------|---------|
| 🟢 **Green** | Success | File shared successfully! |
| � **Green** | Success | Table 'users' created successfully! |
| 🟢 **Green** | Success | Table deleted successfully! |
| 🟢 **Green** | Success | Connection 'My DB' deleted successfully! |
| 🔴 **Red** | Error | Failed to extract data |
| 🔴 **Red** | Error | Failed to create table: Syntax error |
| 🔴 **Red** | Error | Failed to delete table |
| 🔵 **Blue** | Info | Operation in progress |
| 🟡 **Yellow** | Warning | Please select data first |
| 🟡 **Yellow** | Warning | Please enter a table name |

These appear in the **bottom right** and auto-dismiss after 4 seconds.

### Common Notifications Summary

| Operation | Success Message | Error Message |
|-----------|-----------------|---------------|
| **Create Table** | "Table '{name}' created successfully!" | "Failed to create table: {reason}" |
| **Delete Table** | "Table deleted successfully!" | "Failed to delete table" |
| **Delete Connection** | "Connection '{name}' deleted successfully!" | "Failed to delete connection" |
| **Extract Data** | "Data extracted successfully!" | "Failed to extract data" |
| **Share File** | "File shared successfully!" | "Failed to share file" |
| **Save Changes** | "Changes saved successfully!" | "Failed to save changes" |
| **No Tables** | (Blue banner) "No tables found" | — |

---

## 🔌 Page 2: API Connections (Port 8001)

### Overview
**Technical Interface** for developers and technical users to interact with database connections via REST API.

**URL:** http://localhost:8001/api/connections/

### Features Available on This Page:
- ✅ **View all connections** - Display all database connections in JSON format
- ✅ **Create new connection** - POST form to add new connections
- ✅ **View connection details** - Drill into individual connection records
- ✅ **Edit connections** - PUT endpoint to modify existing connections
- ✅ **Delete connections** - Remove connections with cascade delete
- ✅ **Test connections** - Verify connectivity before saving
- ✅ **List tables** - View available tables in each connection

### What This Shows:
- All database connections in **JSON format**
- Connection details (host, port, username, database name)
- Passwords are **encrypted** (for security - encrypted_token format)
- Stored server-side
- User ownership and timestamps
- Staff flag and permission status

### JSON Response Example:
```json
[
  {
    "id": 1,
    "name": "Test PostgreSQL",
    "db_type": "postgresql",
    "host": "localhost",
    "port": 5433,
    "username": "user",
    "password": "gAAAAABp3MwT...[encrypted]...==",
    "database_name": "dataconnector",
    "is_staff": true,
    "user": 1,
    "created_at": "2026-04-13T10:57:23.083816Z"
  }
]
```

### HTTP Methods Supported:
- **GET** - Retrieve all connections or a specific connection
- **POST** - Create a new database connection
- **PUT** - Update an existing connection
- **DELETE** - Remove a connection (with cascade delete)
- **OPTIONS** - View allowed methods and schema

### How to Use This Page - Creating a Connection via API:

1. **Via Django REST Form (GUI):**
   - Click **POST** button at the top right
   - Fill in all required fields:
     - **Name:** "My Database Connection"
     - **Database Type:** postgresql | mysql | mongodb | clickhouse
     - **Host:** Database server address
     - **Port:** Database port number
     - **Username:** Database user
     - **Password:** Database password
     - **Database Name:** Database name
   - Click **POST** button to submit

2. **Via cURL (Command Line):**
   ```bash
   curl -X POST http://localhost:8001/api/connections/ \
     -H "Authorization: Token <your-token>" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "My PostgreSQL",
       "db_type": "postgresql",
       "host": "localhost",
       "port": 5432,
       "username": "postgres",
       "password": "password",
       "database_name": "mydb"
     }'
   ```

3. **Response:** 201 Created with connection ID and encrypted password

### Database Types Supported:
| Type | Default Port | Example Host |
|------|--------------|--------------|
| **postgresql** | 5432 | localhost |
| **mysql** | 3306 | db.example.com |
| **mongodb** | 27017 | mongodb+srv://user:pass@cluster.mongodb.net |
| **clickhouse** | 8123 | ch.example.com |

### Who Should Use This?
- 👨‍💻 Backend developers (API integration)
- 🔧 Database engineers (mass operations)
- 📊 System administrators (scripting & automation)
- 🤖 CI/CD pipelines (automated deployment)

### Security Notes:
- ✅ Passwords are encrypted before storage
- ✅ Only authenticated users can access
- ✅ CSRF protection on POST/PUT/DELETE
- ✅ User-based access control (see own connections)
- ⚠️ Never share API tokens in logs or version control

---

## 📁 Page 3: API Files (Port 8001)

### Overview
**Data Files API** - Technical interface to access extracted data files and manage file sharing.

**URL:** http://localhost:8001/api/files/

### Features Available on This Page:
- ✅ **List all files** - View extracted data files with metadata
- ✅ **View file details** - Get specific file information
- ✅ **Download files** - Retrieve file content (JSON/CSV)
- ✅ **Share files** - Grant access to other users
- ✅ **Unshare files** - Revoke access from users
- ✅ **Delete files** - Soft delete or permanent delete
- ✅ **Restore files** - Recover from trash
- ✅ **Filter & sort** - Query files by date, table, or connection

### What This Shows:
- All extracted data files
- File metadata (owner, format, timestamps)
- Shared access information
- File paths and locations
- File sizes and data counts
- Extraction source (connection & table)

### JSON Response Example:
```json
[
  {
    "id": 13,
    "user": {
      "id": 2,
      "username": "john_sales",
      "email": "john@company.com",
      "is_staff": false
    },
    "extracted_data": 15,
    "filepath": "/media/extraction_Users_Export_john_sales_20260413_152905.json",
    "format_type": "json",
    "shared_with": [
      {
        "id": 3,
        "username": "sarah_analytics",
        "email": "sarah@company.com"
      }
    ],
    "created_at": "2026-04-13T15:29:05.746315Z",
    "updated_at": "2026-04-13T15:29:05.859022Z"
  }
]
```

### Features:
- **View:** All file details in one place
- **Filter:** By format, owner, shared status
- **Download:** In JSON or CSV format
- **Create:** Add new file records

### HTTP Methods Supported:
- **GET** - Retrieve all files or a specific file
- **POST** - Upload or create new file record
- **PUT** - Update file metadata or sharing settings
- **DELETE** - Soft delete or permanently remove files
- **OPTIONS** - View allowed methods and schema

### Available File Operations via API:

**1. Download File:**
```
GET /api/files/{id}/download/
Response: File content (JSON/CSV) with appropriate headers
```

**2. Share File with Users:**
```
POST /api/files/{id}/share/
Body: {
  "user_ids": [2, 3, 4]
}
Response: 200 OK with updated shared_with list
```

**3. Unshare File from Users:**
```
POST /api/files/{id}/unshare/
Body: {
  "user_ids": [2, 3]
}
Response: 200 OK with updated shared_with list
```

**4. Delete File:**
```
DELETE /api/files/{id}/
Response: 204 No Content (soft delete)
```

**5. Restore Deleted File:**
```
POST /api/files/{id}/restore/
Response: 200 OK with restored file data
```

### Query Parameters for Filtering:
```
GET /api/files/?format_type=json&table_name=users&connection_id=1
GET /api/files/?created_after=2026-04-01&created_before=2026-04-30
GET /api/files/?shared_only=true
GET /api/files/?search=keyword
```

### File Metadata Fields:
| Field | Description | Type |
|-------|-------------|------|
| **id** | Unique file identifier | Integer |
| **user** | File owner information | Object |
| **filename** | Original name | String |
| **extracted_data** | Number of records | Integer |
| **filepath** | Server path | String |
| **format_type** | json or csv | String |
| **shared_with** | Users with access | Array |
| **table_name** | Source table | String |
| **connection_name** | Source connection | String |
| **created_at** | Creation timestamp | DateTime |
| **updated_at** | Last modified | DateTime |

### Who Should Use This?
- 👨‍💻 Backend developers (API integration)
- 📊 Data analysts needing raw API access
- 🔧 System integrators (automated workflows)
- 🤖 CI/CD pipelines (file automation)

### Security Notes:
- ✅ User-based access control (see own & shared files)
- ✅ CSRF protection on POST/PUT/DELETE
- ✅ Token-based authentication required
- ✅ File sharing is granular (per user)
- ⚠️ Soft delete preserves data; use restore if needed
- ⚠️ Sharing creates user permissions immediately

---

## ⚙️ Page 4: Admin Panel (Port 8001)

### Overview
**System Administration Interface** - Full control of the platform.

**URL:** http://localhost:8001/admin/

**Access:** Admin users only (Username: `admin`, Password: `admin123`)

### Login Process:
1. Navigate to http://localhost:8001/admin/
2. Enter admin credentials
3. Click **Log in**

### Admin Features:

#### 1. **User Management**
- View all platform users
- Create new user accounts
- Edit user roles and permissions
- Deactivate users
- Reset passwords

#### 2. **Connections Management**
- View all database connections
- Create new connections
- Edit connection details
- Test connections
- Delete unused connections

#### 3. **Files Management**
- Monitor all extracted files
- View file history and timestamps
- Manage file access permissions
- Delete old files
- Export file metadata

#### 4. **System Configuration**
- Configure database settings
- Set up authentication
- Manage security settings
- Configure email notifications
- Set up backup schedules

#### 5. **Data Monitoring**
- Track extraction activities
- Monitor file storage usage
- View audit logs
- Generate system reports
- Check performance metrics

#### 6. **Connector Setup**
- Configure PostgreSQL connections
- Configure MySQL connections
- Set up MongoDB connections
- Set up ClickHouse connections

### Normal Admin Workflow:
```
Log In → View Dashboard → Manage Users → Monitor Connections 
  → Check Files → Configure Settings → View Recent Actions
```

---

## ✅ Common Tasks

### Task 1: Extract Data from a Database

**Scenario:** You need sales data from the PostgreSQL database

**Steps:**

1. ✅ **Go to Frontend** (http://localhost:3000)
2. ✅ **Login** with your credentials
3. ✅ **Select Connection:**
   - Click "Connections" dropdown
   - Choose "Test PostgreSQL"
4. ✅ **Enter Table Name:**
   - Type "orders" (or table name)
5. ✅ **Set Batch Size:**
   - Keep default (1000) or change as needed
6. ✅ **Select Format:**
   - Choose "JSON" or "CSV"
7. ✅ **Click Extract Data**
8. ✅ **Wait** for completion (green notification)
9. ✅ **Preview** in the Data Grid
10. ✅ **Download** or **Share** as needed

**Time Required:** 5-10 seconds typically

---

### Task 2: Share Data with a Colleague

**Scenario:** Your analyst needs to see the extracted sales data

**Steps:**

1. ✅ **Go to Stored Files** section (left panel)
2. ✅ **Find the file** you want to share
3. ✅ **Click the file** to expand it
4. ✅ **Click 📤 Share button**
5. ✅ **Search for colleague's username**
6. ✅ **Select them** from search results
7. ✅ **Click Share**
8. ✅ **See green notification** - File shared successfully!
9. ✅ **Colleague receives access** automatically

**Time Required:** 1-2 minutes

---

### Task 3: Download Data

**Scenario:** You need to take data offline for analysis

**Steps:**

1. ✅ **Go to Stored Files** section
2. ✅ **Find the file** you want to download
3. ✅ **Click on the file** to expand
4. ✅ **Select format:**
   - Choose JSON (for data analysis tools)
   - Choose CSV (for Excel/Sheets)
5. ✅ **Click Download button**
6. ✅ **Choose download location** on your computer
7. ✅ **Click Save**
8. ✅ **File saved** to your Downloads folder

**File Location:** Usually `C:\Users\[YourName]\Downloads\` (Windows) or `~/Downloads/` (Mac/Linux)

---

### Task 4: Create a New Database Connection (Admin)

**Scenario:** You want to add a new MySQL database

**Steps:**

1. ✅ **Go to Frontend** (http://localhost:3000)
2. ✅ **Login as admin**
3. ✅ **Scroll to Connection Form** (top left)
4. ✅ **Fill in connection details:**
   - **Name:** "Customer Database"
   - **Type:** Select "MySQL"
   - **Host:** "mysql.company.local"
   - **Port:** 3306
   - **Username:** "customer_user"
   - **Password:** "password123"
   - **Database Name:** "customers"
5. ✅ **Click Create Connection**
6. ✅ **See success notification**
7. ✅ **Connection appears** in Connections dropdown
8. ✅ **Available for all users** in the system

---

### Task 5: Edit Extracted Data

**Scenario:** You need to fix an error in the extracted data

**Steps:**

1. ✅ **Extract data** (see Task 1)
2. ✅ **Click on any cell** in the Data Grid
3. ✅ **Type new value**
4. ✅ **Press Enter** or click outside cell
5. ✅ **See cell update** (background highlight)
6. ✅ **Scroll to bottom** of the Data Grid
7. ✅ **Click Save Data button**
8. ✅ **See green notification** - Data saved successfully!
9. ✅ **Changes are permanent** in the system

---

## 🐛 Troubleshooting

### Issue 1: "Can't Connect to Backend"

**Symptoms:** Can't access http://localhost:8001

**Solutions:**
1. ✅ Check if Django server is running
2. ✅ Open terminal and run: `python manage.py runserver 0.0.0.0:8001`
3. ✅ Verify port 8001 is not in use: Check Task Manager/Activity Monitor
4. ✅ Restart the backend server

**Command:**
```bash
cd backend
python manage.py runserver 0.0.0.0:8001
```

---

### Issue 2: "Database Connection Failed"

**Symptoms:** Error when trying to extract data

**Solutions:**
1. ✅ Verify database is running
2. ✅ Check connection credentials (host, port, username, password)
3. ✅ Verify table name is correct
4. ✅ Check firewall isn't blocking the port
5. ✅ Test database connection with another tool first

**For PostgreSQL:**
```bash
psql -h localhost -U user -d database_name
```

---

### Issue 3: "Login Failed"

**Symptoms:** "Invalid username or password" error

**Solutions:**
1. ✅ Check CAPS LOCK is OFF
2. ✅ Verify credentials from demo accounts list
3. ✅ Try with `admin` / `admin123` first
4. ✅ Clear browser cookies (Settings → Privacy)
5. ✅ Try in Incognito/Private window
6. ✅ Check server logs for errors

---

### Issue 4: "File Not Downloading"

**Symptoms:** Download button doesn't work

**Solutions:**
1. ✅ Check browser pop-up blocker settings
2. ✅ Allow pop-ups for localhost:3000
3. ✅ Check Downloads folder (might already be there)
4. ✅ Try different file format (JSON vs CSV)
5. ✅ Clear browser cache (Settings → Clear Cache)
6. ✅ Try Chrome browser if using Firefox

---

### Issue 5: "Can't Share File"

**Symptoms:** Share button doesn't work or gives error

**Solutions:**
1. ✅ Make sure you own the file or have permission
2. ✅ Verify colleague's username is spelled correctly
3. ✅ Try searching with first letter only
4. ✅ Refresh page (F5) and try again
5. ✅ Check colleague's username exists in system
6. ✅ Ask admin to verify user account exists

---

## 📞 Getting Help

### For Technical Issues:
- Check backend logs: `django.log` or console output
- Check frontend logs: Browser Developer Tools (F12)
- Review error messages carefully - they usually indicate the problem

### For User Issues:
- Contact your admin or system administrator
- Check this guide for similar situations
- Take a screenshot of the error for support team

### For Feature Requests:
- Document what you want to do
- Explain current limitations
- Get approval from your admin first
- Submit request to development team

---

## 🎯 Quick Reference Card

### URLs to Remember:
| Name | URL | Bookmark |
|------|-----|----------|
| Frontend | http://localhost:3000 | ⭐⭐⭐ |
| Backend Home | http://localhost:8001 | ⭐⭐ |
| API Connections | http://localhost:8001/api/connections/ | ⭐ |
| API Files | http://localhost:8001/api/files/ | ⭐ |
| Admin Panel | http://localhost:8001/admin/ | ⭐⭐ |

### Keyboard Shortcuts:
| Action | Shortcut |
|--------|----------|
| Login | Enter (after filling form) |
| Edit cell | Click and type |
| Save changes | Ctrl+S (or click Save) |
| Go back | Alt+← or Backspace |
| Refresh | F5 or Ctrl+R |
| Developer Tools | F12 |

### Button Reference:
| Button | Location | Action |
|--------|----------|--------|
| Login | Frontend form | Login to system |
| Logout | Top right (after login) | Exit system |
| Extract Data | Right panel | Start data extraction |
| Save Data | Bottom of grid | Save edits |
| Download | Files section | Download file |
| Share | Files section | Share with others |
| Create Connection | Left panel | Add new database |

---

## ✨ Best Practices

### ✅ DO:
- ✅ Test connections before extracting large datasets
- ✅ Use meaningful names for connections
- ✅ Keep sensitive data access restricted
- ✅ Share only necessary data with colleagues
- ✅ Back up important data regularly
- ✅ Review files before sharing
- ✅ Use CSV for Excel, JSON for APIs

### ❌ DON'T:
- ❌ Don't share passwords through chat/email
- ❌ Don't extract extremely large tables (>100k rows without batching)
- ❌ Don't delete files without backup
- ❌ Don't share confidential databases
- ❌ Don't write table names manually without checking spelling
- ❌ Don't modify database connection passwords in plain text

---

## 📝 Verification Checklist

Use this checklist to verify everything is working:

### ✓ System Setup
- [ ] Backend server running on port 8001
- [ ] Frontend server running on port 3000
- [ ] Database(s) accessible
- [ ] All APIs responding

### ✓ Login
- [ ] Can access http://localhost:3000
- [ ] Can login with demo credentials
- [ ] Dashboard displays username correctly
- [ ] Logout button works

### ✓ Connections
- [ ] Can create new connection
- [ ] Connection appears in dropdown
- [ ] Can select from dropdown
- [ ] Shows success notification

### ✓ Data Extraction
- [ ] Can enter table name
- [ ] Can select batch size
- [ ] Can select format (JSON/CSV)
- [ ] Extract Data button works
- [ ] Data appears in grid
- [ ] Notifications display correctly

### ✓ File Management
- [ ] Can see files in Stored Files section
- [ ] Can download files
- [ ] Can change format (JSON/CSV)
- [ ] Downloaded file opens correctly

### ✓ Data Sharing
- [ ] Can click Share button
- [ ] Can search for users
- [ ] Can select and share
- [ ] Friend receives access

### ✓ Admin Functions
- [ ] Can login to admin panel
- [ ] Can view users
- [ ] Can view connections
- [ ] Can view files
- [ ] Can see monitoring data

---

## 🎓 Learning Path for New Users

### Day 1: Getting Started
1. Read "Quick Start" section
2. Access login page (http://localhost:3000)
3. Login with john_sales credentials
4. Explore dashboard layout
5. Logout and try admin credentials

### Day 2: Basic Operations
1. Create a dummy database connection
2. Extract data from a test table
3. View the results in the grid
4. Download data as JSON
5. Try CSV format too

### Day 3: Intermediate Tasks
1. Edit extracted data
2. Save changes
3. Find and share a file
4. Change file permissions
5. Check your shared files

### Day 4: Advanced Features
1. Try batch size variations
2. Extract large datasets
3. Monitor extraction time
4. Check API endpoints at /api/connections/
5. Explore /api/files/ endpoint

### Day 5: Administration (Admin Only)
1. Access admin panel
2. View all users
3. View all connections
4. Check recent activity
5. Try creating a new user

---

## 📊 System Status Page

Visit http://localhost:8001/ to see:
- ✅ System Health
- ✅ API Endpoints available
- ✅ Admin Credentials
- ✅ Features Overview
- ✅ Quick navigation buttons

---

## 🔒 Security Notes

### Data Protection:
- Passwords are **encrypted** before storage
- Connection credentials are **never displayed** in frontend
- Files are stored with **access controls**
- Only authorized users can access shared files

### Best Practices:
- Change default passwords immediately
- Use strong passwords (12+ characters)
- Don't share credentials via email/chat
- Enable two-factor authentication if available
- Review file access permissions regularly

---

## 📞 Support

### Getting Support:
1. Check this guide first (search relevant section)
2. Check troubleshooting section
3. Review error messages carefully
4. Check browser console (F12)
5. Contact your system administrator
6. Include screenshots when reporting issues

### Reporting Issues:
- **What:** Clear description of problem
- **When:** When did it start?
- **Where:** Which page/function?
- **How:** Steps to reproduce
- **Screenshots:** Clear images of error

---

**Last Updated:** April 14, 2026  
**Version:** 2.0  
**Maintained by:** Data Connector Platform Team

---

This guide is designed to be self-sufficient for non-technical users while providing reference material for developers. Please refer back to relevant sections as needed!

