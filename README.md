# django-jodit

[![PyPI version](https://badge.fury.io/py/django-jodit.svg)](https://badge.fury.io/py/django-jodit)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-4.2%2B-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/mounirmesselmeni/django-jodit/workflows/Tests/badge.svg)](https://github.com/mounirmesselmeni/django-jodit/actions)
[![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen.svg)](https://github.com/mounirmesselmeni/django-jodit)

A Django app to easily integrate the [Jodit WYSIWYG editor](https://xdsoft.net/jodit/) into Django forms and admin.

## 🎥 Live Demo

Check out the [example project](./example_project/) to see django-jodit in action!

## Features

- 🎨 Full-featured WYSIWYG editor with Jodit
- 📝 Easy integration with Django forms and admin
- ⚙️ Highly configurable through Django settings
- 🎯 Model field and form field support
- 📦 Includes all necessary static files (CSS/JS)
- 🔧 Custom configuration per field
- 🌐 Multi-language support

## Installation

### From PyPI (Recommended)

```bash
pip install django-jodit
uv add jodit
```

### From Source

```bash
pip install git+https://github.com/mounirmesselmeni/django-jodit.git
```

### Local Development

```bash
git clone https://github.com/mounirmesselmeni/django-jodit.git
cd django-jodit
pip install -e .
```

## Quick Start

### 1. Add to INSTALLED_APPS

Add `'jodit'` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'jodit',
    ...
]
```

### 2. Configure (Optional)

Add custom Jodit configurations to your `settings.py`:

```python
JODIT_CONFIGS = {
    'default': {
        'height': 400,
        'width': '100%',
        'toolbar': True,
        'buttons': [
            'source', '|',
            'bold', 'italic', 'underline', '|',
            'ul', 'ol', '|',
            'font', 'fontsize', 'brush', 'paragraph', '|',
            'image', 'table', 'link', '|',
            'align', 'undo', 'redo', '|',
            'hr', 'eraser', 'fullsize',
        ],
    },
    'simple': {
        'height': 200,
        'toolbar': True,
        'buttons': ['bold', 'italic', 'underline', 'link'],
    },
}
```

## Usage

### In Models

```python
from django.db import models
from jodit.fields import RichTextField

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()  # Uses 'default' config
    summary = RichTextField(config_name='simple')  # Uses 'simple' config
```

### In Forms

```python
from django import forms
from jodit.fields import RichTextFormField

class ArticleForm(forms.Form):
    content = RichTextFormField()
    summary = RichTextFormField(config_name='simple')
```

### In Admin

The widget will automatically be used in the Django admin for `RichTextField` fields:

```python
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title']
```

### Using the Widget Directly

```python
from django import forms
from jodit.widgets import JoditWidget

class MyForm(forms.Form):
    content = forms.CharField(widget=JoditWidget(config_name='default'))
```

## Dark Theme Support 🌙

Django-Jodit automatically detects and supports dark mode!

### Auto-Detection

By default, the editor automatically detects:

- ✅ Django admin dark mode (`data-theme="dark"`)
- ✅ Custom dark mode classes

### Configuration

```python
JODIT_CONFIGS = {
    'default': {
        'theme': 'auto',  # Auto-detect (default)
    },
    'dark': {
        'theme': 'dark',  # Force dark theme
    },
    'light': {
        'theme': 'default',  # Force light theme
    },
}
```

The editor dynamically updates when you switch themes in Django admin!

## Custom Jodit Versions 📦

Use different Jodit versions by specifying custom URLs:

### Use CDN

```python
# settings.py

# Use specific version
JODIT_JS_URL = 'https://unpkg.com/jodit@4.7.9/es2021/jodit.min.js'
JODIT_CSS_URL = 'https://unpkg.com/jodit@4.7.9/es2021/jodit.min.css'

# Or use latest (not recommended for production)
JODIT_JS_URL = 'https://unpkg.com/jodit@latest/es2021/jodit.min.js'
JODIT_CSS_URL = 'https://unpkg.com/jodit@latest/es2021/jodit.min.css'
```

### Use Local Custom Files

```python
# settings.py
JODIT_JS_URL = '/static/custom/jodit.min.js'
JODIT_CSS_URL = '/static/custom/jodit.min.css'
```

### Use Bundled Version (Default)

```python
# No configuration needed - uses bundled Jodit 4.7.9
# Or explicitly set to None
JODIT_JS_URL = None
JODIT_CSS_URL = None
```

## Configuration Options

The Jodit editor supports many configuration options. Here are some common ones:

```python
JODIT_CONFIGS = {
    'default': {
        # Editor dimensions
        'height': 400,
        'width': '100%',

        # Toolbar settings
        'toolbar': True,
        'toolbarButtonSize': 'middle',  # small, middle, large
        'toolbarAdaptive': True,

        # Editor behavior
        'spellcheck': True,
        'language': 'auto',  # or specific language code
        'askBeforePasteHTML': True,
        'askBeforePasteFromWord': True,

        # UI elements
        'showCharsCounter': True,
        'showWordsCounter': True,
        'showXPathInStatusbar': False,

        # Image handling
        'uploader': {
            'insertImageAsBase64URI': True,
        },

        # Custom buttons
        'buttons': [
            'source', '|',
            'bold', 'italic', 'underline', 'strikethrough', '|',
            'ul', 'ol', '|',
            'outdent', 'indent', '|',
            'font', 'fontsize', 'brush', 'paragraph', '|',
            'image', 'table', 'link', '|',
            'align', 'undo', 'redo', '|',
            'hr', 'eraser', 'copyformat', '|',
            'symbol', 'fullsize', 'print',
        ],
        'removeButtons': [],  # List of buttons to remove
    },
}
```

For a complete list of configuration options, see the [Jodit documentation](https://xdsoft.net/jodit/docs/).

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/mounirmesselmeni/django-jodit.git
cd django-jodit

# Install dependencies
uv sync --dev
```

### Running Tests

```bash
# Run tests with coverage
uv run python manage.py test jodit

# Or with coverage report
uv run coverage run --source='jodit' manage.py test jodit
uv run coverage report
uv run coverage html  # Generate HTML report
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Install pre-commit hooks
uv run pre-commit install
```

## Project Structure

```
django-jodit/
├── jodit/
│   ├── __init__.py
│   ├── apps.py
│   ├── configs.py          # Default Jodit configurations
│   ├── fields.py           # RichTextField and RichTextFormField
│   ├── models.py
│   ├── settings.py         # Settings utilities
│   ├── widgets.py          # JoditWidget
│   ├── tests.py            # Test suite
│   ├── testsettings.py     # Test Django settings
│   ├── static/
│   │   └── jodit/
│   │       ├── jodit.min.js
│   │       ├── jodit.min.css
│   │       └── jodit-init.js
│   └── templates/
│       └── jodit/
│           └── widget.html
├── LICENSE
├── MANIFEST.in
├── README.md
├── manage.py
└── pyproject.toml
```

## Screenshots

### Django Admin Integration

The Jodit editor seamlessly integrates with Django admin, providing rich text editing capabilities out of the box.

### Custom Forms

Use Jodit in your custom forms with full control over configuration and styling.

### Multiple Configurations

Different editor configurations for different use cases - full-featured editor for main content, simple editor for excerpts and comments.

## Example Project

A complete example project is included in the [`example_project/`](./example_project/) directory. It demonstrates:

- ✅ Blog application with posts and comments
- ✅ Django admin integration
- ✅ Multiple editor configurations
- ✅ Frontend forms with Jodit
- ✅ Rich text content display

### Running the Example

```bash
cd example_project
./setup.sh
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see it in action!

## Jodit Version

This package includes Jodit Editor version **4.7.9**.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- [Jodit Editor](https://xdsoft.net/jodit/)

## Changelog

### 0.1.1 (2026-08-27)

- Update dependencies to support Django 6.1 and Python 3.14
- Drop support for Django < 5.2
- Upgrade jodit to v4.13.9

### 0.1.0 (2025-11-13)

- Initial release
- Basic Jodit editor integration (v4.7.9)
- Model field and form field support
- Django admin integration
- Configurable through Django settings
- Comprehensive test suite (96% coverage)
- Example project with blog application
- GitHub Actions CI/CD with PyPI publishing
