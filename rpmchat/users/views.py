from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, decorators
from django.contrib.auth.models import User
from users.forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            print(password)
            form.save()
            return redirect('users:login')
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def login_view(request):
    error_msg = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat:client')
        else:
            error_msg = 'Invalid username or password'
    else:
        error_msg = None
    return render(request, 'registration/login.html', {'error_msg': error_msg})


@decorators.login_required(login_url='users:login')
def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'registration/profile.html', {'username': user})


def logout_view(request):
    logout(request)
    return redirect('users:login')
