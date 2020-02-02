from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import SignInForm, SignUpForm
from iauth import models
import requests
from connectors.VKontakte import VKontakte


def start_page(request):
    return HttpResponse("Hello from start page!")


def sign_in(request):
    return render(request, 'i-auth/sign-in.html', context={"SignInForm": SignInForm})


def sign_up(request):
    return render(request, 'i-auth/sign-up.html', context={"SignUpForm": SignUpForm})


def connections(request):
    vk = models.VKApp.objects.all()
    return render(request, 'connections/connections.html', context={"vkontakte": vk})


def vk_oauth_get_token(request):
    if request.method == "GET":
        code = request.GET['code']
        vk = models.VKApp.objects.get(pk=1)
        params = {'client_id': vk.client_id, 'code': code, 'client_secret': vk.client_secret,
                  'redirect_uri': "", 'v': ""}
        token = requests.get("https://oauth.vk.com/access_token", params=params).json()['access_token']
        vk = VKontakte.VKApp(token)
        vk_first_name, vk_last_name, vk_user_id = vk.get_profile_info()
        return HttpResponseRedirect()


def vk_accounts(request):
    return render(request, 'connections/accounts.html')
