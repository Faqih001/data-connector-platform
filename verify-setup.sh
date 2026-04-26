#!/bin/bash

# Data Connector Platform - Setup Verification Script
# This script verifies that all components are installed and configured correctly

set -e

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Function to print section header
print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Function to print check result
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Data Connector Platform - Setup Verification                 ║"
echo "║   $(date '+%Y-%m-%d %H:%M:%S')                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ============================================================================
# 1. System Tools Verification
# ============================================================================

print_header "1. SYSTEM TOOLS VERIFICATION"

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    check_pass "Node.js installed: $NODE_VERSION"
else
    check_fail "Node.js not found - Required v16+"
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    check_pass "npm installed: $NPM_VERSION"
else
    check_fail "npm not found - Required v7+"
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    check_pass "Python3 installed: $PYTHON_VERSION"
else
    check_fail "Python3 not found - Required v3.8+"
fi

# Check pip
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    check_pass "pip3 installed: $(echo $PIP_VERSION | cut -d' ' -f2)"
else
    check_fail "pip3 not found - Required v21+"
fi

# Check Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    check_pass "Git installed: $(echo $GIT_VERSION | cut -d' ' -f3)"
else
    check_warn "Git not found (optional)"
fi

# Check Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    check_pass "Docker installed: $(echo $DOCKER_VERSION | cut -d' ' -f3 | sed 's/,//')"
else
    check_warn "Docker not found (optional for Path A)"
fi

# Check Docker Compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    check_pass "Docker Compose installed: $(echo $COMPOSE_VERSION | cut -d' ' -f3 | sed 's/,//')"
else
    check_warn "Docker Compose not found (optional for Path A)"
fi

# ============================================================================
# 2. Frontend Verification
# ============================================================================

print_header "2. FRONTEND (Next.js) VERIFICATION"

# Check package.json exists
if [ -f "package.json" ]; then
    check_pass "package.json found"
else
    check_fail "package.json not found"
    exit 1
fi

# Check node_modules
if [ -d "node_modules" ]; then
    check_pass "node_modules directory exists"
    
    # Check key dependencies
    if [ -d "node_modules/next" ]; then
        NEXT_VERSION=$(node -e "console.log(require('./node_modules/next/package.json').version)")
        check_pass "Next.js installed: $NEXT_VERSION"
    else
        check_fail "Next.js not installed in node_modules"
    fi
    
    if [ -d "node_modules/react" ]; then
        REACT_VERSION=$(node -e "console.log(require('./node_modules/react/package.json').version)")
        check_pass "React installed: $REACT_VERSION"
    else
        check_fail "React not installed in node_modules"
    fi
else
    check_warn "node_modules not found - run 'npm install'"
fi

# Check .next build directory
if [ -d ".next" ]; then
    check_pass "Next.js build (.next) found"
else
    check_warn ".next build directory not found - run 'npm run build'"
fi

# Check next.config.ts
if [ -f "next.config.ts" ]; then
    check_pass "next.config.ts found"
else
    check_fail "next.config.ts not found"
fi

# ============================================================================
# 3. Backend Verification
# ============================================================================

print_header "3. BACKEND (Django) VERIFICATION"

# Check backend directory
if [ -d "backend" ]; then
    check_pass "backend directory exists"
else
    check_fail "backend directory not found"
    exit 1
fi

# Check Django files
if [ -f "backend/manage.py" ]; then
    check_pass "Django manage.py found"
else
    check_fail "Django manage.py not found"
fi

if [ -f "backend/requirements.txt" ]; then
    check_pass "requirements.txt found"
    REQ_COUNT=$(wc -l < backend/requirements.txt)
    check_pass "Found $REQ_COUNT Python dependencies"
else
    check_fail "requirements.txt not found"
fi

# Check virtual environment
if [ -d "backend/.venv" ]; then
    check_pass "Python virtual environment (.venv) exists"
    
    # Try to detect Python version in venv
    if [ -f "backend/.venv/bin/python3" ]; then
        VENV_PYTHON_VERSION=$(backend/.venv/bin/python3 --version)
        check_pass "Virtual environment Python: $VENV_PYTHON_VERSION"
    fi
    
    # Check if key packages are installed
    if backend/.venv/bin/pip list 2>/dev/null | grep -q "Django"; then
        DJANGO_VERSION=$(backend/.venv/bin/pip show Django 2>/dev/null | grep Version | cut -d' ' -f2)
        check_pass "Django installed in venv: $DJANGO_VERSION"
    else
        check_warn "Django not installed in venv - run 'pip install -r requirements.txt'"
    fi
    
    if backend/.venv/bin/pip list 2>/dev/null | grep -q "psycopg2"; then
        check_pass "psycopg2 (PostgreSQL) installed in venv"
    else
        check_warn "psycopg2 not installed in venv"
    fi
    
    if backend/.venv/bin/pip list 2>/dev/null | grep -q "pymongo"; then
        check_pass "pymongo (MongoDB) installed in venv"
    else
        check_warn "pymongo not installed in venv"
    fi
    
    if backend/.venv/bin/pip list 2>/dev/null | grep -q "mysql-connector"; then
        check_pass "mysql-connector (MySQL) installed in venv"
    else
        check_warn "mysql-connector not installed in venv"
    fi
else
    check_warn "Python virtual environment not found - run 'python3 -m venv backend/.venv'"
fi

