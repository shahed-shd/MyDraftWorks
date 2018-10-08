## Resource links:
  - https://docs.djangoproject.com/en/2.1/intro/tutorial01/

## Notes:
- To view **version**, command in terminal:
`python3 -m django --version`
**or**
`django-admin version`
**Or** in the interpreter:
```python
import django
django.get_version()
```

- To **start** a project, command:
`django-admin startproject mysite`

- To **run** the development server, command:
`python3 manage.py runserver`
By default, server will run at 127.0.0.1:8000
The default *IP* and *port* can be changed mentioning those at the last of the command.

- To **create** app, command:
`python3 manage.py startapp polls`
Here `polls` is the name of the app.
- To create any necessary database tables according to the database **settings** in your `mysite/settings.py` file and the database migrations shipped with the app, command:
`python3 manage.py migrate`

- To tell Django that there's some **changes in my model** and l like the changes to be stored as *migration*, command:
`python3 manage.py makemigrations polls`

- The **sqlmigrate** command takes migration names and returns their SQL. Command:
`python3 manage.py sqlmigrate polls 0001`

- To **check** for any problem in project without making migrations or touching the database, command:
`python manage.py check`

- To invoke the **Python shell**, use this command:
`python3 manage.py shell`

- Creating an **admin** user:
`python3 manage.py createsuperuser`
