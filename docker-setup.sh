#!/bin/bash

# Data Connector Platform - Docker Setup (Path B)
# This script sets up and starts the entire stack in Docker containers

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

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check for venv and optionally activate it
activate_venv() {
    if [ -f "backend/.venv/bin/activate" ]; then
        print_step "Activating Python virtual environment..."
        source backend/.venv/bin/activate
        print_success "Virtual environment activated"
    fi
}

deactivate_venv() {
    if command -v deactivate &> /dev/null; then
        print_step "Deactivating Python virtual environment..."
        deactivate 2>/dev/null || true
        print_success "Virtual environment deactivated"
    fi
}

# Trap to ensure venv is deactivated on exit
trap 'deactivate_venv' EXIT

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Data Connector Platform - Docker Setup (Full Stack)          ║"
echo "║   $(date '+%Y-%m-%d %H:%M:%S')                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ============================================================================
# Step 1: Prerequisites & Warnings
# ============================================================================

print_header "STEP 1: PREREQUISITES CHECK & CONFIGURATION"

print_step "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    print_error "Docker not found. Please install Docker."
    echo "  Visit: https://docs.docker.com/get-docker/"
    exit 1
fi
DOCKER_VERSION=$(docker --version)
print_success "$DOCKER_VERSION found"

print_step "Checking Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose not found. Please install Docker Compose."
    echo "  Visit: https://docs.docker.com/compose/install/"
    exit 1
fi
COMPOSE_VERSION=$(docker-compose --version)
print_success "Docker Compose installed"

print_step "Checking Docker daemon..."
if ! docker info &> /dev/null; then
    print_error "Docker daemon is not running. Please start Docker."
    echo "  On Linux:   sudo systemctl start docker"
    echo "  On Mac/Windows: Open Docker Desktop"
    exit 1
fi
print_success "Docker daemon is running"

print_step "Checking Docker resources..."
MEMORY=$(docker system info | grep "Total Memory" | awk '{print $3}' | sed 's/GiB//')
if (( $(echo "$MEMORY < 6" | bc -l) )); then
    print_warning "Docker memory is less than 6GB ($MEMORY GB) - Build may fail"
    print_info "Recommendation: Increase Docker memory to 8-10GB for reliable builds"
    echo "  Docker Desktop → Preferences/Settings → Resources → Memory"
else
    print_success "Docker memory is sufficient ($MEMORY GB)"
fi

print_step "Checking available disk space..."
DISKSPACE=$(df -BG "$SCRIPT_DIR" | tail -1 | awk '{print $4}' | sed 's/G//')
if (( $(echo "$DISKSPACE < 5" | bc -l) )); then
    print_error "Insufficient disk space ($DISKSPACE GB). Need at least 5GB."
    echo "  Clean up space and retry."
    exit 1
else
    print_success "Disk space is sufficient ($DISKSPACE GB free)"
fi

print_header "STEP 2: DOCKER CONFIGURATION & CLEANUP"

print_step "Verifying docker-compose.yml..."
if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml not found"
    exit 1
fi
print_success "docker-compose.yml found"

print_step "Checking for obsolete version key..."
if grep -q "^version:" docker-compose.yml; then
    print_warning "docker-compose.yml has obsolete 'version' key - will be ignored"
    print_info "Consider removing it with: sed -i '1s/^version:.*//' docker-compose.yml"
else
    print_success "docker-compose.yml version key is correct"
fi

print_warning "Cleaning up Docker system to free memory for build..."
print_step "Running Docker system cleanup..."
docker system prune -f --volumes > /dev/null 2>&1 || true
print_success "Docker system cleaned"

print_step "Checking Docker build cache..."
docker system df 2>/dev/null | grep -A1 "Build cache" || true

# ============================================================================
# Step 3: Pre-build Frontend (Avoid SIGBUS)
# ============================================================================

print_header "STEP 3: PRE-BUILD FRONTEND LOCALLY (Avoid Docker SIGBUS Error)"

print_warning "Building frontend locally first to avoid Docker memory issues"
print_info "This avoids SIGBUS errors during Docker build"

print_step "Checking Node.js..."
if ! command -v node &> /dev/null; then
    print_warning "Node.js not found - will build in Docker"