# Check settings.py
if [ -f "backend/backend/settings.py" ]; then
    check_pass "Django settings.py found"
else
    check_fail "Django settings.py not found"
fi

# Check database migrations
if [ -d "backend/connector/migrations" ]; then
    MIGRATION_COUNT=$(find backend/connector/migrations -name "*.py" | wc -l)
    check_pass "Database migrations directory found ($MIGRATION_COUNT files)"
else
    check_warn "Database migrations directory not found"
fi

# ============================================================================
# 4. Docker Verification
# ============================================================================

print_header "4. DOCKER CONFIGURATION VERIFICATION"

# Check docker-compose.yml
if [ -f "docker-compose.yml" ]; then
    check_pass "docker-compose.yml found"
    
    # Check if version key is present (should be removed)
    if grep -q "^version:" docker-compose.yml; then
        check_warn "docker-compose.yml contains obsolete 'version' key (should be removed)"
    else
        check_pass "docker-compose.yml version key removed (correct)"
    fi
    
    # Check for required services
    for service in frontend backend db mysql mongo clickhouse; do
        if grep -q "  $service:" docker-compose.yml; then
            check_pass "Service '$service' defined in docker-compose.yml"
        else
            check_warn "Service '$service' not found in docker-compose.yml"
        fi
    done
else
    check_fail "docker-compose.yml not found"
fi

# Check Dockerfiles
if [ -f "Dockerfile.frontend" ]; then
    check_pass "Dockerfile.frontend found"
    
    # Check for memory optimization
    if grep -q "NODE_OPTIONS" Dockerfile.frontend; then
        check_pass "Dockerfile.frontend has NODE_OPTIONS memory optimization"
    else
        check_warn "Dockerfile.frontend missing NODE_OPTIONS optimization"
    fi
else
    check_fail "Dockerfile.frontend not found"
fi

if [ -f "Dockerfile.backend" ]; then
    check_pass "Dockerfile.backend found"
else
    check_fail "Dockerfile.backend not found"
fi

# Check if Docker is running
if command -v docker &> /dev/null; then
    if docker info &> /dev/null; then
        check_pass "Docker daemon is running"
    else
        check_warn "Docker daemon is not running"
    fi
fi

# ============================================================================
# 5. Configuration Files Verification
# ============================================================================

print_header "5. CONFIGURATION FILES VERIFICATION"

CONFIG_FILES=(
    "tsconfig.json"
    "eslint.config.mjs"
    "postcss.config.mjs"
    "backend/backend/settings.py"
    "backend/backend/urls.py"
)

for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        check_pass "Config file found: $file"
    else
        check_warn "Config file not found: $file (may be optional)"
    fi
done

# ============================================================================
# 6. Port Availability Check
# ============================================================================

print_header "6. PORT AVAILABILITY CHECK"

# Function to check port
check_port() {
    local port=$1
    local service=$2
    
    if command -v nc &> /dev/null; then
        if ! nc -z localhost $port 2>/dev/null; then
            check_pass "Port $port available for $service"
        else
            check_warn "Port $port already in use ($service)"
        fi
    else
        check_warn "netcat not found - cannot check ports"
    fi
}

check_port 3000 "Frontend"
check_port 8000 "Backend"
check_port 5433 "PostgreSQL"
check_port 3307 "MySQL"
check_port 27018 "MongoDB"
check_port 8124 "ClickHouse"

# ============================================================================
# 7. Disk Space Check
# ============================================================================

print_header "7. DISK SPACE VERIFICATION"

AVAILABLE_SPACE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$AVAILABLE_SPACE" -ge 2 ]; then
    check_pass "Sufficient disk space: ${AVAILABLE_SPACE}GB available (need 2GB+)"
else
    check_warn "Low disk space: only ${AVAILABLE_SPACE}GB available"
fi

# Check specific directory sizes
if [ -d "node_modules" ]; then
    NODE_SIZE=$(du -sh node_modules 2>/dev/null | cut -f1)
    check_pass "node_modules size: $NODE_SIZE"
fi

if [ -d ".next" ]; then
    NEXT_SIZE=$(du -sh .next 2>/dev/null | cut -f1)
    check_pass ".next build size: $NEXT_SIZE"
fi

if [ -d "backend/.venv" ]; then
    VENV_SIZE=$(du -sh backend/.venv 2>/dev/null | cut -f1)
    check_pass "backend/.venv size: $VENV_SIZE"
fi

# ============================================================================
# Summary
# ============================================================================

print_header "VERIFICATION SUMMARY"

TOTAL=$((PASSED + FAILED))
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ "$FAILED" -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
fi
echo -e "Total:  $TOTAL"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Your setup is ready.${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "  1. For local development (Path A):"
    echo "     Terminal 1: npm run dev"
    echo "     Terminal 2: cd backend && source .venv/bin/activate && python manage.py runserver"
    echo ""
    echo "  2. For Docker setup (Path B):"
    echo "     docker-compose up -d"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please review the errors above.${NC}"
    echo ""
    echo -e "${YELLOW}Common fixes:${NC}"
    echo "  • npm install                          (install frontend deps)"
    echo "  • python3 -m venv backend/.venv        (create Python env)"
    echo "  • cd backend && source .venv/bin/activate && pip install -r requirements.txt"
    echo "  • npm run build                        (build Next.js)"
    echo ""
    exit 1
fi
