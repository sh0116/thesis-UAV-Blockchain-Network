from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organizations = models.TextField()
    peers = models.TextField()
    uavs = models.TextField()
    channels = models.TextField()

    def __str__(self):
        return self.user.username

class AuthenticationPeer(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='Authprofile')
    auth_name = models.TextField()
    mspid = models.TextField()
    cryptopath = models.TextField()
    certpath = models.TextField()
    keypath = models.TextField()
    tlscertpath = models.TextField()
    peerendpoint = models.TextField()
    gatewaypeer = models.TextField()


    def __str__(self):
        return self.userprofile.user.username