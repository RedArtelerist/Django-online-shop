from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from ..forms import CreateUserForm
from django.contrib import messages
from ..models import *

from django.contrib.auth import authenticate, login, logout


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('store')

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')

            Customer.objects.create(user=user, email=email, name=firstname + " " + lastname,)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')


    context = {'form': form}
    return render(request, 'main/registrationAndAuthorization/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'username or password is incorrect')
            # render(request, 'main/registrationAndAuthorization/login.html', context)

    context = {}
    return render(request, 'main/registrationAndAuthorization/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
