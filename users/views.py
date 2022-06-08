from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm, UserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import uuid

from .models import *


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = NewUserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']

                try:
                    if User.objects.filter(username=username).first():
                        messages.warning(request, 'Username already taken')
                        return redirect('login')
                    if User.objects.filter(email=email).first():
                        messages.warning(request, 'Email already taken')
                        return redirect('login')
                    
                    user = User(username=username, first_name=first_name, last_name=last_name, email=email)
                    user.set_password(password)
                    user.save()
                    auth_token = str(uuid.uuid4())
                    profile = Profile.objects.create(user=user, auth_token=auth_token)
                    profile.save()
                    send_mail_after_registration(email, auth_token)
                    return redirect('token_send')
                except Exception as e:
                    print(e)
            else:
                messages.warning(request, 'Invalid Credentials')
                return redirect('register')
        else:
            form = NewUserForm()
        context = {
            'form': form,
        }
        return render(request, 'users/register_new.html', context)


def success(request):
    return render(request , 'users/success.html')


def token_send(request):
    return render(request , 'users/token_send.html')


def verify(request, auth_token):
    try:
        profile = Profile.objects.filter(auth_token=auth_token).first()
        if profile:
            if profile.is_verified:
                messages.success(request, 'Account already verified')
                return redirect('login')
            profile.is_verified = True
            profile.save()
            messages.success(request, 'Account successfully verified')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('')


def error_page(request):
    return  render(request , 'users/error.html')


def send_mail_after_registration(email , auth_token):
    subject = 'Account Verification'
    message = f'Hi, visit the given link to verify your account http://127.0.0.1:8000/verify/{auth_token}'
    email_from = 'admin@admin.com'
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list )


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = User.objects.filter(username=username).first()
                if user is not None:
                    profile = Profile.objects.filter(user=user).first()
                    if not profile.is_verified:
                        messages.warning(request, 'Please verify your email before logging in.')
                        return redirect('login')
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect('home')
                else:
                    messages.warning(request, 'Invalid Credentials')
                    return redirect('login')
            else:
                messages.warning(request, 'Invalid Credentials')
                return redirect('login')
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'users/login_new.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.') 
    return redirect('home')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "users/password_reset_email.txt"
                    c = {
					"email": user.email,
					'domain': '127.0.0.1:8000',
					'site_name': 'AwesomeBlog',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@admin.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid Header Found')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    context = {
        "password_reset_form":password_reset_form
    }
    return render(request, 'users/password_reset.html', context)


@login_required(login_url=settings.LOGIN_URL)
def profile(request, slug):
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile was successfully updated.')
            return redirect('profile', slug=user)
        else:
            messages.error(request, 'Unable to complete request')
            return redirect('profile', slug=user)

    form = UserForm(instance=user)
    context = {
        'user': user,
        'form': form,
    }
    return render(request, 'users/profile.html', context)