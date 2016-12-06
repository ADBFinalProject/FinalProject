import settings
from bs4 import BeautifulSoup
import re
import urllib, urllib2, cookielib, time
try:
    import simplejson as json
except (ImportError,):
    import json


MALES_NUMBER = 700
FEMALES_NUMBER = 300
MATCH_URL = 'https://www.okcupid.com/match'
PROFILE_URL = 'https://www.okcupid.com/profile/{0}'


def get_cookie(gender):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    if gender == 'M':
        print "Load: {0}".format(settings.username_male)
        login_data = urllib.urlencode({'username' : settings.username_male, 'password' : settings.password_male})
    else:
        print "Load: {0}".format(settings.username_female)
        login_data = urllib.urlencode({'username' : settings.username_female, 'password' : settings.password_female})
    opener.open('https://www.okcupid.com/login', login_data)
    return opener


def get_html_text(opener, url):
    response = opener.open(url)
    html_text = str(response.read())
    return html_text


def clean_data(html_text):
    raw_data = html_text.split('addBundles(')
    raw_data = raw_data[1].split('util.executeDomLoad();')
    cleaned_data = ''
    open_bracket = 0
    for character in raw_data[0]:
        cleaned_data = cleaned_data + character
        if character == '[':
            open_bracket += 1
        if character == ']':
            open_bracket -= 1
        if open_bracket == 0 and character == ']':
            break
    cleaned_data = cleaned_data.strip()
    python_data = json.loads(cleaned_data)
    return python_data


def get_user_basic_info(user_gender_limit, gender, cookies):
    dict_of_users = {}
    while len(dict_of_users) < user_gender_limit:
        print len(dict_of_users)
        time.sleep(5)
        html_text = get_html_text(cookies, MATCH_URL)
        data = clean_data(html_text)
        for user in data[1]['params'][0]['data']:
            if user['username'] not in dict_of_users:
                dict_of_users[user['username']] = {'id' : user['userid'],
                                                   'gender': user['userinfo']['gender'],
                                                   'age': user['userinfo']['age'],
                                                   'rel_status': user['userinfo']['rel_status'],
                                                   'orientation': user['userinfo']['orientation'],
                                                   'location': user['userinfo']['location'],
                                                   'picture': user['thumbs'][0]['800x800']}
    return dict_of_users


def get_user_data(opener, user, user_data):
    data = {}
    user_url = PROFILE_URL.format(user.encode('utf-8'))
    html_text = get_html_text(opener, user_url)
    soup = BeautifulSoup(html_text, 'html.parser')
    if not soup.findAll("div", { "class" : "blank_state helvetica no_buttons" }):
        title_sections = soup.findAll("div", { "class" : "essays2015-essay-title profilesection-title" })
        text_sections = soup.findAll("div", { "class" : "essays2015-essay-content" })
        for index, title in enumerate(title_sections):
            data[title.text] = ", ".join(text_sections[index].strings)
    looking_for = soup.find("div", { "class" : "lookingfor2015-sentence" }).text.split(',')
    data['looking_for'] = looking_for
    data['user_url'] = user_url
    for key in user_data:
        data[key] = user_data[key]
    return data


def launch_crawler(dict_of_users, cookies):
    for user, user_data in dict_of_users.iteritems():
        print user
        data = get_user_data(cookies, user, user_data)
        dict_of_users[user] = data
        time.sleep(5)
    return dict_of_users


def safe_data(dict_of_users, file_title):
    output = json.dumps( dict_of_users, ensure_ascii=False, encoding='utf8')
    with open("data/{0}.json".format(file_title), "w+") as save:
        save.write(output.encode('utf8'))

# This is a sample of how to use the code
# You need to configure an okcupid account to log to the website.
# Use a settings file with your password and login
"""
gender = 'M'
user_wanted = 310
cookies = get_cookie(gender)
dict_of_male_user = get_user_basic_info(user_wanted, gender, cookies)
dict_of_male_user = launch_crawler(dict_of_male_user, cookies)
safe_data(dict_of_male_user, "NY_female")
"""
