import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, AuthenticationPeer, MissionAndTask
from .forms import UserProfileForm
import requests


class UMS_LoginView(LoginView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
            
@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/') 


@login_required(login_url='/login/')
def index(request):
    user_profile = UserProfile.objects.get(user=request.user)
    auth_peers = AuthenticationPeer.objects.filter(userprofile=user_profile)
    mission_task = MissionAndTask.objects.order_by('created_at')
    context = {
        'user': request.user,
        'auth_peers': auth_peers,
        'mission_task': mission_task
    }
    return render(request, 'index.html', context)

@login_required(login_url='/login/')
def dashboard(request):
    host = request.get_host()
    return HttpResponseRedirect('http://' + host + ':3000/dashboards')

@login_required(login_url='/login/')
def history(request):
    return render(request, 'history.html')

@login_required(login_url='/login/')
def tracker(request):
    return render(request, 'tracker.html')

@login_required(login_url='/login/')
def mission(request):
    user_profile = UserProfile.objects.get(user=request.user)
    auth_peers = AuthenticationPeer.objects.filter(userprofile=user_profile)
    mission_task = MissionAndTask.objects.order_by('created_at')
    context = {
        'user': request.user,
        'auth_peers': auth_peers,
        'mission_task': mission_task
    }
    return render(request, "mission.html", context)

@login_required(login_url='/login/')
def task(request):
    user_profile = UserProfile.objects.get(user=request.user)
    auth_peers = AuthenticationPeer.objects.filter(userprofile=user_profile)
    mission_task = MissionAndTask.objects.order_by('created_at')
    context = {
        'user': request.user,
        'auth_peers': auth_peers,
        'mission_task': mission_task
    }
    return render(request, "task.html", context)



@login_required(login_url='/login/')
def fanet_getAsset(request):
    response = requests.get('http://' + '192.168.72.130' + ':8000/uav/')
    return JsonResponse(response.json(), safe=False)

class HLF:
    def __init__(self, host):
        self.base_url = 'https://' + host + ':3030'

    def send_request(self, endpoint, method='GET', data=None):
        url = f'{self.base_url}{endpoint}'
        response = None

        if method == 'GET':
            response = requests.get(url, json=data, verify=False)
        elif method == 'POST':
            response = requests.post(url, json=data, verify=False)
        elif method == 'DELETE':
            response = requests.delete(url, json=data, verify=False)

        return response

    def get_auth_data(self, auth_peer):
        return {
            'mspID': auth_peer.mspid,
            'cryptoPath': auth_peer.cryptopath,
            'certPath': auth_peer.certpath,
            'keyPath': auth_peer.keypath,
            'tlsCertPath': auth_peer.tlscertpath,
            'peerEndpoint': auth_peer.peerendpoint,
            'gatewayPeer': auth_peer.gatewaypeer,
        }

    def get_auth_peer(self, auth_id):
        try:
            auth_peer = AuthenticationPeer.objects.get(id=auth_id)
            return auth_peer
        except AuthenticationPeer.DoesNotExist:
            return None

@login_required(login_url='/login/')
def hlf_Connect(request, auth_peer_id):
    client = HLF(host = request.get_host())
    auth_peer = client.get_auth_peer(auth_peer_id)
    auth_data = client.get_auth_data(auth_peer)
    response = client.send_request('/connect', method='GET', data={'auth': auth_data})
    if response.status_code == 200:
        try:
            return JsonResponse(response.json(), safe=False)
        except:
            return JsonResponse(response.status_code, safe=False)
    else:
        return HttpResponse(response.status_code, status=response.status_code, content_type='application/json')

@login_required(login_url='/login/')
def hlf_getAllMission(request, auth_peer_id=0):
    if request.method == 'POST':
        client = HLF(host = request.get_host())
        try:
            if auth_peer_id:
                auth_peer = client.get_auth_peer(auth_peer_id)
                auth_peers = [auth_peer]
            else:
                auth_peers = AuthenticationPeer.objects.all()

            for auth_peer in auth_peers:
                auth_data = client.get_auth_data(auth_peer)
                response = client.send_request('/getAllMissions', method='GET', data={'auth': auth_data})

                if response.status_code == 200:
                    try:
                        return JsonResponse(response.json(), safe=False)
                    except:
                        return JsonResponse(response.status_code, safe=False)
                else:
                    return HttpResponse(response.status_code, status=response.status_code, content_type='application/json')

        except Exception as e:
            print(e)
            return HttpResponse(status=500)

    return HttpResponse(status=405)

@login_required(login_url='/login/')
def hlf_createMission(request, auth_peer_id):
    if request.method == 'POST':
        client = HLF(host = request.get_host())
        try:
            auth_peer = client.get_auth_peer(auth_peer_id)
            auth_data = client.get_auth_data(auth_peer)
            data = json.loads(request.body)
            data['auth'] = auth_data
            response = client.send_request('/createMission', method='POST', data=data)
            if response.status_code == 200:
                data = {
                    "admin_user" : UserProfile.objects.get(user=request.user),
                    "mission_task" : "MISSION",
                    "mission_task_name" : data['Mission_Asset']['ID'],
                    "mission_task_coment" : "CREATE"
                }
                manager = MissionAndTask(**data)
                manager.save()
                try:
                    return JsonResponse(response.json(), safe=False)
                except:
                    return JsonResponse(response.status_code, safe=False)
            else:
                return HttpResponse(response.status_code, status=response.status_code, content_type='application/json')
        except Exception as e:
            print(e)
            return HttpResponse(status=500)

    return HttpResponse(status=405)

@login_required(login_url='/login/')
def hlf_deleteMission(request, auth_peer_id):
    if request.method == 'DELETE':
        client = HLF(host = request.get_host())
        try:
            auth_peer = client.get_auth_peer(auth_peer_id)
            auth_data = client.get_auth_data(auth_peer)
            data = json.loads(request.body)
            data['auth'] = auth_data
            response = client.send_request('/DeleteMissionByID', method='DELETE', data=data)

            if response.status_code == 200:
                data = {
                    "admin_user" : UserProfile.objects.get(user=request.user),
                    "mission_task" : "MISSION",
                    "mission_task_name" : data['Mission_Asset']['ID'],
                    "mission_task_coment" : "DELETE"
                }
                manager = MissionAndTask(**data)
                manager.save()
                try:
                    return JsonResponse(response.json(), safe=False)
                except:
                    return JsonResponse(response.status_code, safe=False)
            else:
                return HttpResponse(response.status_code, status=response.status_code, content_type='application/json')

        except Exception as e:
            print(e)
            return HttpResponse(status=500)

    return HttpResponse(status=405)

@login_required(login_url='/login/')
def hlf_createTask(request, auth_peer_id):
    if request.method == 'POST':
        client = HLF(host = request.get_host())
        try:
            auth_peer = client.get_auth_peer(auth_peer_id)
            auth_data = client.get_auth_data(auth_peer)
            data = json.loads(request.body)
            data['auth'] = auth_data
            response = client.send_request('/createTask', method='POST', data=data)

            if response.status_code == 200:
                data = {
                    "admin_user" : UserProfile.objects.get(user=request.user),
                    "mission_task" : "TASK",
                    "mission_task_name" : data['Task_Asset']['ID'],
                    "mission_task_coment" : "CREATE"
                }
                manager = MissionAndTask(**data)
                manager.save()
                try:
                    return JsonResponse(response.json(), safe=False)
                except:
                    return JsonResponse(response.status_code, safe=False)
            else:
                return HttpResponse(response.status_code, status=response.status_code, content_type='application/json')

        except Exception as e:
            print(e)
            return HttpResponse(status=500)

    return HttpResponse(status=405)



@login_required(login_url='/login/')
def updateAuthenticationPeer(request, auth_peer_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            auth_peer = AuthenticationPeer.objects.get(pk=auth_peer_id)
            auth_peer.update(data)
            response_data = auth_peer.get_json_data()
            return JsonResponse(response_data, status=200)
        except AuthenticationPeer.DoesNotExist:
            return JsonResponse({'error': 'AuthenticationPeer not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required(login_url='/login/')
def update_userprofile(request):
    userprofile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=userprofile)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'index.html', {'user': form})
