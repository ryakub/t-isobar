"""tisobar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from iauth import views as iauth_views
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', iauth_views.start_page, name='start-page'),
    url(r'^sign-in/$', iauth_views.sign_in, name='sign-in'),
    url(r'^sign-up/$', iauth_views.sign_up, name='sign-up'),
    url(r'^connections/$', iauth_views.connections, name='connections'),
    url(r'^vkontakte/accounts/$', iauth_views.vk_accounts, name='vk_accounts'),
    url(r'^vkontakte/oauth/code/', iauth_views.vk_oauth_get_token, name='vk_oauth_get_token'),
]
