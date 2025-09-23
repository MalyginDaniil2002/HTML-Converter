from .forms import SignInForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
import requests, os
from django.conf import settings


# Create your views here.
def log_in(request):
    if request.method == 'POST':
        signinform = SignInForm(request.POST)
        if not signinform.is_valid():
            return render(request, "auth.html", {'form': signinform})
        username = signinform.cleaned_data['login']
        password = signinform.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Данный пользователь отсутствует!")
            return render(request, "auth.html", {'form': signinform})
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Ввод логина или пароля выполнен неверно!")
            return render(request, "auth.html", {'form': signinform})
        login(request, user)
        return redirect('../account/')
    else:
        if request.user.is_authenticated:
            return redirect('../account/')
        signinform = SignInForm()
    return render(request, "auth.html", {'form': signinform})


def register(request):
    if request.method == 'POST':
        registerform = RegisterForm(request.POST)
        if not registerform.is_valid():
            return render(request, "auth.html", {'form': registerform})
        username        = registerform.cleaned_data['login']
        email           = registerform.cleaned_data['email']
        main_password   = registerform.cleaned_data['main_password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Данный логин существует!")
            return render(request, "auth_page.html", {'form': registerform})
        user = User.objects.create_user(username=username, password=main_password)
        login(request, user)
        return redirect('../account/')
    else:
        registerform = RegisterForm()
    return render(request, "auth.html", {'form': registerform})

def nologin(request):
    return redirect('/')

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')
