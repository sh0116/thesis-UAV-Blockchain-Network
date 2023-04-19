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
    region = models.TextField(blank=True)
    user_code = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class AuthenticationPeer(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='Authprofile', blank=True)
    auth_name = models.TextField(blank=True)
    mspid = models.TextField(blank=True)
    cryptopath = models.TextField(blank=True, default='../management_system')
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

    def save(self, *args, **kwargs):

        if self.certpath_file:
            self.certpath = self.cryptopath+self.certpath_file.url
        if self.tlscertpath_file:
            self.tlscertpath = self.cryptopath+self.tlscertpath_file.url
        if self.keypath_file:
            self.keypath = self.cryptopath+'/'.join(self.keypath_file.url.split("/")[:-1])

        super().save(*args, **kwargs)



class MissionAndTask(models.Model):
    admin_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='mission_task', blank=True)
    mission_task = models.TextField(blank=True)
    mission_task_name = models.TextField(blank=True)
    mission_task_coment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.mission_task} - {self.mission_task_name}" 