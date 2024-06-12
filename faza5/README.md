# PROJECT SETUP 
Download project and open ./faza5 in PyCharm.

Open terminal in PyCharm.


### VIRTUAL ENVIRONMENT SETUP
To create a new virtual environment named "my_env", 
run the following command in terminal:
```commandline
python -m venv my_env
```
Note that it is important to name the virtual environment "my_env"


To activate new virtual environment, run:
```commandline
 my_env\Scripts\activate
```

To download necessary python packages, run:
```commandline
pip install django

pip install requests

pip install mysqlclient

pip install translators
```

To set up my_env as the interpreter:


Click on Python 3.x in the bottom right corner of PyCharm, 
then click on "Add new interpreter" then "Add local interpreter", navigate to virtual environment
then choose "Existing environment" and specify the path to my_env/Scripts/python.exe


### LOCAL SECRETS SETUP

In the directory ./faza5 create a file named ```localSecrets.py```.

In this file add necessary information:
```python
# database settings
DB_HOST = ...
DB_PORT = ...
DB_USER = ...
DB_PASSWORD = ...

# email settings
EMAIL_HOST_USER = ...
EMAIL_HOST_PASSWORD = ...

# OMDB api key
OMDB_API_KEY = ...
```
Note that this file should always stay out of Gerrit repo.

### DATABASE SETUP

To connect with the database from Django project, run following commands in terminal:
```commandline
python manage.py inspectdb > cineverse/models.py

python manage.py makemigrations

python manage.py migrate
```

In order to locally connect to the database, open MySQL Workbench 
and create a new connection using the necessary information.


# RUNNING THE APPLICATION

To run the application, run the following command in terminal:
```commandline
python manage.py runserver
```

# PLUGINS
In order to make sequence diagrams, install Mermaid plugin or extension.