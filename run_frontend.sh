#!/bin/bash

# Find available port in range
find_available_port() {
    local start_port=$1
    local end_port=$2
    
    for port in $(seq $start_port $end_port); do
        if ! lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo $port
            return 0
        fi
    done
    
    # If no port available, use start_port anyway
    echo $start_port
    return 1
}

# Frontend server with port range 3000-3009
FRONTEND_PORT=$(find_available_port 3000 3009)
echo "Starting Next.js frontend on port $FRONTEND_PORT..."
exec npm run dev -- -p $FRONTEND_PORT
