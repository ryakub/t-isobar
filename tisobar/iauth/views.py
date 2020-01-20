from django.http import HttpResponse
from django.shortcuts import render
from .forms import SignInForm, SignUpForm


def start_page(request):
    return HttpResponse("Hello from start page!")


def sign_in(request):
    return render(request, 'i-auth/sign-in.html', context={"SignInForm": SignInForm})


def sign_up(request):
    return render(request, 'i-auth/sign-up.html', context={"SignUpForm": SignUpForm})


def connections(request):
    return render(request, 'connections/connections.html')


def vk_accounts(request):
    return render(request, 'connections/accounts.html')
