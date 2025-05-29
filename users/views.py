from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User

def register_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or ''
    messages = None
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Student'
            user.save()
            login(request, user)
            return redirect(next_url or 'home')
        else:
            messages = form.non_field_errors()
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {
        'form': form,
        'next': next_url,
        'messages': messages,
        })

def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or ''
    messages = None
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect(next_url or 'home')
            else:
                messages = "Invalid username or password."
        else:
            messages = form.non_field_errors()
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {
        'form': form,
        'next': next_url,
        'messages': messages,
        })

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})
