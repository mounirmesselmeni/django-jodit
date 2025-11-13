"""Default settings for django-jodit."""

from django.conf import settings

# Default Jodit configuration
JODIT_DEFAULT_CONFIG = {
    "height": 400,
    "width": "100%",
    "toolbar": True,
    "spellcheck": True,
    "language": "auto",
}


def get_config(config_name="default"):
    """
    Get Jodit configuration by name.

    Args:
        config_name: Name of the configuration to retrieve

    Returns:
        Dictionary with Jodit configuration
    """
    configs = getattr(settings, "JODIT_CONFIGS", {})
    return configs.get(config_name, JODIT_DEFAULT_CONFIG)
