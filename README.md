# web-plant-phenotyping

GENERAL INSTRUCTIONS:

1) In the root directory, find and install req.txt. It contains all necessary packages.
2) Within the same directory, the following commands can be executed:

python3 manage.py runserver (to start the local server)
python3 manage.py makemigrations (to convert the python models into SQL instructions)
python3 manage.py migrate (to execute the converted SQL instructions in database)
python3 manage.py createsuperuser (to create superuser, to access admin panel)


ROOT DIRECTORY:

1) leaf_counter_projects contains the project configuration files.
2) prediction contains the app logical functions, links backend python, AI model to frontend templates.
3) readme.md contains the instructions.
4) config.ini contains the Cloudinary API credentials.
5) db.sqlite3 is an in-app database which saves user history.
6) manage.py is “the brain” of Django. Interact with Django using commands such as the ones mentioned above.
7) req.txt contains dependency (python packages) information needed to install and run the application.


LEAF_COUNT_PROJECT:

This is the project’s configuration and integration hub.
1) settings.py contains database, app information.
2) urls.py contains the routing instructions for the web app.

PREDICTION:

1) ai_model contains the two necessary files (.h5 and .json) to load the ML model in Keras for prediction.
2) migrations contains files generated by the python3 manage.py makemigrations command. This uses models.py which holds information on the database table. Migration files are created when changes are found.
3) static contains frontend related files such as images, CSS, JS, Bootstrap.
4) template contains all the html files necessary for the web app.
5) init.py is an empty file needed to convert an ordinary folder to act like a python package.
6) admin.py contains admin panel information.
7) models.py contains all information on the database table and its column types.
8) urls.py contains the url routes for the views.py functions.
9) views.py is “the heart” of Django. It links backend functions with html templates using url routes. It also handles all http methods for incoming and outgoing requests.
