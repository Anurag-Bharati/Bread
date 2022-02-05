from django.shortcuts import render


def authenticate(request):
    return render(request, 'signInUp.html')
