from django.contrib import admin
from django.urls import path, include
from myapp import views
app_name = 'myapp'

urlpatterns = [
    # admin page
    path('admin/', admin.site.urls),
    # User Auth
    path('login/', views.UMS_LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Pages
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),
    path('tracker/', views.tracker, name='tracker'),
    path('mission/', views.mission, name='mission'),
    path('task/', views.task, name='task'),
    # EndPoint
    path('fanet_getAsset/', views.fanet_getAsset, name='fanet_getAsset'),
    path('hlf_Connect/<int:auth_peer_id>/', views.hlf_Connect, name='hlf_Connect'),
    path('hlf_getAllMission/<int:auth_peer_id>/', views.hlf_getAllMission, name='hlf_getAllMission'),
    path('hlf_createMission/<int:auth_peer_id>/', views.hlf_createMission, name='hlf_createMission'),
    path('hlf_deleteMission/<int:auth_peer_id>/', views.hlf_deleteMission, name='hlf_deleteMission'),
    path('hlf_createTask/<int:auth_peer_id>/', views.hlf_createTask, name='hlf_createTask'),
    path('hlf_getHistory/<int:auth_peer_id>/<str:mission_task_id>/', views.hlf_getHistory, name='hlf_getHistory'),
    # Update Django Model
    path('updateAuthenticationPeer/<int:auth_peer_id>/', views.updateAuthenticationPeer, name='updateAuthenticationPeer'),
    path('update_userprofile/', views.update_userprofile, name='update_userprofile'),
]

