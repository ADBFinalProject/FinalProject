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
python manage.py migrate
python manage.py createsuperuser
# Follow the instruction
```
Now you should be able to run the server:

```
python manage.py runserver
```
Go on: http://127.0.0.1:8000/

If you want to access to the admin interface:

Go on: http://127.0.0.1:8000/admin

# Design of the project

![alt tag](https://github.com/ADBFinalProject/FinalProject/img/index)
![alt tag](https://github.com/ADBFinalProject/FinalProject/img/login)


