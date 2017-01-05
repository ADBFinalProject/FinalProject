from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import User


def index(request):
        return render(request, 'website/index.html', {})


@login_required
def home(request):
    return render(request, 'website/home.html', {})


@login_required
def my_account(request):
    return render(request, 'website/my_account.html', {})


@login_required
def match(request):
    return render(request, 'website/match.html', {})


@login_required
def get_match(request):
    print request.POST
    min_age = request.POST.get('minAge', '')
    max_age = request.POST.get('maxAge', '')
    people_around = request.POST.get('around', '')
    looking_for = request.POST.getlist('lookingFor', '')
    print min_age, max_age, looking_for, people_around
    return redirect('website:home')


def logout(request):
    auth.logout(request)
    return redirect('/')


def log_in(request):
    return render(request, 'website/login.html', {})


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print username, password
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('website:home')
    else:
        return redirect('website:index')


def signup(request):
    return render(request, 'website/signup.html', {})


class UserFormView(View):
    form_class = UserForm
    template_name = 'website/signup.html'

    # Display the form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # Process the form
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            print user.username
            print user.description
            # Cleaning and normalizing data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            mail = form.cleaned_data['email']
            user.set_password(password)
            user.save()
            new_usr = User(username=username,
                           password=password,
                           email=mail)
            new_usr.save()
            # returns User objects if the credential are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('website:home')
        return render(request, self.template_name, {'form': form})
