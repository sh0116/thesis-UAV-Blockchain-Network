from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .models import Uav


@csrf_exempt
def uav(request):
    if request.method == 'GET':
        queryset = Uav.objects.all()
        queryset_json = serializers.serialize('json', queryset)
        return HttpResponse(queryset_json, content_type='application/json')

    if request.method == 'POST':
        if request.POST['PK']:
            Uav.objects.filter(pk=request.POST['PK']).update(
                latitude = request.POST['latitude'],
                longitude = request.POST['longitude'],
                uav_manager = request.POST['uav_manager']
            )
        else:
            Uav.objects.create(
                latitude = request.POST['latitude'],
                longitude = request.POST['longitude'],
                uav_manager = request.POST['uav_manager']
            )
        return HttpResponse("200", content_type='application/json')