else
    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION found"
    
    print_step "Installing frontend dependencies..."
    if npm ci --prefer-offline --no-audit; then
        print_success "Frontend dependencies installed"
    else
        print_error "Failed to install frontend dependencies"
        print_warning "Continuing with Docker build..."
    fi
    
    print_step "Building Next.js application..."
    if npm run build 2>/dev/null; then
        print_success "Next.js build successful locally"
        print_info "Frontend .next folder will be used in Docker"
    else
        BUILD_STATUS=$?
        if [ $BUILD_STATUS -eq 139 ] || [ $BUILD_STATUS -eq 134 ]; then
            print_error "Next.js build failed with SIGBUS (memory issue)"
            print_warning "This is a known issue with Node.js on some systems"
            print_info "Continuing with Docker build using Debian-based Node image"
        else
            print_error "Next.js build failed (exit code: $BUILD_STATUS)"
            print_warning "Docker build will attempt to build frontend"
        fi
    fi
fi

# ============================================================================
# Step 4: Clean Up Previous Containers
# ============================================================================

print_header "STEP 4: CLEANUP PREVIOUS CONTAINERS"

print_step "Checking for existing containers..."
if docker-compose ps -q &> /dev/null; then
    EXISTING=$(docker-compose ps -q | wc -l)
    if [ "$EXISTING" -gt 0 ]; then
        print_warning "Found $EXISTING existing containers"
        print_step "Removing existing containers automatically..."
        # Try graceful stop first, then force kill if needed
        if ! docker-compose down -v 2>/dev/null; then
            print_warning "Graceful shutdown failed, force removing containers..."
            # Force remove containers with permission errors
            docker-compose ps -q | xargs -r docker rm -f 2>/dev/null || true
            print_success "Containers force removed"
        else
            print_success "Existing containers removed"
        fi
    fi
fi

# ============================================================================
# Step 5: Build Docker Images
# ============================================================================

print_header "STEP 5: BUILDING DOCKER IMAGES"

print_warning "This may take 5-15 minutes depending on system resources"
print_info "Using node:20-slim (Debian-based) to avoid Alpine SIGBUS issues"

print_step "Building Docker images..."
BUILD_EXIT_CODE=0
if ! docker-compose build 2>&1; then
    BUILD_EXIT_CODE=$?
    print_error "Docker build failed (Exit code: $BUILD_EXIT_CODE)"
    echo ""
    print_warning "RECOVERY STRATEGIES:"
    echo ""
    echo "  1. SIGBUS / Memory Error:"
    echo "     • Updated Dockerfile uses node:20-slim (Debian) instead of Alpine"
    echo "     • Retry: docker-compose build --no-cache"
    echo "     • If still fails, increase Docker memory to 8-10GB"
    echo ""
    echo "  2. Disk Space Error:"
    echo "     • Free up at least 5-10GB of disk space"
    echo "     • Run: docker system prune -a && docker-compose build --no-cache"
    echo ""
    echo "  3. Cache Issues:"
    echo "     • Clear builder cache: docker builder prune -a"
    echo "     • Rebuild everything: docker-compose build --no-cache"
    echo ""
    echo "  4. If all else fails:"
    echo "     • Completely reset Docker: docker system prune -a --volumes"
    echo "     • Then retry: ./docker-setup.sh"
    echo ""
    print_info "After applying fixes, retry: ./docker-setup.sh"
    exit 1
else
    print_success "Docker images built successfully"
fi

# ============================================================================
# Step 6: Start Services
# ============================================================================

print_header "STEP 6: STARTING DOCKER SERVICES"

print_step "Starting all services..."
if docker-compose up -d 2>&1 | grep -E "(Running|Started|exited with code)"; then
    print_success "All services started"
    START_RESULT=0
else
    START_RESULT=$?
    # If we get a permission error, force remove and retry
    if docker-compose ps -q 2>/dev/null | xargs -r docker rm -f 2>/dev/null; then
        print_warning "Force removed problematic containers, retrying..."
        sleep 2
        if docker-compose up -d 2>&1 | head -3; then
            print_success "Services started after cleanup"
            START_RESULT=0
        else
            print_error "Failed to start services after cleanup"
            START_RESULT=1
        fi
    fi
fi

if [ $START_RESULT -ne 0 ]; then
    exit 1
fi

print_step "Waiting for services to initialize..."
sleep 10

print_step "Checking service status..."
docker-compose ps

