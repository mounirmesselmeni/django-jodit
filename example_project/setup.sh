#!/bin/bash
# Setup script for django-jodit example project

set -e

echo "🚀 Setting up Django-Jodit Example Project..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source .venv/bin/activate

# Install django-jodit from parent directory
echo "📥 Installing django-jodit from parent directory..."
pip install -e ..

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Run migrations
echo "🔧 Running migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser
echo ""
echo "👤 Create a superuser account for Django admin:"
python manage.py createsuperuser

# Load sample data
echo ""
echo "📊 Loading sample data..."
python manage.py loaddata sample_data.json || echo "⚠️  Sample data not found, skipping..."

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 You can now run the development server:"
echo "   python manage.py runserver"
echo ""
echo "📱 Access the application at:"
echo "   Frontend: http://127.0.0.1:8000/"
echo "   Admin: http://127.0.0.1:8000/admin/"
echo ""
