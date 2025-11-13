"""
Views for the blog app.
"""

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm, CommentForm


class PostListView(ListView):
    """Display list of all published posts."""

    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(published=True)


class PostDetailView(DetailView):
    """Display a single post with comments."""

    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(approved=True)
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(CreateView):
    """Create a new blog post."""

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    """Update an existing blog post."""

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)


def add_comment(request, slug):
    """Add a comment to a post."""
    post = get_object_or_404(Post, slug=slug, published=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', slug=slug)

    return redirect('post_detail', slug=slug)
