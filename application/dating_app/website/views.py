from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import Dater
from neomodel import db
import re


def index(request):
        return render(request, 'website/index.html', {})


@login_required
def get_user_profile(request, username):
    user = Dater.objects.get(username=username)
    return render(request, 'website/user_profile.html', {"user":user})


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
    matched_user = []
    query = 'MATCH (a:user {user_id:"%s"}) ' \
            'OPTIONAL MATCH (b:user)' \
            'WHERE EXISTS ' % (request.user.username)
    #get_user_from_query(query)
    return render(request, 'website/match.html', {})


@login_required
def get_match(request):
    min_age = request.POST.get('minAge', '')
    max_age = request.POST.get('maxAge', '')
    people_around = request.POST.get('around', 'off')
    looking_for = request.POST.getlist('lookingFor', '__empty__')
    if request.method == "POST":
        request.session['people_around'] = people_around
        if people_around == "off":  # Own filter
            users = get_users_basic_filter(request)
            if isinstance(min_age, int):
                users = users.filter(age__gte=min_age)
                request.session['min_age'] = min_age
            else:
                request.session['min_age'] = 0
            if isinstance(max_age, int):
                users = users.filter(age__lte=max_age)
            else:
                request.session['max_age'] = 99
            if looking_for != "__empty__":
                final_users = set()  # Awful hack to solve one day...
                for user in users:
                    for item in user.looking_for:
                        if item in looking_for:
                            final_users.add(user)
                users = list(final_users)
                request.session['looking_for'] = looking_for
            else:
                request.session['looking_for'] = ['sex', 'friend', 'short_term', 'long_term']
        else:  # People around
            limit = '1000'
            query = build_neo4j_cyper_query(request.user, limit)
            users = get_user_from_query(query)
            request.session['people_around'] = people_around
    else:
        users = get_user_from_sessions(request)
    paginator = Paginator(users, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'website/search.html', {'users': users})


def build_neo4j_cyper_query(user, limit):
    if user.sexual_orientation == "bisexual":
        cmd = 'MATCH (a:user {user_id: "%s"}) ' \
              'OPTIONAL MATCH (b:user) ' \
              'WHERE not a.user_id = b.user_id ' \
              'RETURN b.user_id as username, distance(point(a), point(b)) as dist ' \
              'ORDER BY dist ' \
              'LIMIT %s ' % (user.username, limit)
    elif user.sexual_orientation == "gay":
        cmd = 'MATCH (a:user {user_id:\'%s\'}) ' \
              'OPTIONAL MATCH (b:user) ' \
              'WHERE not a.user_id = b.user_id AND a.gender=b.gender ' \
              'RETURN b.user_id , distance(point(a), point(b)) as dist ' \
              'ORDER BY dist ' \
              'LIMIT %s ' % (user.username, limit)
    else:
        cmd = 'MATCH (a:user {user_id:\'%s\'}) ' \
              'OPTIONAL MATCH (b:user) ' \
              'WHERE not a.user_id = b.user_id AND NOT a.gender=b.gender ' \
              'RETURN b.user_id , distance(point(a), point(b)) as dist ' \
              'ORDER BY dist ' \
              'LIMIT %s ' % (user.username, limit)
    return cmd


def get_user_from_query(query):
    users_neo4j = db.cypher_query(query)
    users_sqlite3 = Dater.objects.all()
    final_user_list = []
    for user_neo4j in users_neo4j[0]:
        for user_sql in users_sqlite3:
            if user_sql.username == user_neo4j[0]:
                final_user_list.append(user_sql)
                break
    return final_user_list


def get_user_from_sessions(request):
    if request.session['people_around'] == "on":
        query = build_neo4j_cyper_query(request.user, '1000')
        users = get_user_from_query(query)
    else:
        users = get_users_basic_filter(request)
        users = users.filter(age__gte=request.session['min_age'])
        users = users.filter(age__lte=request.session['max_age'])
        final_users = set()  # Awful hack to solve one day...
        for user in users:
            for item in user.looking_for:
                if item in request.session['looking_for']:
                        final_users.add(user)
        users = list(final_users)
    return users


def get_users_basic_filter(request):
    gender = request.user.gender
    sexual_orientation = request.user.sexual_orientation
    users = Dater.objects.all().exclude(username=request.user.username).exclude(is_superuser=True)
    if gender == "m":
        if sexual_orientation == "straight":
            users = users.filter(gender="w")
        if sexual_orientation == "gay":
            users = users.filter(gender="m")
    else:
        if sexual_orientation == "straight":
            users = users.filter(gender="m")
        if sexual_orientation == "gay":
            users = users.filter(gender="w")
    return users


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
        print form.errors
        if form.is_valid():
            user = form.save(commit=False)
            # Cleaning and normalizing data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            summary = form.cleaned_data['summary']
            age = int(form.cleaned_data['age'])
            gender = form.cleaned_data['gender']
            sexual_orientation = form.cleaned_data['sexual_orientation']
            looking_for = form.cleaned_data['looking_for']
            mail = form.cleaned_data['email']

            user.set_password(password)
            user.latitude = 24.8047
            user.longitude = 120.9714
            user.save()

            # create a user node in neo4j db
            cmd = 'CREATE (u:user {user_id:\'%s\', summary:\'%s\', age:%d, gender:\'%s\', orientation:\'%s\', email:\'%s\', latitude:%d, longitude:%d})' \
                  % (username, re.escape(summary), age, gender, sexual_orientation, mail, user.latitude, user.longitude)
            db.cypher_query(cmd)
            # add the label
            for target in looking_for:
                cmd = 'MATCH (u:user {user_id:\'%s\'}) SET u:%s' % (username, target)
                db.cypher_query(cmd)
            # returns User objects if the credential are correct
            user = authenticate(username=username, password=password)
            

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('website:home')
        return render(request, self.template_name, {'form': form})
