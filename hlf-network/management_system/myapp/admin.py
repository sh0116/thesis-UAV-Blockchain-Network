from django.contrib import admin
from .models import UserProfile, AuthenticationPeer
# Register your models here.
@admin.register(UserProfile) 
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'organizations', 'peers', 'uavs', 'channels']
    list_display_links = ['user', 'organizations', 'peers', 'uavs', 'channels']

@admin.register(AuthenticationPeer) 
class AuthenticationPeerAdmin(admin.ModelAdmin):
    list_display = ['userprofile', 'auth_name', 'mspid', 'cryptopath', 'certpath', 'keypath', 'tlscertpath', 'peerendpoint', 'gatewaypeer']
    list_display_links = ['userprofile', 'auth_name', 'mspid', 'cryptopath', 'certpath', 'keypath', 'tlscertpath', 'peerendpoint', 'gatewaypeer']