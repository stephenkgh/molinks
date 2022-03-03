from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth

from molinks import forms


def login(request):
    # redirect out if user already logged in
    if request.user.is_authenticated:
        return redirect_next(request)

    errors = False
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is None:
                errors = True
            else:
                auth.login(request, user)
                return redirect_next(request)
    else:
        form = forms.LoginForm()

    return render(request, 'login.html', {'form': form, 'errors': errors})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


# ---- utility ---------------------------------------------------------------------------------------

def redirect_next(request):
    if 'next' in request.GET:
        return HttpResponseRedirect(request.GET['next'])
    else:
        return HttpResponseRedirect('/')
