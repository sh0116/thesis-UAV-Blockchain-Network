from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json, os, requests

from django.conf import settings
import boto3

# AWS Location Service 클라이언트 생성
location_client = boto3.client(
    'location',
    region_name="ap-northeast-1",
    aws_access_key_id="AKIA4AV6IAXHVO7JP4SB",
    aws_secret_access_key="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"
)
def my_view(request):
    # 여기서 AWS Location Service API를 호출하고 처리할 수 있습니다.
    # 예를 들어, geocoding API를 사용하여 주소를 좌표로 변환하려면 다음과 같이 작성합니다.
    response = location_client.search_place_index_for_text(
        IndexName='YourPlaceIndexName',
        Text='1600 Amphitheatre Parkway, Mountain View, CA'
    )

    # 결과를 처리하고 템플릿에 전달하거나 JSON 형식으로 반환할 수 있습니다.
    coordinates = response['Results'][0]['Place']['Geometry']['Point']
    context = {'coordinates': coordinates}
    return render(request, 'history.html', context)

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
