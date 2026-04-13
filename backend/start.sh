#!/bin/bash
# Helper script to run Django server from project root

cd "$(dirname "$0")"  # Change to backend directory

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Run the server
python manage.py runserver 0.0.0.0:8000
