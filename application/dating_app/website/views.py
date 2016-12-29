from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from .models import User


def index(request):
        return render(request, 'website/index.html', {})


def home(request):
        return render(request, 'website/home.html', {})


def log_in(request):
        return render(request, 'website/login.html', {})


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

                        # Cleaning and normalizing data
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
                        mail = form.cleaned_data['email']

                        user.set_password(password)
                        user.save()
                        new_usr = User(username=username,
                                       password=password,
                                       email=mail).save()
                        new_usr.save()

                        # returns User objects if the credential are correct
                        user = authenticate(username=username, password=password)
                        if user is not None:
                                if user.is_active:
                                        login(request, user)
                                        return redirect('website:home')
                return render(request, self.template_name, {'form': form})
