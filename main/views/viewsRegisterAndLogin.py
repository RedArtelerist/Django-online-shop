from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from ..forms import CreateUserForm
from django.contrib import messages
from ..models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View


# ------------------------------------   Register, Login    ----------------------------------------------------------------------------------
from ..utils import generate_token


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        form.is_active = False
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                email = form.cleaned_data.get('email')

                current_site = request.META['HTTP_HOST']
                print(current_site)
                email_subject ='Activate your account'
                message = render_to_string('main/auth/activate.html',
                                           {
                                               'user': user,
                                               'domain': current_site,
                                               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                               'token': generate_token.make_token(user)

                                           })

                email_message = EmailMessage(
                    email_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                )

                email_message.send()

                return redirect('verify_email')

        context = {'title': 'Register Account', 'form': form}
        for error in form.errors:
            print(form.errors[error])
        return render(request, 'main/register.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'main/login.html', context)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Email was confirmed')
            return redirect('login')
        return render(request, 'main/auth/activate_failed.html', status=401)


def verifyEmailPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'main/auth/verify_email.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')
