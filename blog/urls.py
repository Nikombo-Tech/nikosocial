from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("accounts/login", login_view, name="login"),
    path("accounts/logout", logout_view, name="logout"),
    path("accounts/register", register_view, name="register"),
]