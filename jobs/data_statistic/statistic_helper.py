import json
import plotly.offline as po
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
po.offline.init_notebook_mode()

def generate_box_plot(dictionary, title):
    data = []
    for gender, ages in dictionary.iteritems():
        x = []
        y = []
        for age, list_values in ages.iteritems():
            x = x + [age for value in list_values]
            y = y + list_values
        if gender == 'Men':
            color = 'rgb(7, 73, 239)'
        else:
             color = 'rgb(239, 98, 225)'
        trace = go.Box(
            y=y[10:-10],
            x=x[10:-10],
            name=gender,
            boxpoints='suspectedoutliers',
            marker = dict(
                color = color,
            )
        )
        data.append(trace)
    layout = go.Layout(
        title=title,
        yaxis=dict(
            title='Age difference'
        ),
        xaxis=dict(
            title='Age of the category',
            dtick=1
        ),
        boxmode='group'
    )
    fig = go.Figure(data=data, layout=layout)
    po.iplot(fig)

def generate_bar_chart(labels, colors, *args):
    titlelizer = True
    values = []
    titles = []
    data = []
    for arg in args:
        if titlelizer:
            titles.append(arg)
            titlelizer = False
        else:
            values.append(arg)
            titlelizer = True
    for index, value in enumerate(values):
        trace = go.Bar(
            x = labels,
            y= value,
            name=titles[index],
            marker=dict(
                color=colors[index]
            )
        )
        data.append(trace)
    layout = go.Layout(
        barmode='group'
    )
    fig = go.Figure(data=data, layout=layout)
    po.iplot(fig, filename='angled-text-bar')


def generate_histograms(title, colors, *args):
    data = []
    labelizer = False
    values = []
    labels = []
    for arg in args:
        if labelizer:
            labels.append(arg)
            labelizer = False
        else:
            values.append(arg)
            labelizer = True
    for index, label in enumerate(labels):
        trace = go.Histogram(
                    x=values[index][15:-15],
                    opacity=0.90,
                    name=label,
                    marker=dict(
                        color=colors[index]
                    ),
                    histnorm='probability'
                )
        data.append(trace)
    layout = go.Layout(
        title=title,
        barmode='group'
    )
    fig = go.Figure(data=data, layout=layout)
    po.iplot(fig)

def generate_pie(dictionary, title):
    pie_values = []
    labels = []
    for key, value in dictionary.iteritems():
        pie_values.append(value)
        labels.append(key)
    fig = {
    'data': [{'labels': labels,
              'values': pie_values,
              'type': 'pie'}],
    'layout': {'title': title}
     }

    po.iplot(fig)

def load_data_from_file(file_name):
    with open('../../data/{0}.json'.format(file_name)) as data_file:
        data = json.load(data_file)
    return data

def safe_data(dict_of_users, file_title):
    output = json.dumps( dict_of_users, ensure_ascii=False, encoding='utf8')
    with open("../../data/{0}.json".format(file_title), "w+") as save:
        save.write(output.encode('utf8'))


all_users = load_data_from_file('all_users_cleaned')

nb_users = len(all_users)
nb_women = 0
nb_men = 0
list_age_women_distribution = []
list_age_men_distribution = []
list_age_min_men_distribution = []
list_age_min_women_distribution = []
list_age_max_men_distribution = []
list_age_max_women_distribution = []
rel_status = {}
orientation = {}
casual_sex_women = 0
casual_sex_men = 0
friend_women = 0
friend_men = 0
short_women = 0
short_men = 0
long_women = 0
long_men = 0
near_men = 0
near_women = 0
max_age_per_age = {'Women':{}, 'Men': {}}
min_age_per_age = {'Women':{}, 'Men': {}}

for user, dictionary in all_users.iteritems():
   age_expectations = dictionary['looking_for']['age']
   age_expectations = age_expectations.split('-')
   age_expectations = dictionary['looking_for']['age']
   age_expectations = age_expectations.split('-')
   age = dictionary['age']
   if dictionary['gender'] == 'Woman':
       if age in max_age_per_age['Women']:
           max_age_per_age['Women'][age].append(age - int(age_expectations[1]))
       else:
           max_age_per_age['Women'][age] = [age - int(age_expectations[1])]
       if age in min_age_per_age['Women']:
           min_age_per_age['Women'][age].append(age - int(age_expectations[0]))
       else:
           min_age_per_age['Women'][age] = [age - int(age_expectations[0])]
       list_age_min_women_distribution.append(int(age_expectations[0]))
       list_age_max_women_distribution.append(int(age_expectations[1]))
       nb_women += 1
       list_age_women_distribution.append(dictionary['age'])
       if 'casual_sex' in dictionary['looking_for']:
           casual_sex_women += 1
       if 'friend' in dictionary['looking_for']:
           friend_women += 1
       if 'long_term' in dictionary['looking_for']:
           long_women += 1
       if 'short_term' in dictionary['looking_for']:
           short_women += 1
       if dictionary['looking_for']['near'] == True:
           near_women += 1
   else:
       if age in max_age_per_age['Men']:
           max_age_per_age['Men'][age].append(age - int(age_expectations[1]))
       else:
           max_age_per_age['Men'][age] = [age - int(age_expectations[1])]
       if age in min_age_per_age['Men']:
           min_age_per_age['Men'][age].append(age - int(age_expectations[0]))
       else:
           min_age_per_age['Men'][age] = [age - int(age_expectations[0])]
       if 'casual_sex' in dictionary['looking_for']:
           casual_sex_men += 1
       if 'friend' in dictionary['looking_for']:
           friend_men += 1
       if 'long_term' in dictionary['looking_for']:
           long_men += 1
       if 'short_term' in dictionary['looking_for']:
           short_men += 1
       if dictionary['looking_for']['near'] == True:
           near_men += 1
       list_age_min_men_distribution.append(int(age_expectations[0]))
       list_age_max_men_distribution.append(int(age_expectations[1]))
       nb_men += 1
       list_age_men_distribution.append(dictionary['age'])
   if dictionary['rel_status'] not in rel_status:
       rel_status[dictionary['rel_status']] = 1
   else:
       rel_status[dictionary['rel_status']] += 1
   if dictionary['orientation'] not in orientation:
       orientation[dictionary['orientation']] = 1
   else:
       orientation[dictionary['orientation']] += 1

list_age = sorted(list_age_women_distribution + list_age_men_distribution)
list_age_min_men_distribution = sorted(list_age_min_men_distribution)
list_age_max_men_distribution = sorted(list_age_max_men_distribution)
list_age_min_women_distribution = sorted(list_age_min_women_distribution)
list_age_max_women_distribution = sorted(list_age_max_women_distribution)
list_age_men_distribution = sorted(list_age_men_distribution)
list_age_women_distribution = sorted(list_age_women_distribution)
casual_sex_women = casual_sex_women * 100.0 / float(nb_women)
casual_sex_men = casual_sex_men * 100.0 / float(nb_men)
friend_women = friend_women * 100.0 / float(nb_women)
friend_men = friend_men * 100.0 / float(nb_men)
short_women = short_women * 100.0 / float(nb_women)
short_men = short_men * 100.0 / float(nb_men)
long_women = long_women * 100.0 / float(nb_women)
long_men = long_men * 100.0 / float(nb_men)
near_women = near_women * 100.0 / float(nb_women)
near_men = near_men * 100.0 / float(nb_men)
list_wanted_female = [casual_sex_women, friend_women, short_women, long_women, near_women]
list_wanted_male = [casual_sex_men, friend_men, short_men, long_men, near_men]
