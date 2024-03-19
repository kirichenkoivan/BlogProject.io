# blogs/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView

urlpatterns = [
    path('login/', views.custom_login, name='login'),  # Используйте ваше кастомное представление для страницы входа
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('', views.home, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('edit/<int:blog_post_id>/', views.edit_blog_post, name='edit_blog_post'),
    path('delete/<int:blog_post_id>/', views.delete_blog_post, name='delete_blog_post'),
]
