from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 유저에 관한 정보
    # 채널에 대한 정보
    # 조직에 대한 정보
    # UAV에 관한 정보
    def __str__(self):
        return self.user.username