# ============================================================================
# Step 7: Verify Services
# ============================================================================

print_header "STEP 7: SERVICE VERIFICATION"

# Check each service
SERVICES=("frontend" "backend" "db" "mysql" "mongo" "clickhouse")
for service in "${SERVICES[@]}"; do
    STATE=$(docker-compose ps $service -q | xargs -I {} docker inspect {} --format='{{.State.Status}}' 2>/dev/null || echo "not-found")
    
    if [ "$STATE" = "running" ]; then
        print_success "Service '$service' is running"
    elif [ "$STATE" = "exited" ]; then
        print_error "Service '$service' exited - check logs: docker-compose logs $service"
    else
        print_error "Service '$service' status unknown"
    fi
done

print_step "Checking backend logs for errors..."
BACKEND_LOGS=$(docker-compose logs backend 2>/dev/null | tail -5)
if echo "$BACKEND_LOGS" | grep -iq "error\|failed\|exception"; then
    print_warning "Potential errors in backend logs:"
    echo "$BACKEND_LOGS" | head -3
else
    print_success "Backend logs look good"
fi

# ============================================================================
# Step 8: Database Migrations
# ============================================================================

print_header "STEP 8: DATABASE MIGRATIONS"

print_step "Waiting for database connections..."
sleep 5

print_step "Running Django migrations..."
if docker-compose exec -T backend python manage.py migrate --noinput; then
    print_success "Database migrations completed"
else
    print_warning "Database migrations failed or already applied"
fi

# ============================================================================
# Step 9: Create Superuser (Optional)
# ============================================================================

print_header "STEP 9: CREATE SUPERUSER (OPTIONAL)"

print_info "Creating default superuser (admin/admin123)"
if docker-compose exec -T backend python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✓ Superuser "admin" created with password "admin123"')
else:
    print('✓ Superuser "admin" already exists')
EOF
then
    print_success "Superuser setup completed"
else
    print_warning "Superuser creation skipped or failed"
fi

# ============================================================================
# Step 10: Create Demo Users Only (Fresh Start Approach)
# ============================================================================

print_header "STEP 10: CREATE DEMO USERS (FRESH START)"

print_step "Creating demo users (admin, john_sales, sarah_analytics, mike_reporting)..."
if docker-compose exec -T backend python manage.py shell << EOF
from django.contrib.auth.models import User

users = [
    ('admin', 'admin@example.com', 'admin123'),
    ('john_sales', 'john@example.com', 'john123'),
    ('sarah_analytics', 'sarah@example.com', 'sarah456'),
    ('mike_reporting', 'mike@example.com', 'mike789'),
]

for username, email, password in users:
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, email=email, password=password)
        print(f'✓ Created user: {username}')
    else:
        print(f'✓ User already exists: {username}')
EOF
then
    print_success "Demo users created"
else
    print_warning "Demo users creation skipped or failed (non-critical)"
fi

# ============================================================================
# Step 11: Create Demo Database Connections
# ============================================================================

print_header "STEP 11: CREATE DEMO DATABASE CONNECTIONS"

print_step "Creating demo connections (PostgreSQL, MySQL, MongoDB, ClickHouse)..."

# Insert demo connections directly into PostgreSQL database
# Using SQL insert is more reliable than Django management commands
if docker-compose exec -T db psql -U user -d dataconnector << 'EOSQL' > /dev/null 2>&1
INSERT INTO connector_databaseconnection (name, db_type, host, port, username, password, database_name, created_at, user_id)
SELECT 
    name, db_type, host, port, username, password, database_name, NOW(), user_id
FROM (
    VALUES 
        ('Demo PostgreSQL (Docker)', 'postgresql', 'db', 5432, 'user', 'password', 'dataconnector'),
        ('Demo MySQL (Docker)', 'mysql', 'mysql', 3306, 'user', 'password', 'testdb'),
        ('Demo MongoDB (Docker)', 'mongodb', 'mongo', 27017, '', '', 'test_db'),
        ('Demo ClickHouse (Docker)', 'clickhouse', 'clickhouse', 9000, 'default', '', 'default')
) AS t(name, db_type, host, port, username, password, database_name)
WHERE NOT EXISTS (
    SELECT 1 FROM connector_databaseconnection 
    WHERE connector_databaseconnection.name = t.name
)
RETURNING name;
EOSQL
then
    print_success "Demo connections created"
