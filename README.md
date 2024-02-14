Clone the repo and cd to the project directory.

To run the app run `python manage.py runserver`

To make a admin account run the command `python manage.py createssuperuser` and enter the username and password.

To sync the database , remove all te pycache files and db.sqlite.
Run the following commands 
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py migrate --run-syncdb`
