#!/bin/bash
# Quick test script for local development

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Testing Django-Jodit Example Project Locally          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the example_project directory"
    exit 1
fi

# Check if parent directory has django-jodit
if [ ! -f "../jodit/__init__.py" ]; then
    echo "❌ Error: django-jodit package not found in parent directory"
    exit 1
fi

echo "✓ Found django-jodit package in parent directory"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install django-jodit in editable mode from parent directory
echo "📥 Installing django-jodit in development mode..."
pip install -e .. > /dev/null 2>&1
echo "✓ django-jodit installed from ../jodit"

# Install Django if not present
echo "📥 Installing Django..."
pip install Django > /dev/null 2>&1
echo "✓ Django installed"

# Verify imports
echo "🔍 Verifying django-jodit installation..."
python -c "
import jodit
from jodit.widgets import JoditWidget
from jodit.fields import RichTextField, RichTextFormField
print('✓ All imports successful')
print(f'✓ Version: {jodit.__version__}')
" || {
    echo "❌ Failed to import django-jodit"
    exit 1
}

# Check if database exists
if [ ! -f "db.sqlite3" ]; then
    echo ""
    echo "🔧 Setting up database..."
    python manage.py migrate > /dev/null 2>&1
    echo "✓ Database created"

    echo ""
    echo "📊 Loading sample data..."
    python manage.py loaddata sample_data.json > /dev/null 2>&1
    echo "✓ Sample data loaded (3 posts, 3 comments)"

    echo ""
    echo "👤 Creating superuser..."
    echo "   (You can skip this and create it later with: python manage.py createsuperuser)"
    python manage.py createsuperuser || echo "⚠️  Skipped superuser creation"
else
    echo "✓ Database exists"
fi

# Run Django checks
echo ""
echo "🔍 Running Django system checks..."
python manage.py check > /dev/null 2>&1
echo "✓ No issues found"

# Show what's in the database
echo ""
echo "📊 Database contents:"
python manage.py shell -c "
from blog.models import Post, Comment
posts = Post.objects.count()
comments = Comment.objects.count()
print(f'   Posts: {posts}')
print(f'   Comments: {comments}')
"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  ✅ Setup Complete!                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 What to test:"
echo ""
echo "1️⃣  Admin Interface (Full Jodit editor):"
echo "   http://127.0.0.1:8080/admin/"
echo "   → Login and create/edit blog posts"
echo ""
echo "2️⃣  Frontend Form (Custom form with Jodit):"
echo "   http://127.0.0.1:8080/create/"
echo "   → Create a post using the frontend form"
echo ""
echo "3️⃣  Post List (View all posts):"
echo "   http://127.0.0.1:8080/"
echo "   → See formatted content display"
echo ""
echo "4️⃣  Post Detail (View & comment):"
echo "   http://127.0.0.1:8080/post/welcome-to-django-jodit/"
echo "   → Add comments with simple Jodit editor"
echo ""
echo "📝 Editor Configurations:"
echo "   • Content field: Full editor (all features)"
echo "   • Excerpt field: Simple editor (basic formatting)"
echo "   • Comments: Simple editor"
echo ""
echo "🔧 Development Mode:"
echo "   Changes to ../jodit/ will be reflected immediately"
echo "   (no need to reinstall the package)"
echo ""
echo "🚀 Starting development server..."
echo "   Press Ctrl+C to stop"
echo ""

# Run the development server
python manage.py runserver 0.0.0.0:8080
