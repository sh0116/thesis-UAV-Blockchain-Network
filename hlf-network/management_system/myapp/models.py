from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import os

def certpath_upload_to(instance, filename):
    user_id = instance.userprofile.user.id
    return os.path.join(f"{user_id}/{instance.auth_name}/signcerts/", filename)

def tlscertpath_file_upload_to(instance, filename):
    user_id = instance.userprofile.user.id
    return os.path.join(f"{user_id}/{instance.auth_name}/tls/", filename)

def keypath_file_upload_to(instance, filename):
    user_id = instance.userprofile.user.id
    return os.path.join(f"{user_id}/{instance.auth_name}/keystore/", filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=True)
    organizations = models.TextField(blank=True)
    peers = models.TextField(blank=True)
    uavs = models.TextField(blank=True)
    channels = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class AuthenticationPeer(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='Authprofile', blank=True)
    auth_name = models.TextField(blank=True)
    mspid = models.TextField(blank=True)
    cryptopath = models.TextField(blank=True, default='../management_system/media/')
    peerendpoint = models.TextField(blank=True)
    gatewaypeer = models.TextField(blank=True)
    
    certpath = models.TextField(blank=True)
    keypath = models.TextField(blank=True)
    tlscertpath = models.TextField(blank=True)

    keypath_file = models.FileField(upload_to=keypath_file_upload_to, default='', blank=True)
    tlscertpath_file = models.FileField(upload_to=tlscertpath_file_upload_to, default='', blank=True)
    certpath_file = models.FileField(upload_to=certpath_upload_to, default='', blank=True)

    def __str__(self):
        return self.userprofile.user.username

class Mission(models.Model):
    admin_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='mission', blank=True)
    mission_name = models.CharField(max_length=255, unique=True, primary_key=True)
    mission_coment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.mission_name

class Task(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, to_field='mission_name', related_name='task', blank=True)
    task_name = models.CharField(max_length=100, primary_key=True)
    task_coment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.mission} - {self.task_name}" 