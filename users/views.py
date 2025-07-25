# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from django.urls import reverse


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Role based redirect
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'staff':
                return redirect('staff_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'users/login.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        role = request.POST.get('role', 'customer')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            phone=phone,
            address=address,
            role=role
        )
        user.save()
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'users/register.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def admin_dashboard(request):
    # You can add admin dashboard logic here
    if request.user.role != 'admin':
        return redirect('login')
    return render(request, 'users/admin_dashboard.html')


@login_required
def staff_dashboard(request):
    # You can add staff dashboard logic here
    if request.user.role != 'staff':
        return redirect('login')
    return render(request, 'users/staff_dashboard.html')


@login_required
def home(request):
    # Home page after customer login
    return render(request, 'users/home.html')
