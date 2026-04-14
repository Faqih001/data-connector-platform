#!/bin/bash
# Data Connector Platform - Automated Setup Script
# Runs all necessary setup steps for the project

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Data Connector Platform - Complete Setup Script              ║"
echo "║   This will install dependencies and set up demo data          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"
BACKEND_DIR="$PROJECT_ROOT/backend"

echo -e "${BLUE}Project directory: $PROJECT_ROOT${NC}\n"

# Step 1: Check prerequisites
echo -e "${BLUE}Step 1: Checking Prerequisites...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found: $(node -v)${NC}"

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}✗ Python is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found: $(python3 --version 2>/dev/null || python --version)${NC}"
echo ""

# Step 2: Install Node dependencies
echo -e "${BLUE}Step 2: Installing Node.js Dependencies...${NC}"
if [ ! -d "$PROJECT_ROOT/node_modules" ]; then
    cd "$PROJECT_ROOT"
    npm install
    echo -e "${GREEN}✓ Node dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Node dependencies already installed${NC}"
fi
echo ""

# Step 3: Setup Python virtual environment
echo -e "${BLUE}Step 3: Setting up Python Virtual Environment...${NC}"
cd "$BACKEND_DIR"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv 2>/dev/null || python -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source .venv/bin/activate 2>/dev/null || . .venv/Scripts/activate

echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Step 4: Install Python dependencies
echo -e "${BLUE}Step 4: Installing Python Dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"
echo ""

# Step 5: Run Django migrations
echo -e "${BLUE}Step 5: Running Database Migrations...${NC}"
python manage.py migrate --noinput
echo -e "${GREEN}✓ Database migrations completed${NC}"
echo ""

# Step 6: Create admin user
echo -e "${BLUE}Step 6: Setting up Admin User...${NC}"
python reset_admin.py
echo -e "${GREEN}✓ Admin user configured${NC}"
echo ""

# Step 7: Setup demo users
echo -e "${BLUE}Step 7: Creating Demo Users...${NC}"
python setup_demo_users.py
echo -e "${GREEN}✓ Demo users created${NC}"
echo ""

# Step 8: Populate demo data (optional)
echo -e "${BLUE}Step 8: Populating Demo Data...${NC}"
if [ -f "populate_demo_data.py" ]; then
    python populate_demo_data.py
    echo -e "${GREEN}✓ Demo data populated${NC}"
else
    echo -e "${YELLOW}⚠ Demo data script not found, skipping${NC}"
fi
echo ""

# Summary
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✓ Setup Complete!                                           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo -e "1. ${YELLOW}Start the backend:${NC}"
echo -e "   cd $BACKEND_DIR"
echo -e "   source .venv/bin/activate  # Linux/macOS"
echo -e "   python manage.py runserver 0.0.0.0:8001"
echo ""
echo -e "2. ${YELLOW}Start the frontend (in a new terminal):${NC}"
echo -e "   cd $PROJECT_ROOT"
echo -e "   npm run dev"
echo ""
echo -e "3. ${YELLOW}Open your browser:${NC}"
echo -e "   http://localhost:3000"
echo ""
echo -e "${BLUE}Demo Credentials:${NC}"
echo -e "   👤 ${YELLOW}admin${NC} / ${YELLOW}admin123${NC} (Admin Account)"
echo -e "   👤 ${YELLOW}john_sales${NC} / ${YELLOW}john123${NC}"
echo -e "   👤 ${YELLOW}sarah_analytics${NC} / ${YELLOW}sarah456${NC}"
echo -e "   👤 ${YELLOW}mike_reporting${NC} / ${YELLOW}mike789${NC}"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
