from django.contrib import admin
from .models import Uav
# Register your models here.
@admin.register(Uav) 
class UavAdmin(admin.ModelAdmin):
    list_display = ['latitude', 'longitude', 'uav_manager']
    list_display_links = ['latitude', 'longitude', 'uav_manager']