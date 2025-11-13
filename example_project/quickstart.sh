#!/bin/bash
# Quick start script - runs the example project without full setup

set -e

echo "🚀 Quick Start - Django-Jodit Example Project"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Running full setup..."
    ./setup.sh
    exit 0
fi

# Activate virtual environment
source .venv/bin/activate

# Check if database exists
if [ ! -f "db.sqlite3" ]; then
    echo "📊 Database not found. Creating database..."
    python manage.py migrate
    
    # Load sample data
    echo "📊 Loading sample data..."
    python manage.py loaddata sample_data.json
    
    echo ""
    echo "⚠️  No superuser created. To access admin, run:"
    echo "   python manage.py createsuperuser"
fi

echo ""
echo "🎉 Starting development server..."
echo ""
echo "📱 Access the application at:"
echo "   Frontend: http://127.0.0.1:8000/"
echo "   Admin: http://127.0.0.1:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
