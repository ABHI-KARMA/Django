# Auth Views
from django.shortcuts import render,redirect
from django.http import request,HttpResponse
from .models import SignupModel
from django.contrib.auth import authenticate, login,logout
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    else:
        return redirect('LOGIN')

def signup(request):
    if request.method == 'POST':
        n = request.POST['name']
        num = request.POST['number']
        cname = request.POST['companyname']
        e = request.POST['email']
        pas = request.POST['pass']
        user = SignupModel.objects.create(name=n,number=num,cname=cname,email=e,pw=pas)
        return redirect('LOGIN')
    return render(request,'signup.html')

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['userpass']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('HOME')
        else:
            return HttpResponse("username and password are incorrect")
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('LOGIN')

# Auth Model 
from django.db import models
class SignupModel(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    cname = models.CharField(max_length=100)
    email = models.EmailField()
    uname = models.CharField(max_length=50,default="")
    pw = models.CharField(max_length=30)
    
# Auth Urls
from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='HOME'),
    path('login/',loginUser,name='LOGIN'),    
    path('signup/',signup,name='SIGNUP'),
    path('logout/',logoutUser,name='LOGOUT')
]
