"""
Blog models demonstrating django-jodit integration.
"""

from django.db import models
from django.urls import reverse
from django.utils import timezone
from jodit.fields import RichTextField


class Post(models.Model):
    """Blog post model with rich text fields."""

    title = models.CharField(max_length=200, help_text="Post title")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL-friendly version of title")

    # Rich text field with default (full-featured) configuration
    content = RichTextField(help_text="Main post content with full editor features")

    # Rich text field with simple configuration
    excerpt = RichTextField(config_name='simple', blank=True, help_text="Short excerpt with basic formatting")

    author = models.CharField(max_length=100, default="Admin")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    """Comment model with simple rich text field."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)

    # Simple rich text field for comments
    content = RichTextField(config_name='simple', help_text="Comment content with basic formatting")

    created_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"
