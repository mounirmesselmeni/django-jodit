"""
Forms for the blog app using django-jodit.
"""

from django import forms
from jodit.fields import RichTextFormField
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating/editing blog posts."""

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'excerpt', 'author', 'published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].help_text = "Enter a catchy title for your post"
        self.fields['slug'].help_text = "URL-friendly version (auto-generated from title)"


class CommentForm(forms.ModelForm):
    """Form for adding comments to posts."""

    class Meta:
        model = Comment
        fields = ['author', 'content']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].help_text = "Your name"
        self.fields['content'].help_text = "Your comment (basic formatting available)"


class StandalonePostForm(forms.Form):
    """Standalone form demonstrating direct use of RichTextFormField."""

    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Using RichTextFormField directly
    content = RichTextFormField(config_name='default', help_text="Full-featured rich text editor")

    # Another rich text field with different configuration
    summary = RichTextFormField(config_name='simple', required=False, help_text="Brief summary with basic formatting")

    author = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
