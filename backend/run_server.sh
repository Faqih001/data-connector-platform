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

# Backend server with port range 8000-8009
BACKEND_PORT=$(find_available_port 8000 8009)
echo "Starting Django backend on port $BACKEND_PORT..."
exec python manage.py runserver "0.0.0.0:$BACKEND_PORT"
