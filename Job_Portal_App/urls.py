from django.contrib import admin
from django.urls import path, include
from Job_Portal_App.views import *

urlpatterns = [
    path("", home_page, name="home_page"),
    path("login/", login_page, name="login_page"),
    path("register/", register_page, name="register_page"),
]
