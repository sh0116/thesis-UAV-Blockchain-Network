from __future__ import absolute_import, unicode_literals
from celery import shared_task, current_task
from celery.exceptions import SoftTimeLimitExceeded
from haversine import haversine, Unit
from .models import Uav
import time, json, math
from config.celery import app as celery_app


@celery_app.task(bind=True)
def calculate_position(self, start, end, progress):
    lat1, lon1 = start
    lat2, lon2 = end

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    new_lat = lat1 + delta_lat * progress
    new_lon = lon1 + delta_lon * progress

    return new_lat, new_lon

@celery_app.task(bind=True)
def update_uav_position(self, uav_id, src_lat, src_lng, dest_lat, dest_lng, speed_kph, time_interval=1):
    distance_km = haversine((src_lat, src_lng), (dest_lat, dest_lng))
    time_seconds = (distance_km / speed_kph) * 3600
    uav = Uav.objects.get(pk=uav_id)

    for i in range(int(time_seconds) + 1):
        progress = i / time_seconds
        current_position = calculate_position((src_lat, src_lng), (dest_lat, dest_lng), progress)
        print(f"Time: {i}s, Position: {current_position}")
        uav.latitude, uav.longitude = current_position
        uav.save()

        time.sleep(time_interval)

    current_task.update_state(state='PROGRESS', meta={'progress': progress})
