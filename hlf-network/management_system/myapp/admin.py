from django.contrib import admin
from .models import UserProfile, AuthenticationPeer, Task, Mission
# Register your models here.
@admin.register(UserProfile) 
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'organizations', 'peers', 'uavs', 'channels']
    list_display_links = ['user', 'organizations', 'peers', 'uavs', 'channels']

@admin.register(AuthenticationPeer) 
class AuthenticationPeerAdmin(admin.ModelAdmin):
    list_display = ['userprofile', 'auth_name', 'mspid', 'cryptopath', 'certpath', 'keypath', 'tlscertpath', 'peerendpoint', 'gatewaypeer', "keypath_file", "tlscertpath_file", "certpath_file"]
    list_display_links = ['userprofile', 'auth_name', 'mspid', 'cryptopath', 'certpath', 'keypath', 'tlscertpath', 'peerendpoint', 'gatewaypeer', "keypath_file", "tlscertpath_file", "certpath_file"]

@admin.register(Mission) 
class MissionAdmin(admin.ModelAdmin):
    list_display = ['admin_user', 'mission_name', 'mission_coment', "created_at"]
    list_display_links = ['admin_user', 'mission_name', 'mission_coment', "created_at"]

@admin.register(Task) 
class TaskAdmin(admin.ModelAdmin):
    list_display = ['mission', 'task_name', 'task_coment', "created_at"]
    list_display_links = ['mission', 'task_name', 'task_coment', "created_at"]
