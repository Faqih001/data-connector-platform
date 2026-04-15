#!/bin/bash
# Database Test Runner
# Runs all database connection tests

set -e

cd "$(dirname "$0")/.."
BACKEND_DIR="$PWD/backend"

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║          DATABASE CONNECTION TEST SUITE - ALL 4 DATABASES         ║"
echo "╚════════════════════════════════════════════════════════════════════╝"

source "$BACKEND_DIR/.venv/bin/activate"
cd "$BACKEND_DIR"

echo ""
echo "Running comprehensive all-databases test..."
python ../tests/test_all_databases.py

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                     INDIVIDUAL DATABASE TESTS                      ║"
echo "╚════════════════════════════════════════════════════════════════════╝"

echo ""
echo "Running PostgreSQL test..."
python ../tests/test_postgresql.py

echo ""
echo "Running MySQL test..."
python ../tests/test_mysql.py

echo ""
echo "Running MongoDB test..."
python ../tests/test_mongodb.py

echo ""
echo "Running ClickHouse test..."
python ../tests/test_clickhouse.py

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ ALL TESTS COMPLETED                         ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
