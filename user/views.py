import re
import validate_email as EmailValidator

from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from user.utils import activation_token


# Handles login and register
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


def verification(request, identity, token):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(identity)))

            if not activation_token.check_token(user, token) or user.is_active:
                return redirect('activated' + '?message=' + user.username + ' already activated')

            user.is_active = True
            user.save()

            messages.success(request, 'Your account has been successfully activated')
            return redirect('activated')

        except Exception as ex:
            print(ex)
            return redirect('auth')

def activated(request):
    return render(request, 'activated.html')


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
    return render(request, 'signInUp.html')


def signup(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    context = {
        'fieldValues': request.POST,
        'signUp': True
    }

    # Guard Clauses

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Username already taken!')
        return render(request, 'signInUp.html', context)
    elif User.objects.filter(email=email).exists():
        messages.error(request, 'Email already exists')
        return render(request, 'signInUp.html', context)
    elif not EmailValidator.validate_email(email):
        messages.error(request, 'Invalid Email')
        return render(request, 'signInUp.html', context)
    elif checkPass(request, password):
        return render(request, 'signInUp.html', context)
    else:
        # If All Check Passes
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()

        current_site = get_current_site(request).domain

        magic_link = reverse('activate', kwargs={
            'identity': urlsafe_base64_encode(force_bytes(user.pk)), 'token': activation_token.make_token(user)})

        activate_url = 'http://' + current_site + magic_link

        email = EmailMessage(
            "Activate your account",
            'Hi ' + user.username + ', Please visit the link to activate your account \n' + activate_url,
            'noreply@bread.com',
            [email],
        )
        email.send(fail_silently=False)
        messages.success(request, 'Account successfully Created')
        return render(request, 'signInUp.html', context)

# EMAIL VERF WORKED SUCCESSFULLY BUT VERF LINK HAD A PROB

