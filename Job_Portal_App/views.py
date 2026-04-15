from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from Job_Portal_App.models import *
from Job_Portal_App.forms import *

# Create your views here.


def home_page(request):
    return render(request, "home.html")


def register_page(request):
    if request.method == "POST":
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect("login_page")
    form_data = RegisterForm()
    context = {
        "form_data": form_data,
        "title": "Registration",
    }
    return render(request, "register.html", context)


def login_page(request):
    if request.method == "POST":
        form_data = LoginForm(request, request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            login(request, user)
            return redirect("home_page")
    form_data = LoginForm()
    context = {
        "form_data": form_data,
        "title": "Login",
    }
    return render(request, "login.html", context)


@login_required
def logout_page(request):
    logout(request)
    return redirect("home_page")


@login_required
def profile_page(request):

    return render(request, "profile.html")


@login_required
def profile_update(request):
    user = request.user
    if user.user_types == "Recruiter":
        try:
            profile = user.recruiter_profile
        except RecruiterProfileModel.DoesNotExist:
            profile = None
        if request.method == "POST":
            form_data = RecProfileForm(request.POST, request.FILES, instance=profile)
            if form_data.is_valid():
                data = form_data.save(commit=False)
                data.recruiter = user
                data.save()
                return redirect("profile_page")
        form_data = RecProfileForm()
    else:
        try:
            profile = user.seeker_profile
        except JobSeekerProfileModel.DoesNotExist:
            profile = None
        if request.method == "POST":
            form_data = SeekerProfileForm(request.POST, request.FILES, instance=profile)
            if form_data.is_valid():
                data = form_data.save(commit=False)
                data.seeker = user
                data.save()
                return redirect("profile_page")
        form_data = SeekerProfileForm()

    context = {
        "form_data": form_data,
        "title": "Update Profile",
        "heading": "Update Profile",
        "btn": "Update Profile",
    }
    return render(request, "master/base-form.html", context)


def job_list(request):
    return render(request, "job-list.html")


def job_post(request):
    if request.method == "POST":
        form_data = JobPostForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect("job_list")
    form_data = JobPostForm()
    context = {
        "form_data": form_data,
        "title": "Add Job Post",
        "heading": "Add Job Post",
        "btn": "Post Job",
    }
    return render(request, "master/base-form.html", context)
