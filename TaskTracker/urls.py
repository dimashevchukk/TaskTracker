"""
URL configuration for TaskTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('tasks/', views.tasks_view, name='tasks'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
]

handler404 = 'main.views.custom_404'
handler500 = 'main.views.custom_500'
