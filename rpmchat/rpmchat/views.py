from django.shortcuts import render


def home_run(request):
    return render(request, 'chat/home.html')
