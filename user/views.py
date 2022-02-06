import re

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render

import validate_email as EmailValidator


def authenticate(request):
    if request.method == 'POST':
        if 'email' not in request.POST:
            return login(request)
        else:
            return signup(request)

    else:
        return render(request, 'signInUp.html')


def home(request):
    return render(request, 'base.html')

# CUSTOM FUNCTIONS

def checkPass(request, password):
    if len(password) < 6:
        messages.error(request, 'Password too short')
        return True
    elif not re.search("[a-z]", password):
        messages.error(request, 'Password must contain small letters')
        return True
    elif not re.search("[A-Z]", password):
        messages.error(request, 'Password must contain capital letters')
        return True
    elif not re.search("[0-9]", password):
        messages.error(request, 'Password must contain number')
        return True
    return False


def login(request):
    print("F")
    return render(request, 'signInUp.html')


def signup(request):

    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    context = {
        'fieldValues': request.POST,
        'signUp': True
    }

    if User.objects.filter(username=username).exists():
        pass
    elif User.objects.filter(email=email).exists():
        pass
    elif not EmailValidator.validate_email(email):
        pass
    elif checkPass(request, password):
        return render(request, 'signInUp.html', context)
    else:
        return render(request, 'signInUp.html', context)

