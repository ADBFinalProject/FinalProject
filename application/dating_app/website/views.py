from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import User, Dater


def index(request):
        return render(request, 'website/index.html', {})


@login_required
def home(request):
    return render(request, 'website/home.html', {})


@login_required
def my_account(request):
    return render(request, 'website/my_account.html', {})


@login_required
def search(request):
    return render(request, 'website/search.html', {})


@login_required
def match(request):
    return render(request, 'website/match.html', {})


@login_required
def get_match(request):
    min_age = request.POST.get('minAge', '')
    max_age = request.POST.get('maxAge', '')
    people_around = request.POST.get('around', 'off')
    looking_for = request.POST.getlist('lookingFor', '__empty__')
    if people_around == "off":
        print min_age, max_age, people_around, looking_for
        users = Dater.objects.all().exclude(username=request.user.username, is_superuser=True)
        if isinstance(min_age, int):
            users = users.filter(age__lte=min_age)
        if isinstance(max_age, int):
            users = users.filter(age__lte=max_age)
        if looking_for != "__empty__":
            final_users = set()  # Awful hack to solve one day...
            for user in users:
                for item in user.looking_for:
                    if item in looking_for:
                        final_users.add(user)
            users = list(final_users)
    else:
        return redirect('website:index') # Add neo4J request here
    print users
    paginator = Paginator(users, 2)  # Show 2 contacts per page
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'website/search.html', {'users': users})


def logout(request):
    auth.logout(request)
    return redirect('/')


def log_in(request):
    return render(request, 'website/login.html', {})


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
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
        print form
        if form.is_valid():
            print "is valid"
            user = form.save(commit=False)
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
