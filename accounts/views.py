from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def home(request):
    return render(request, 'accounts/home.html')
def dashboard(request):
    return render(request,'accounts/dashboard.html')
def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save user and hash password
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "User created successfully! Please login.")
            return redirect('dashboard')
        else:
            # Show form errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/signup.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')
