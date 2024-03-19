# BlogProject/urls.py
from django.contrib import admin
from django.urls import path, include    # Включите include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogs.urls')),    # Перенаправьте корневой URL-адрес на blogs.urls
    # Добавьте другие URL-адреса вашего проекта, если есть
]
