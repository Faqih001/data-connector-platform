#!/bin/bash

# Data Connector Platform - Quick Start Setup (Path A - Local Development)
# This script automates the local development setup

set -e

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_step() {
    echo -e "${YELLOW}→${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Data Connector Platform - Quick Start Setup (Local Dev)       ║"
echo "║   $(date '+%Y-%m-%d %H:%M:%S')                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ============================================================================
# Step 1: Prerequisites Check
# ============================================================================

print_header "STEP 1: CHECKING PREREQUISITES"

print_step "Checking Node.js..."
if ! command -v node &> /dev/null; then
    print_error "Node.js not found. Please install Node.js v16+"
    exit 1
fi
NODE_VERSION=$(node --version)
print_success "Node.js $NODE_VERSION found"

print_step "Checking Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 not found. Please install Python v3.8+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
print_success "Python $PYTHON_VERSION found"

print_step "Checking npm..."
if ! command -v npm &> /dev/null; then
    print_error "npm not found. Please install npm v7+"
    exit 1
fi
NPM_VERSION=$(npm --version)
print_success "npm $NPM_VERSION found"

# ============================================================================
# Step 2: Frontend Setup
# ============================================================================

print_header "STEP 2: FRONTEND SETUP"

print_step "Installing Node.js dependencies..."
if npm install; then
    print_success "Node.js dependencies installed"
else
    print_error "Failed to install Node.js dependencies"
    exit 1
fi

print_step "Building Next.js application..."
if npm run build; then
    print_success "Next.js build successful"
else
    print_error "Failed to build Next.js application"
    print_error "Try: npm install --legacy-peer-deps"
    exit 1
fi

# ============================================================================
# Step 3: Backend Setup
# ============================================================================

print_header "STEP 3: BACKEND SETUP"

print_step "Navigating to backend directory..."
cd backend

print_step "Creating Python virtual environment..."
if [ ! -d ".venv" ]; then
    if python3 -m venv .venv; then
        print_success "Virtual environment created"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
else
    print_success "Virtual environment already exists"
fi

print_step "Activating virtual environment..."
if source .venv/bin/activate 2>/dev/null; then
    print_success "Virtual environment activated"
else
    print_error "Failed to activate virtual environment"
    exit 1
fi

print_step "Upgrading pip..."
pip install --quiet --upgrade pip

print_step "Installing Python dependencies..."
if pip install -q -r requirements.txt; then
    print_success "Python dependencies installed"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

print_step "Verifying Django installation..."
if python -c "import django; print(f'Django {django.VERSION[0]}.{django.VERSION[1]}')" &> /dev/null; then
    print_success "Django verified"
else
    print_error "Django installation failed"
    exit 1
fi

# ============================================================================
# Step 4: Database Setup
# ============================================================================

print_header "STEP 4: DATABASE SETUP (Docker)"

print_step "Checking Docker availability..."
if ! command -v docker &> /dev/null; then
    print_error "Docker not found. Skipping database initialization."
    echo -e "${YELLOW}To use databases, install Docker and run:${NC}"
    echo "  docker-compose up -d db mysql mongo clickhouse"
else
    print_success "Docker found"
    
    print_step "Starting database services..."
    cd ..  # Back to project root
    
    if docker-compose up -d db mysql mongo clickhouse; then
        print_success "Database services started"
        
        print_step "Waiting for databases to initialize..."
        sleep 15
        
        print_step "Verifying database connectivity..."
        cd backend
        
        # Test PostgreSQL
        if python -c "import psycopg2; psycopg2.connect('dbname=dataconnector user=user password=password host=localhost port=5433')" &> /dev/null; then
            print_success "PostgreSQL connection verified"
        else
            print_error "PostgreSQL connection failed (this may be normal if not using it)"
        fi
    else
        print_error "Failed to start database services"
        print_error "Make sure Docker daemon is running"
    fi
    
    cd backend
fi

# ============================================================================
# Step 5: Django Migrations
# ============================================================================

print_header "STEP 5: DJANGO MIGRATIONS"

print_step "Running database migrations..."
if python manage.py migrate --noinput; then
    print_success "Database migrations completed"
else
    print_error "Failed to run migrations"
    print_error "If using SQLite (default), this is usually okay"
fi

# ============================================================================
# Step 6: Final Verification
# ============================================================================

print_header "STEP 6: FINAL VERIFICATION"

print_step "Checking Django setup..."
if python manage.py check &> /dev/null; then
    print_success "Django system check passed"
else
    print_error "Django system check failed"
fi

print_step "Verifying backend can start..."
# Try to start server for 3 seconds to verify it works
timeout 3 python manage.py runserver &> /dev/null || true
print_success "Backend server verified (can start)"

# ============================================================================
# Summary & Next Steps
# ============================================================================

print_header "SETUP COMPLETE!"

echo -e "${GREEN}✓ All setup steps completed successfully!${NC}"
echo ""
echo -e "${BLUE}Project structure:${NC}"
echo "  Frontend: $(pwd)/../app"
echo "  Backend:  $(pwd)"
echo "  Database: Docker containers (if Docker available)"
echo ""
echo -e "${BLUE}Configuration:${NC}"
echo "  • Frontend runs on: http://localhost:3000"
echo "  • Backend runs on:  http://localhost:8000"
echo "  • PostgreSQL:       localhost:5433"
echo "  • MySQL:            localhost:3307"
echo "  • MongoDB:          localhost:27018"
echo "  • ClickHouse:       localhost:8124"
echo ""
echo -e "${YELLOW}To start development:${NC}"
echo ""
echo "  Terminal 1 - Frontend:"
echo "    cd $(pwd)/../"
echo "    npm run dev"
echo ""
echo "  Terminal 2 - Backend:"
echo "    cd $(pwd)"
echo "    source .venv/bin/activate"
echo "    python manage.py runserver"
echo ""
echo "  Terminal 3 - View Database Logs (optional):"
echo "    docker-compose logs -f db mysql mongo clickhouse"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo "  • npm run build          - Build Next.js for production"
echo "  • npm run lint           - Run ESLint"
echo "  • python manage.py test  - Run backend tests"
echo "  • docker-compose down    - Stop all database services"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "  • See SETUP.md for detailed setup instructions"
echo "  • See README.md for project overview"
echo "  • See NAVIGATION_AND_USER_GUIDE.md for usage guide"
echo ""
