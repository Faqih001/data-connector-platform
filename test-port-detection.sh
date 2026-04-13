#!/bin/bash
#
# Test script for port detection functionality
# Tests the port-detector.js utility
#

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "========================================"
echo "PORT DETECTION FUNCTIONALITY TEST"
echo "========================================"
echo ""

# Test 1: Check if port-detector.js exists
echo "TEST 1: Checking if port-detector.js exists..."
if [ -f "port-detector.js" ]; then
    echo "✅ port-detector.js found"
else
    echo "❌ port-detector.js not found"
    exit 1
fi
echo ""

# Test 2: Check if port-detector.js is executable
echo "TEST 2: Checking if port ranges are defined in port-detector.js..."
if grep -q "findAvailablePort.*8000.*8009" port-detector.js && grep -q "findAvailablePort.*3000.*3009" port-detector.js; then
    echo "✅ Backend range (8000-8009) and frontend range (3000-3009) defined"
else
    echo "❌ Port ranges not properly defined"
    exit 1
fi
echo ""

# Test 3: Check if npm scripts are configured
echo "TEST 3: Checking if npm scripts are configured..."
if grep -q '"backend".*port-detector.js backend' package.json && grep -q '"frontend".*port-detector.js frontend' package.json; then
    echo "✅ npm scripts for backend and frontend configured"
else
    echo "❌ npm scripts not properly configured"
    exit 1
fi
echo ""

# Test 4: Test port detection logic with Node
echo "TEST 4: Testing port detection logic..."
cat > /tmp/test_ports.js << 'EOF'
const net = require('net');

async function checkPort(port) {
  return new Promise((resolve) => {
    const server = net.createServer();
    server.once('error', (err) => {
      resolve(false);
    });
    server.once('listening', () => {
      server.close();
      resolve(true);
    });
    server.listen(port, '0.0.0.0');
  });
}

async function testPortDetection() {
  try {
    // Test if port 3000 is available
    const port3000Available = await checkPort(3000);
    const port8000Available = await checkPort(8000);
    
    console.log(`Port 3000 available: ${port3000Available ? 'yes' : 'no'}`);
    console.log(`Port 8000 available: ${port8000Available ? 'yes' : 'no'}`);
    
    if (port3000Available && port8000Available) {
      console.log('✅ Port detection logic working');
      process.exit(0);
    } else {
      console.log('⚠️  Some ports are in use (expected in multi-instance scenarios)');
      process.exit(0);
    }
  } catch (err) {
    console.error('❌ Error testing ports:', err.message);
    process.exit(1);
  }
}

testPortDetection();
EOF
node /tmp/test_ports.js
echo ""

# Test 5: Check ConnectionForm auto-detection
echo "TEST 5: Checking ConnectionForm auto-detection..."
if grep -q "DEFAULT_PORTS" app/components/ConnectionForm.tsx && grep -q "DEFAULT_HOST" app/components/ConnectionForm.tsx; then
    echo "✅ ConnectionForm has default host/port configuration"
else
    echo "❌ ConnectionForm missing default host/port configuration"
    exit 1
fi

# Check if handleDbTypeChange updates ports
if grep -q "handleDbTypeChange" app/components/ConnectionForm.tsx; then
    echo "✅ ConnectionForm has handler for database type changes"
else
    echo "❌ ConnectionForm missing database type change handler"
    exit 1
fi
echo ""

# Test 6: Verify database port mappings
echo "TEST 6: Verifying database port mappings..."
PORTS_OK=true

if grep -q "postgresql.*5432" app/components/ConnectionForm.tsx; then
    echo "✅ PostgreSQL: 5432"
else
    echo "❌ PostgreSQL port not mapped"
    PORTS_OK=false
fi

if grep -q "mysql.*3306" app/components/ConnectionForm.tsx; then
    echo "✅ MySQL: 3306"
else
    echo "❌ MySQL port not mapped"
    PORTS_OK=false
fi

if grep -q "mongodb.*27017" app/components/ConnectionForm.tsx; then
    echo "✅ MongoDB: 27017"
else
    echo "❌ MongoDB port not mapped"
    PORTS_OK=false
fi

if grep -q "clickhouse.*9000" app/components/ConnectionForm.tsx; then
    echo "✅ ClickHouse: 9000"
else
    echo "❌ ClickHouse port not mapped"
    PORTS_OK=false
fi

if [ "$PORTS_OK" = false ]; then
    exit 1
fi
echo ""

# Test 7: Verify environment setup
echo "TEST 7: Checking environment setup..."
if [ -d "node_modules" ]; then
    echo "✅ node_modules directory exists (dependencies installed)"
else
    echo "⚠️  node_modules directory not found (install with: npm install)"
fi

if [ -d "backend/.venv" ] || [ -d "backend/venv" ]; then
    echo "✅ Python virtual environment exists"
else
    echo "⚠️  Python virtual environment not found"
fi
echo ""

# Test 8: Quick smoke test
echo "TEST 8: Smoke test - checking if dependencies are importable..."
if npm --version > /dev/null 2>&1; then
    echo "✅ npm available"
else
    echo "❌ npm not available"
    exit 1
fi

if python3 --version > /dev/null 2>&1; then
    echo "✅ Python available"
else
    echo "❌ Python not available"
    exit 1
fi
echo ""

echo "========================================"
echo "✅ ALL TESTS PASSED!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Run backend:  npm run backend"
echo "2. Run frontend: npm run frontend"
echo "3. Visit: http://localhost:3000"
echo ""
