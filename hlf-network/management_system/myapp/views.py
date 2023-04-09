from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from .models import UserProfile, AuthenticationPeer
import json, os, requests


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


def logout_view(request):
    logout(request)
    return redirect('/') 

@login_required(login_url='/login/')
def updateAuthenticationPeer(request, auth_peer_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            auth_peer = AuthenticationPeer.objects.get(pk=auth_peer_id)
            print(data)
            auth_peer.auth_name = data.get('auth_name', auth_peer.auth_name)
            auth_peer.mspid = data.get('mspid', auth_peer.mspid)
            auth_peer.cryptopath = data.get('cryptopath', auth_peer.cryptopath)
            auth_peer.certpath = data.get('certpath', auth_peer.certpath)
            auth_peer.keypath = data.get('keypath', auth_peer.keypath)
            auth_peer.tlscertpath = data.get('tlscertpath', auth_peer.tlscertpath)
            auth_peer.peerendpoint = data.get('peerendpoint', auth_peer.peerendpoint)
            auth_peer.gatewaypeer = data.get('gatewaypeer', auth_peer.gatewaypeer)
            
            auth_peer.save()
            response_data = {
                'id': auth_peer.id,
                'auth_name': auth_peer.auth_name,
                'mspid': auth_peer.mspid,
                'cryptopath': auth_peer.cryptopath,
                'certpath': auth_peer.certpath,
                'keypath': auth_peer.keypath,
                'tlscertpath': auth_peer.tlscertpath,
                'peerendpoint': auth_peer.peerendpoint,
                'gatewaypeer': auth_peer.gatewaypeer,
            }
            return JsonResponse(response_data, status=200)
        except AuthenticationPeer.DoesNotExist:
            return JsonResponse({'error': 'AuthenticationPeer not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required(login_url='/login/')
def index(request):
    user_profile = UserProfile.objects.get(user=request.user)
    auth_peers = AuthenticationPeer.objects.filter(userprofile=user_profile)
    context = {
        'user': request.user,
        'auth_peers': auth_peers
        }
    return render(request, 'index.html', context)

@login_required(login_url='/login/')
def dashboard(request):
    host = request.get_host()
    return HttpResponseRedirect('http://'+host+':3000/dashboards')

@login_required(login_url='/login/')
def client_uav(request):
    url = "http://192.168.72.130:8000"+"/uav/"
    response = requests.get(url)
    return HttpResponse(json.dumps(response.json()), content_type='application/json')

@login_required(login_url='/login/')
def client_hlf(request, auth_peer_id):
    url = "http://192.168.72.128:3030/connect"
    auth_peer = AuthenticationPeer.objects.get(pk=auth_peer_id)

    requests_data = {
        "auth" : {
            'mspID': auth_peer.mspid,
            'cryptoPath': auth_peer.cryptopath,
            'certPath': auth_peer.certpath,
            'keyPath': auth_peer.keypath,
            'tlsCertPath': auth_peer.tlscertpath,
            'peerEndpoint': auth_peer.peerendpoint,
            'gatewayPeer': auth_peer.gatewaypeer,
        },
        "asset" : {
            "ID":"",
            "Status":"",
            "Latitude":"",
            "Longitude":""
        }
    }
    response = requests.get(url, data=json.dumps(requests_data))
    if response.status_code==200:
        return HttpResponse(response.status_code, content_type='application/json')
    else:
        return HttpResponse(response.status_code, content_type='application/json')
""
@login_required(login_url='/login/')
def history(request):
    return render(request, 'history.html')

@login_required(login_url='/login/')
def tracker(request):
    return render(request, 'tracker.html')

@login_required(login_url='/login/')
def mission(request, mission_name):
    return render(request, "mission.html")
