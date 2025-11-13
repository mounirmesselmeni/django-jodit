# Django-Jodit Example Project

This is a complete example Django project demonstrating the django-jodit package integration.

## Features Demonstrated

- ✅ RichTextField in Django models
- ✅ Django admin integration
- ✅ Custom forms with Jodit editor
- ✅ Multiple editor configurations
- ✅ Frontend display of rich text content

## Quick Start

### 1. Install Dependencies

```bash
cd example_project
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Load Sample Data (Optional)

```bash
python manage.py loaddata sample_data.json
```

### 4. Run Development Server

```bash
python manage.py runserver
```

### 5. Access the Application

- **Frontend**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Create Post**: http://127.0.0.1:8000/create/

## What's Inside

### Models (`blog/models.py`)

```python
from jodit.fields import RichTextField

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()  # Full-featured editor
    excerpt = RichTextField(config_name='simple')  # Simple editor
```

### Views (`blog/views.py`)

- List view showing all blog posts
- Detail view for individual posts
- Create view with form using Jodit editor

### Templates

- `base.html` - Base template with Bootstrap
- `post_list.html` - List of all posts
- `post_detail.html` - Individual post display
- `post_form.html` - Create/edit post form

### Admin (`blog/admin.py`)

Django admin configuration with Jodit editor automatically applied to RichTextField fields.

## Configuration

See `example_project/settings.py` for Jodit configuration examples:

```python
JODIT_CONFIGS = {
    'default': {
        'height': 400,
        'buttons': [...],  # Full toolbar
    },
    'simple': {
        'height': 200,
        'buttons': ['bold', 'italic', 'underline', 'link'],  # Minimal toolbar
    },
}
```

## Screenshots

### Admin Interface
The Jodit editor automatically appears in Django admin for RichTextField fields.

### Create Post Form
Custom form view with Jodit editor for content creation.

### Post Display
Rich text content rendered with proper HTML formatting.

## Project Structure

```
example_project/
├── blog/                      # Blog application
│   ├── models.py             # Post model with RichTextField
│   ├── views.py              # Views for list/detail/create
│   ├── forms.py              # Form with RichTextFormField
│   ├── admin.py              # Admin configuration
│   └── templates/            # HTML templates
├── example_project/          # Project settings
│   ├── settings.py           # Django settings with JODIT_CONFIGS
│   ├── urls.py               # URL configuration
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

## Try It Out

1. **Create a new post** via the admin panel at `/admin/blog/post/add/`
2. **Use the Jodit editor** to create rich text content with:
   - Text formatting (bold, italic, underline)
   - Lists (ordered and unordered)
   - Links and images
   - Tables
   - Code blocks
3. **View the post** on the frontend to see the rendered content

## Notes

- The `content` field uses the 'default' configuration with full toolbar
- The `excerpt` field uses the 'simple' configuration with minimal toolbar
- You can customize configurations in `settings.py`
- Static files are served automatically in development mode
