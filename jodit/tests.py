"""Tests for django-jodit."""

import json

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.test import TestCase, override_settings

from .fields import RichTextField, RichTextFormField
from .widgets import JoditWidget


class TestModel(models.Model):
    """Test model for RichTextField."""

    content = RichTextField()
    custom_content = RichTextField(config_name="simple")

    class Meta:
        app_label = "jodit"

    def __str__(self):
        return self.content or ""


class JoditWidgetTestCase(TestCase):
    """Test cases for JoditWidget."""

    def test_widget_initialization_default(self):
        """Test widget initialization with default config."""
        widget = JoditWidget()
        self.assertEqual(widget.config_name, "default")
        self.assertIn("height", widget.config)
        self.assertIn("width", widget.config)

    def test_widget_initialization_custom_config(self):
        """Test widget initialization with custom config name."""
        widget = JoditWidget(config_name="simple")
        self.assertEqual(widget.config_name, "simple")
        # Should have the simple config from testsettings
        self.assertEqual(widget.config["height"], 200)
        self.assertFalse(widget.config["toolbar"])

    def test_widget_media(self):
        """Test that widget includes correct media files."""
        widget = JoditWidget()
        media = widget.media

        # Check CSS files
        css_files = media._css.get("all", [])
        self.assertTrue(any("jodit.min.css" in str(f) for f in css_files))

        # Check JS files
        js_files = [str(f) for f in media._js]
        self.assertTrue(any("jodit.min.js" in f for f in js_files))
        self.assertTrue(any("jodit-init.js" in f for f in js_files))

    def test_widget_render(self):
        """Test widget rendering."""
        widget = JoditWidget()
        html = widget.render("content", "Test content", attrs={"id": "id_content"})

        self.assertIn("textarea", html)
        self.assertIn("Test content", html)
        self.assertIn("data-jodit-config", html)
        self.assertIn("django-jodit-widget", html)

    def test_widget_render_with_value(self):
        """Test widget rendering with initial value."""
        widget = JoditWidget()
        html = widget.render("content", "<p>HTML content</p>", attrs={"id": "id_content"})

        # Check that the content is in the textarea (may have HTML escaping)
        self.assertIn("HTML content", html)
        self.assertIn("textarea", html)

    def test_widget_render_config_in_context(self):
        """Test that config is properly passed to template context."""
        widget = JoditWidget(config_name="advanced")
        context = widget.get_context("content", "", {"id": "id_content"})

        config_json = context["widget"]["config"]
        config = json.loads(config_json)

        self.assertIn("buttons", config)
        self.assertEqual(config["height"], 600)

    @override_settings(JODIT_CONFIGS={"invalid": "not_a_dict"})
    def test_widget_invalid_config_type(self):
        """Test that invalid config type raises ImproperlyConfigured."""
        with self.assertRaises(ImproperlyConfigured):
            JoditWidget(config_name="invalid")

    @override_settings(JODIT_CONFIGS="not_a_dict")
    def test_widget_invalid_configs_setting(self):
        """Test that invalid JODIT_CONFIGS setting raises ImproperlyConfigured."""
        with self.assertRaises(ImproperlyConfigured):
            JoditWidget()

    def test_widget_nonexistent_config(self):
        """Test that nonexistent config name raises ImproperlyConfigured."""
        with self.assertRaises(ImproperlyConfigured):
            JoditWidget(config_name="nonexistent")


class RichTextFormFieldTestCase(TestCase):
    """Test cases for RichTextFormField."""

    def test_form_field_initialization(self):
        """Test form field initialization."""
        field = RichTextFormField()
        self.assertIsInstance(field.widget, JoditWidget)

    def test_form_field_with_config(self):
        """Test form field with custom config."""
        field = RichTextFormField(config_name="simple")
        self.assertEqual(field.widget.config_name, "simple")

    def test_form_field_in_form(self):
        """Test form field usage in a Django form."""

        class TestForm(forms.Form):
            content = RichTextFormField()

        form = TestForm()
        self.assertIn("content", form.fields)
        self.assertIsInstance(form.fields["content"].widget, JoditWidget)

    def test_form_field_validation(self):
        """Test form field validation."""

        class TestForm(forms.Form):
            content = RichTextFormField(required=True)

        # Test with empty data
        form = TestForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

        # Test with valid data
        form = TestForm(data={"content": "<p>Test</p>"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["content"], "<p>Test</p>")


class RichTextFieldTestCase(TestCase):
    """Test cases for RichTextField model field."""

    def test_model_field_initialization(self):
        """Test model field initialization."""
        field = RichTextField()
        self.assertEqual(field.config_name, "default")

    def test_model_field_with_config(self):
        """Test model field with custom config."""
        field = RichTextField(config_name="simple")
        self.assertEqual(field.config_name, "simple")

    def test_model_field_formfield(self):
        """Test that model field returns correct form field."""
        field = RichTextField()
        form_field = field.formfield()

        self.assertIsInstance(form_field, RichTextFormField)
        self.assertIsInstance(form_field.widget, JoditWidget)

    def test_model_field_formfield_with_config(self):
        """Test that model field passes config to form field."""
        field = RichTextField(config_name="advanced")
        form_field = field.formfield()

        self.assertEqual(form_field.widget.config_name, "advanced")
        self.assertEqual(form_field.widget.config["height"], 600)


class IntegrationTestCase(TestCase):
    """Integration tests for django-jodit."""

    def test_model_form_integration(self):
        """Test integration with Django ModelForm."""

        class TestModelForm(forms.ModelForm):
            class Meta:
                model = TestModel
                fields = ["content", "custom_content"]

        form = TestModelForm()

        # Both fields should have JoditWidget
        self.assertIsInstance(form.fields["content"].widget, JoditWidget)
        self.assertIsInstance(form.fields["custom_content"].widget, JoditWidget)

        # Check config names
        self.assertEqual(form.fields["content"].widget.config_name, "default")
        self.assertEqual(form.fields["custom_content"].widget.config_name, "simple")

    def test_widget_rendering_in_form(self):
        """Test widget rendering within a form."""

        class TestForm(forms.Form):
            content = RichTextFormField()

        form = TestForm()
        html = str(form)

        self.assertIn("textarea", html)
        self.assertIn("data-jodit-config", html)
        self.assertIn("django-jodit-widget", html)

    def test_form_submission(self):
        """Test form submission with rich text content."""

        class TestForm(forms.Form):
            content = RichTextFormField()

        html_content = (
            "<h1>Test Heading</h1><p>This is a <strong>test</strong> paragraph with <em>formatting</em>."
            "</p><ul><li>Item 1</li><li>Item 2</li></ul>"
        )

        form = TestForm(data={"content": html_content})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["content"], html_content)


