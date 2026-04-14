#!/bin/bash
pkill -9 -f "manage.py runserver" 2>/dev/null || true
sleep 2
cd /home/amir/Desktop/projects/data-connector-platform/backend
.venv/bin/python manage.py runserver 8001 > /tmp/backend.log 2>&1 &
sleep 4 
echo "Backend started with PID $(pgrep -f 'manage.py runserver')"
