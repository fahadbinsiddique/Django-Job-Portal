from django.contrib import admin
from django.urls import path, include
from Job_Portal_App.views import *

urlpatterns = [
    path("", home_page, name="home_page"),
    path("login/", login_page, name="login_page"),
    path("register/", register_page, name="register_page"),
    path("logout/", logout_page, name="logout_page"),
    path("profile/", profile_page, name="profile_page"),
    path("profile-update/", profile_update, name="profile_update"),
    path("job-list/", job_list, name="job_list"),
    path("job-post/", job_post, name="job_post"),
    path("job-edit/<str:j_id>/", job_edit, name="job_edit"),
    path("job-delete/<str:j_id>/", job_delete, name="job_delete"),
]
