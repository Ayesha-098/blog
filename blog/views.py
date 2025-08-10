from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import CustomUserCreationForm, PostForm, CommentForm
from .models import Post, Comment, User


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_update_blog.html'
    success_url = reverse_lazy('my_posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        form.save_m2m()
        return response


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_update_blog.html'
    success_url = reverse_lazy('my_posts')

    def get_queryset(self):
        # Limit to posts authored by the current user
        return Post.objects.filter(author=self.request.user)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('my_posts')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PublishedPostsView(ListView):
    model = Post
    template_name = 'posts/all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.select_related('author').all()


class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/my_blogs.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.select_related('author').all()
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=self.object.pk)
        context = self.get_context_data(comment_form=comment_form)
        return self.render_to_response(context)


class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'account/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('published_posts')
        return render(request, 'account/signup.html', {'form': form})
