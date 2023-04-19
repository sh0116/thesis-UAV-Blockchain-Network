from django.contrib import admin
from .models import UserProfile, AuthenticationPeer, MissionAndTask
# Register your models here.
@admin.register(UserProfile) 
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'organizations', 'region', 'user_code']
    list_display_links = ['user', 'organizations', 'region', 'user_code']

@admin.register(AuthenticationPeer) 
class AuthenticationPeerAdmin(admin.ModelAdmin):
    list_display = ['userprofile', 'auth_name', 'mspid', 'cryptopath', 'certpath', 'keypath', 'tlscertpath', 'peerendpoint', 'gatewaypeer', "keypath_file", "tlscertpath_file", "certpath_file"]
    list_display_links = ['userprofile', 'auth_name', 'mspid', 'cryptopath', 'certpath', 'keypath', 'tlscertpath', 'peerendpoint', 'gatewaypeer', "keypath_file", "tlscertpath_file", "certpath_file"]

@admin.register(MissionAndTask) 
class MissionAndTaskAdmin(admin.ModelAdmin):
    list_display = ['admin_user', 'mission_task', 'mission_task_name', "mission_task_coment","created_at"]
    list_display_links = ['admin_user', 'mission_task', 'mission_task_name', "mission_task_coment","created_at"]