"""Jodit form and model fields for Django."""

from django import forms
from django.db import models

from jodit.widgets import JoditWidget


class RichTextField(models.TextField):
    """
    A TextField that uses JoditWidget for form representation.

    Example usage in models:
        content = RichTextField(config_name='default')
    """

    def __init__(self, *args, **kwargs):
        self.config_name = kwargs.pop("config_name", "default")
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        """Return a form field instance for this model field."""
        defaults = {
            "form_class": RichTextFormField,
            "config_name": self.config_name,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class RichTextFormField(forms.CharField):
    """
    A form field that uses JoditWidget.

    Example usage in forms:
        content = RichTextFormField(config_name='default')
    """

    widget = JoditWidget

    def __init__(self, config_name="default", *args, **kwargs):
        kwargs["widget"] = self.widget(config_name=config_name)
        super().__init__(*args, **kwargs)
