"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from uav import views

urlpatterns = [
    path('iamnotadmin/', admin.site.urls),
    path('uav/', views.uav),
    path('start_task/', views.start_task, name='start_task'),
    path('check_task/<str:task_id>/', views.check_task, name='check_task'),
    path('cancel_task/<str:task_id>/', views.cancel_task, name='cancel_task'),
]