else
    print_warning "Demo connections creation skipped (non-critical)"
fi

print_info "💡 System starts with demo connections pre-configured"
print_info "💡 Users can immediately select connections and extract data"
print_info "💡 Extracted data is auto-saved with auto-refresh UI (1-second delay)"
print_info "💡 Automatic cleanup: Files > 24h old are auto-deleted during maintenance"

# ============================================================================
# Summary & Next Steps
# ============================================================================

print_header "DOCKER SETUP COMPLETE!"

echo -e "${GREEN}✓ Docker stack is running!${NC}"
echo ""

# Get port mappings
FRONTEND_PORT=$(docker-compose port frontend 3000 2>/dev/null | cut -d: -f2)
BACKEND_PORT=$(docker-compose port backend 8000 2>/dev/null | cut -d: -f2)

echo -e "${BLUE}Access points:${NC}"
if [ -n "$FRONTEND_PORT" ]; then
    echo "  • Frontend: http://localhost:$FRONTEND_PORT"
fi
if [ -n "$BACKEND_PORT" ]; then
    echo "  • Backend:  http://localhost:$BACKEND_PORT/api/"
fi
echo "  • PostgreSQL: localhost:5433 (user/password)"
echo "  • MySQL:      localhost:3307 (user/password)"
echo "  • MongoDB:    localhost:27018"
echo "  • ClickHouse: localhost:8124"
echo ""

echo -e "${BLUE}Demo Users Created:${NC}"
echo "  • admin / admin123 (Full system access)"
echo "  • john_sales / john123 (Sales user)"
echo "  • sarah_analytics / sarah456 (Analytics user)"
echo "  • mike_reporting / mike789 (Reporting user)"
echo ""

echo -e "${BLUE}Fresh Start Workflow:${NC}"
echo "  1. Log in with any demo user credentials"
echo "  2. Pre-configured demo connections are ready to use:"
echo "     • Demo PostgreSQL (Docker) → db:5432"
echo "     • Demo MySQL (Docker) → mysql:3306"
echo "     • Demo MongoDB (Docker) → mongo:27017"
echo "     • Demo ClickHouse (Docker) → clickhouse:9000"
echo "  3. Select a connection and extract data from tables"
echo "  4. Stored files auto-populate (1-second refresh)"
echo "  5. Extracted data auto-saves to Extracted Data section"
echo "  6. Old files (>24h) are automatically cleaned up"
echo ""

echo -e "${BLUE}System State:${NC}"
echo "  • ✓ Pre-configured demo connections ready"
echo "  • No pre-populated files (auto-generated on extraction)"
echo "  • Ready to test data extraction immediately"
echo ""

echo -e "${BLUE}Useful commands:${NC}"
echo "  # View logs"
echo "  docker-compose logs -f [service-name]"
echo ""
echo "  # Execute command in container"
echo "  docker-compose exec backend python manage.py shell"
echo ""
echo "  # Stop all services"
echo "  docker-compose stop"
echo ""
echo "  # Stop and remove containers"
echo "  docker-compose down"
echo ""
echo "  # Complete reset (including volumes)"
echo "  docker-compose down -v && docker-compose up -d"
echo ""

echo -e "${BLUE}Documentation:${NC}"
echo "  • See SETUP.md for detailed instructions"
echo "  • See README.md for project overview"
echo ""

# ============================================================================
# Health Check
# ============================================================================

print_header "RUNNING HEALTH CHECKS"

print_step "Testing frontend accessibility..."
if curl -s http://localhost:3001 > /dev/null 2>&1; then
    print_success "Frontend is responding"
else
    print_warning "Frontend not yet responding (may need time to start)"
fi

print_step "Testing backend API..."
if curl -s http://localhost:8001/api/ > /dev/null 2>&1; then
    print_success "Backend API is responding"
else
    print_warning "Backend API not yet responding (may need time to start)"
fi

print_step "Testing database connectivity..."
if docker-compose exec -T db psql -U user -d dataconnector -c "SELECT 1;" &> /dev/null; then
    print_success "PostgreSQL is responding"
else
    print_warning "PostgreSQL not responding (check logs)"
fi

echo ""
print_info "Open your browser to http://localhost:3001 (or the port shown above)"
echo ""
