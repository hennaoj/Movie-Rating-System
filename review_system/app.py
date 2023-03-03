from flask import Flask

# init stuff
app = Flask(__name__)

from models import db, Movie, Genre, Review, User
from api import api
