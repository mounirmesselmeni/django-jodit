"""
Django admin configuration for blog models.
Jodit editor is automatically used for RichTextField fields.
"""

from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model."""

    list_display = ['title', 'author', 'created_at', 'published']
    list_filter = ['published', 'created_at', 'author']
    search_fields = ['title', 'content', 'author']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {'fields': ('title', 'slug', 'author', 'published')}),
        (
            'Content',
            {
                'fields': ('content', 'excerpt'),
                'description': 'Use the Jodit editor to format your content. '
                'The content field has full features, while excerpt has basic formatting only.',
            },
        ),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    readonly_fields = ['updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model."""

    list_display = ['author', 'post', 'created_at', 'approved']
    list_filter = ['approved', 'created_at']
    search_fields = ['author', 'content', 'post__title']
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {'fields': ('post', 'author', 'content', 'approved')}),
        ('Metadata', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

    readonly_fields = ['created_at']
