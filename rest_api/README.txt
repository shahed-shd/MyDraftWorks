The tasks to do are in "REST API Test.md" file.

Need to create a database in mysql.
Then in "model.py", to connect the database, change the line:
"engine = create_engine('mysql+pymysql://root:abcd1234@localhost/rest_api_test', echo=True)"

Here,
root is the username for mysql server.
abcd1234 is the password for that user in mysql.
@localhost indicates that the mysql server is in localhost.
rest_api_test is the name of the database to be connected.

No need to create any table in the database.
"model.py" will create the database tables according to its necessity.

Finally, Just need to run "flask_app.py" to get ready for responses to HTTP requests.
Flask will run in localhost, one can modify it in source code.

Dependencies:
- python (3.5.2)
- flask (1.0.2)
- mysql (5.7.22-0ubuntu0.16.04.1)
- sqlalchemy (1.2.7)
- pymysql (0.8.1)
- apscheduler (3.5.1)
