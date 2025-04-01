# django-elearning-app
This is an elearning application developed with Django and SQLite.

## Setting up the application
The first step to set up the application after unzipping the folder is to install the packages in the requirements.txt file. This can be done in the command prompt by directing to the location of the project folder and running:
````
pip install -r requirements.txt
````

After installing the packages, migrate changes to ensure that the tables in the database are up to date.
This can be done by running the following commands:
````
python3 manage.py makemigrations
python3 manage.py migrate
````

## Starting the server
In order to use the websocket, run the Redis server and run the project on the Daphne server.
The steps to do this on the Windows OS:
1. Run Linux
2. Open the command prompt and run:
````
wsl --install
````
4. Start Redis
On Linux, run:
````
sudo service redis-server start
````
5. Start the Daphne server

Open a new tab in the command prompt

Redirect to the project location

Activate the virtual environment
````
.\<env name>\Scripts\activate
````
Run the command:
````
daphne <project name>.asgi:application
````
In this case the project name is Endtermproj
