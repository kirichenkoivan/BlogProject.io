# blogs/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
def home(request):
    blog_posts = BlogPost.objects.all().order_by('-date_added')
    return render(request, 'blogs/home.html', {'blog_posts': blog_posts})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправление на домашнюю страницу после успешной аутентификации
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # Перенаправляем на домашнюю страницу после выхода из системы
    else:
        # Обработка случая, когда запрос пришел методом GET
        return redirect('home')
@login_required
def create_blog_post(request):
    if request.method == 'GET':
        form = BlogPostForm()
        return render(request, 'blogs/create_blog_post.html', {'form': form})
    elif request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            new_blog_post = form.save(commit=False)
            new_blog_post.author = request.user
            new_blog_post.save()
            return redirect('home')
        else:
            return render(request, 'blogs/create_blog_post.html', {'form': form})

@login_required
def edit_blog_post(request, blog_post_id):
    blog_post = get_object_or_404(BlogPost, id=blog_post_id)
    if blog_post.author != request.user:
        raise Http404("You are not allowed to edit this post.")
    if request.method == 'POST':
        form = BlogPostForm(instance=blog_post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogPostForm(instance=blog_post)
    return render(request, 'blogs/edit_blog_post.html', {'form': form})

@login_required
def delete_blog_post(request, blog_post_id):
    blog_post = get_object_or_404(BlogPost, id=blog_post_id)
    if blog_post.author != request.user:
        raise Http404("You are not allowed to delete this post.")
    if request.method == 'POST':
        blog_post.delete()
        return redirect('home')
    return redirect('home')

