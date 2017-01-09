# Purpose of this project

Welcome on our Final project for the Advanced database course.

The project is to build a dating app. We also need to fill it with 1000 users.

So we implemented a crawler that crawl the data from OkCupid via 2 fake accounts.

We in total collect 3000 users.

To build the application we used: Django and Neo4J.

# Usage

To download the project:

```
git clone https://github.com/ADBFinalProject/FinalProject
cd FinalProject
```
Now you will have to use the virtual environement.

```
pip install virtualenv
virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
```
Now let's launch the application:

```
cd application/dating_app
python manage.py migrate --run-syncdb
python manage.py createsuperuser
# Follow the instruction
```
Now you should be able to run the server:

```
python manage.py runserver
```

Don't forget to migrate user data

```
cd ../../jobs/data_migration
python insertion_data_mySQL.py
python add_UserNodes.py
python user_location_rel.py
python add_init_usr_rel.py
```

Now you can start the application !!

Go on: http://127.0.0.1:8000/

If you want to access to the admin interface:

Go on: http://127.0.0.1:8000/admin

# Design of the project

Our main page look like that:
![alt tag](https://raw.githubusercontent.com/ADBFinalProject/FinalProject/master/img/index.png)

This is the login page
![alt tag](https://raw.githubusercontent.com/ADBFinalProject/FinalProject/master/img/login.png)


