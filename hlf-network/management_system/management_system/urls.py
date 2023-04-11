"""management_system URL Configuration

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
from django.urls import path, include
from myapp import views
app_name = 'myapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.UAV_LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),
    path('tracker/', views.tracker, name='tracker'),
    path('mission/', views.mission, name='mission'),
    path('task/', views.task, name='task'),
    path('pages/', views.index, name='pages'),
    path('client_uav/', views.client_uav, name='client_uav'),
    path('client_hlf/<int:auth_peer_id>/', views.client_hlf, name='client_hlf'),
    path('client_hlf_getAllMission/', views.client_hlf_getAllMission, name='client_hlf_getAllMission'),
    path('updateAuthenticationPeer/<int:auth_peer_id>/', views.updateAuthenticationPeer, name='updateAuthenticationPeer'),
]

