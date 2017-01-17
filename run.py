from os import environ
from os.path import exists
import warnings

from flask import Flask
from flask.exthook import ExtDeprecationWarning

from core.flask import FlaskApp


warnings.simplefilter('ignore', ExtDeprecationWarning)


app = FlaskApp()

app.config.from_pyfile('settings/dist.py')
if exists('settings/local.py'):
    app.config.from_pyfile('settings/local.py')

from apps import AppsApp
apps = AppsApp(app)

from users import UsersApp
users = UsersApp(app)

from datastore import DatastoreApp
datastore = DatastoreApp(app)