class ConfigTestCase(TestCase):
    """Test cases for configuration handling."""

    def test_default_config_loaded(self):
        """Test that default config is loaded correctly."""
        widget = JoditWidget()
        self.assertIsNotNone(widget.config)
        self.assertIsInstance(widget.config, dict)

    def test_custom_config_override(self):
        """Test that custom config overrides defaults."""
        widget = JoditWidget(config_name="advanced")

        # Custom config should override defaults
        self.assertEqual(widget.config["height"], 600)
        self.assertIn("buttons", widget.config)

    def test_config_merge(self):
        """Test that custom config is merged with defaults."""
        widget = JoditWidget(config_name="simple")

        # Should have custom settings
        self.assertEqual(widget.config["height"], 200)
        # Should still have defaults not overridden
        self.assertIn("width", widget.config)


class LazyEncoderTestCase(TestCase):
    """Test cases for LazyEncoder."""

    def test_lazy_encoder_with_lazy_string(self):
        """Test that LazyEncoder handles lazy translation strings."""
        from django.utils.translation import gettext_lazy as _

        from .widgets import LazyEncoder

        lazy_string = _("Test String")
        encoder = LazyEncoder()
        result = encoder.encode({"message": lazy_string})

        # Should encode without errors
        self.assertIsInstance(result, str)
        self.assertIn("Test String", result)

    def test_lazy_encoder_with_regular_data(self):
        """Test that LazyEncoder handles regular data."""
        from .widgets import LazyEncoder

        data = {"key": "value", "number": 123}
        encoder = LazyEncoder()
        result = encoder.encode(data)

        # Should encode normally
        decoded = json.loads(result)
        self.assertEqual(decoded["key"], "value")
        self.assertEqual(decoded["number"], 123)

    def test_json_encode_function(self):
        """Test json_encode helper function."""
        from django.utils.translation import gettext_lazy as _

        from .widgets import json_encode

        data = {"test": "data", "lazy": _("Lazy String")}
        result = json_encode(data)

        # Should return JSON string
        self.assertIsInstance(result, str)
        decoded = json.loads(result)
        self.assertEqual(decoded["test"], "data")


class SettingsTestCase(TestCase):
    """Test cases for settings utilities."""

    def test_get_config_default(self):
        """Test get_config with default config."""
        from .settings import get_config

        config = get_config("default")
        self.assertIsInstance(config, dict)
        self.assertIn("height", config)

    def test_get_config_custom(self):
        """Test get_config with custom config."""
        from .settings import get_config

        config = get_config("simple")
        self.assertIsInstance(config, dict)
        self.assertEqual(config["height"], 200)

    def test_get_config_nonexistent(self):
        """Test get_config with nonexistent config returns default."""
        from .settings import JODIT_DEFAULT_CONFIG, get_config

        config = get_config("nonexistent_config")
        # Should return default config
        self.assertEqual(config, JODIT_DEFAULT_CONFIG)

    @override_settings(JODIT_CONFIGS={})
    def test_get_config_no_configs(self):
        """Test get_config when JODIT_CONFIGS is empty."""
        from .settings import JODIT_DEFAULT_CONFIG, get_config

        config = get_config("default")
        # Should return default config
        self.assertEqual(config, JODIT_DEFAULT_CONFIG)


class PackageMetadataTestCase(TestCase):
    """Test cases for package metadata."""

    def test_package_version(self):
        """Test that package version is set."""
        import jodit

        self.assertIsNotNone(jodit.__version__)
        self.assertIsInstance(jodit.__version__, str)

    def test_package_author(self):
        """Test that package author is set."""
        import jodit

        self.assertEqual(jodit.__author__, "Mounir Messelmeni")

    def test_package_email(self):
        """Test that package email is set."""
        import jodit

        self.assertEqual(jodit.__email__, "messelmeni.mounir@gmail.com")


class CustomJoditVersionTestCase(TestCase):
    """Test cases for custom Jodit version support."""

    @override_settings(
        JODIT_JS_URL='https://cdn.example.com/jodit.js', JODIT_CSS_URL='https://cdn.example.com/jodit.css'
    )
    def test_custom_jodit_urls(self):
        """Test that custom Jodit URLs are used."""
        widget = JoditWidget()
        media = widget.media

        # Check that custom URLs are in media
        js_files = [str(f) for f in media._js]
        css_files = media._css.get('all', [])
        css_files = [str(f) for f in css_files]

        self.assertTrue(any('cdn.example.com/jodit.js' in f for f in js_files))
        self.assertTrue(any('cdn.example.com/jodit.css' in f for f in css_files))

    @override_settings(JODIT_JS_URL=None, JODIT_CSS_URL=None)
    def test_bundled_jodit_urls(self):
        """Test that bundled Jodit URLs are used when custom URLs are None."""
        JoditWidget()
