from django.shortcuts import render
from django.http import HttpResponse
import json, os, requests


def index(request):
   return render(request, "index.html")

def client(request):
    url = "http://192.168.72.130:8000"+"/uav/"
    response = requests.get(url)

    if response.status_code == 200:
        markers = []
        for res in response.json():
            markers.append({'lat' : res['fields']['latitude'], 'lng': res['fields']['longitude']})
        markers_json = json.dumps(markers)
    return HttpResponse(markers_json, content_type='application/json')

def history(request):

    return render(request, 'history.html')


def channel(request, channel_name):
    return render(request, "channel.html")
#data = {"latitude": 39.904211, "longitude": 115.407395, "uav_manager": "New York"}
