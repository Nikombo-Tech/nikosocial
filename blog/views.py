from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
@login_required
def home(request):
    form = User.objects.all()
    context = {"form": form}
    return render(request, 'home.html', context)

def register_view(request):
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    email = request.POST.get('email')

    if request.method == 'POST':
        if password1 == password2:
            # Here you would typically save the user to the database
            User.objects.create_user(username=username, password=password1, email=email)
            return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})
        
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        # Here you would typically check the credentials against the database
        # For simplicity, we are using Django's built-in authentication system
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        # Here you would typically check the credentials against the database
        # For simplicity, we are using Django's built-in authentication system
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
        
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    # Here you would typically log the user out of the system
    return redirect('login')