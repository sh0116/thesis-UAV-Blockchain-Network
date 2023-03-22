from django.db import models

# Create your models here.
class Uav(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    uav_manager = models.TextField()
    def __str__(self):  # admin에서 표시될 user 필드 정보 설정
        return str(self.pk)
    class Meta:
        db_table = 'uav'
        verbose_name = 'uav' 
        verbose_name_plural = 'uav' 