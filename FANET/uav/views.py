from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from .models import Uav
from .tasks import update_uav_position
from celery.app.control import Control
from config.celery import app

import time, json, math


@csrf_exempt
def uav(request):
    if request.method == 'GET':
        queryset = Uav.objects.all()
        queryset_json = serializers.serialize('json', queryset)
        return HttpResponse(queryset_json, content_type='application/json')

    if request.method == 'PUT':
        data = json.loads(request.body)
        uav_id = data.get('PK')
        uav = Uav.objects.get(pk=uav_id)
        uav.latitude, uav.longitude = data.get('latitude'), data.get('longitude')
        uav.save()

        return HttpResponse("200", content_type='application/json')

    if request.method == 'POST':
        Uav.objects.create(
            latitude = request.POST['latitude'],
            longitude = request.POST['longitude'],
            uav_manager = request.POST['uav_manager']
        )
        return HttpResponse("200", content_type='application/json')

@csrf_exempt
def start_task(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        src_lat = Uav.objects.get(pk=data.get('PK')).latitude
        src_lng = Uav.objects.get(pk=data.get('PK')).longitude
        dest_lat = float(data.get('latitude'))
        dest_lng = float(data.get('longitude'))
        speed_kph = 200.0
        time_interval = 2  # 2초 간격

        uav_id = data.get('PK')

        task = update_uav_position.apply_async(args=(uav_id, src_lat, src_lng, dest_lat, dest_lng, speed_kph))
        
        return JsonResponse({'task_id': task.id}, status=202)


@csrf_exempt
def check_task(request, task_id):
    if request.method == 'GET':
        task = update_uav_position.AsyncResult(task_id)
        if task.state == 'PENDING':
            return JsonResponse({'state': task.state})
        elif task.state == 'PROGRESS':
            return JsonResponse({'state': task.state, 'progress': task.info.get('progress', 0)})
        else:
            return JsonResponse({'state': task.state})


@csrf_exempt
def cancel_task(request, task_id):
    task = update_uav_position.AsyncResult(task_id)
    task.revoke(terminate=True)
    return JsonResponse({'state': 'REVOKED'})