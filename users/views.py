import re
import validate_email as EmailValidator

from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth

from bread import settings
from manage.models import Customer
from users.forms import LoginForm, RegistrationForm
from users.models import User
from users.utils import activation_token

from django.template.loader import render_to_string

import threading

class Thread(threading.Thread):

    def __init__(self, task):
        self.task = task
        threading.Thread.__init__(self)

    def run(self):
        self.task.send(fail_silently=False)

# Handles login and register
def authenticate(request):
    messages.error(request, "")
    if request.method == 'POST':
        if 'email' not in request.POST:
            return login(request)
        else:
            return signup(request)

    else:
        return render(request, 'signInUp.html')


def home(request):
    return render(request, 'base/home_base.html')


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

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('auth')


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
    form = LoginForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please fill all the forms.")
        return render(request, 'signInUp.html')

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    if not username and not password:
        messages.error(request, "Please fill all the forms.")
        return render(request, 'signInUp.html')

    user = auth.authenticate(username=username, password=password)
    context = {
        'fieldValues': request.POST,
        'signUp': False
    }
    if not user:
        try:
            user_temp = User.objects.get(username=username)
        except Exception as e:
            print('[DatabaseQueryException] @users.views "User not found", line 87 | Response = '+str(e))
            user_temp = None

        if user_temp is None:
            messages.error(request, "Invalid credentials")
            return render(request, 'signInUp.html')
        elif not user_temp.check_password(password):
            messages.error(request, "Password doesn't match")
            return render(request, 'signInUp.html', context)
        else:
            messages.error(request, "Account not activated, Please check your email.")
            return render(request, 'signInUp.html', context)

    auth.login(request, user)
    if request.user.is_staff:
        return redirect('dashboard')
    return redirect('home-page')

def signup(request):
    context = {
        'fieldValues': request.POST,
        'signUp': True
    }
    form = RegistrationForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please fill all the forms.")
        return render(request, 'signInUp.html', context)

    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    address = request.POST['address']

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
        user.is_staff = False
        user.is_admin = False
        user.is_customer = True
        user.save()
        Customer.objects.create(user=user, name=username, address=address)

        current_site = get_current_site(request).domain

        magic_link = reverse('activate', kwargs={
            'identity': urlsafe_base64_encode(force_bytes(user.pk)), 'token': activation_token.make_token(user)})
        activate_url = 'http://' + current_site + magic_link

        email_context = render_to_string('email/account_verification.html', {'user': user.username, "activator": activate_url})
        text_content = strip_tags(email_context)

        mail = EmailMultiAlternatives(
            "Activate your account",
            text_content,
            settings.EMAIL_HOST_USER,
            [email]
        )
        mail.attach_alternative(email_context, "text/html")

        Thread(mail).start()
        messages.success(request, 'A verification mail is sent to your email')
        return render(request, 'signInUp.html', context)

# TODO ForgetPassword

