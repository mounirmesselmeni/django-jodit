"""Jodit widget for Django forms."""

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.widgets import Media
from django.templatetags.static import static
from django.utils.encoding import force_str
from django.utils.functional import Promise

from .configs import DEFAULT_CONFIG


class LazyEncoder(DjangoJSONEncoder):
    """JSON encoder that handles Django's lazy translation objects."""

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super().default(obj)


def json_encode(data):
    """Encode data as JSON using LazyEncoder."""
    return LazyEncoder().encode(data)


class JoditWidget(forms.Textarea):
    """
    Widget providing Jodit WYSIWYG editor for rich text editing.

    Supports configuration through settings.JODIT_CONFIGS.

    Example usage:
        widget = JoditWidget(config_name='default')
    """

    def __init__(self, config_name="default", template_name="jodit/widget.html", *args, **kwargs):
        self.template_name = template_name
        super().__init__(*args, **kwargs)

        self.config_name = config_name
        # Setup config from defaults.
        self.config = DEFAULT_CONFIG.copy()

        # Try to get valid config from settings.
        configs = getattr(settings, "JODIT_CONFIGS", None)
        if configs:
            if isinstance(configs, dict):
                # Make sure the config_name exists.
                if self.config_name in configs:
                    config = configs[self.config_name]
                    # Make sure the configuration is a dictionary.
                    if not isinstance(config, dict):
                        raise ImproperlyConfigured(
                            f'JODIT_CONFIGS["{self.config_name}"] setting must be a dictionary type.'
                        )
                    # Override defaults with settings config.
                    self.config.update(config)
                else:
                    raise ImproperlyConfigured(
                        f"No configuration named '{self.config_name}' found in your JODIT_CONFIGS setting."
                    )
            else:
                raise ImproperlyConfigured("JODIT_CONFIGS setting must be a dictionary type.")

    @property
    def media(self):
        """
        Return media files required by Jodit editor.

        Supports custom Jodit paths via settings:
        - JODIT_JS_URL: Custom JavaScript file path/URL
        - JODIT_CSS_URL: Custom CSS file path/URL

        Falls back to bundled static files if not configured.
        """
        # Get custom paths from settings or use defaults
        jodit_js = getattr(settings, 'JODIT_JS_URL', None)
        jodit_css = getattr(settings, 'JODIT_CSS_URL', None)

        # Use custom paths if provided, otherwise use bundled files
        if jodit_js is None:
            jodit_js = static('jodit/jodit.min.js')
        if jodit_css is None:
            jodit_css = static('jodit/jodit.min.css')

        # Always use our initialization script
        jodit_init = static('jodit/jodit-init.js')

        return Media(
            css={"all": [jodit_css]},
            js=[jodit_js, jodit_init],
        )

    def get_context(self, name, value, attrs):
        """Build widget context with Jodit configuration."""
        context = super().get_context(name, value, attrs)
        context["widget"]["config"] = json_encode(self.config)
        return context
