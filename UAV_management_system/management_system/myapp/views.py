from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json, os, requests

from django.conf import settings
<<<<<<< HEAD
=======

>>>>>>> 3bb20780f00f0da7dbfcf099c807bd1e79455654

class UAV_LoginView(LoginView):
    template_name = 'login.html'  # 사용자 정의 로그인 템플릿을 지정합니다.
    def post(self, request, *args, **kwargs):
        # 로그인 인증 과정
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})

    

@login_required(login_url='/login/')
def index(request):
   return render(request, "index.html")

@login_required(login_url='/login/')
def dashboard(request):
    host = request.get_host()
    return HttpResponseRedirect('http://'+host+':3000/dashboards')

@login_required(login_url='/login/')
def client(request):
    url = "http://192.168.72.130:8000"+"/uav/"
    response = requests.get(url)
    return HttpResponse(json.dumps(response.json()), content_type='application/json')

@login_required(login_url='/login/')
def history(request):
    return render(request, 'history.html')

@login_required(login_url='/login/')
def tracker(request):
    return render(request, 'tracker.html')

@login_required(login_url='/login/')
def mission(request, mission_name):
    return render(request, "mission.html")
#data = {"latitude": 39.904211, "longitude": 115.407395, "uav_manager": "New York"}
