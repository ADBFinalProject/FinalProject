from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.urlresolvers import reverse


def index(request):
    return render(request, 'website/index.html', {})


@login_required
def home(request):
    res = reverse('website/home.html', args=[request.user.username])
    print res, "looolooooolool"
    return HttpResponseRedirect()


def logout(request):
    print("hell yes")
    auth.logout(request)
    return redirect('/')


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
            print user.username
            print user.description
            # Cleaning and normalizing data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if the credential are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('website:home')
        return render(request, self.template_name, {'form': form})
