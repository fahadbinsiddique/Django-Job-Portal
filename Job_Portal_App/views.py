from django.shortcuts import render,redirect
from Job_Portal_App.models import *
from Job_Portal_App.forms import *
# Create your views here.

def home_page(request):
    return render(request,"home.html")

def register_page(request):
    if request.method =='POST':
        form_data=RegisterForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login_page')
    form_data= RegisterForm()
    context={
        'form_data':form_data,
        'title':'Registration'
    }
    return render(request, "register.html", context)

def login_page(request):
    return render(request,"login.html")
