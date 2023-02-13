from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init stuff
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie_rating_system.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# movies-genres many-to-many relationship table
movie_genre = db.Table("movie_genre",
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True)
)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256))

    # movie-genre relationship
    genres = db.relationship("Genre", secondary="movie_genre", back_populates="movies")

    # one-to-many relationship with movie-reviews
    reviews = db.relationship("Review", back_populates="movie")

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    # many-to-many relationship with movies-genres
    movies = db.relationship("Movie", secondary="movie_genre", back_populates="genres")

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(256))
    date = db.Column(db.DateTime, nullable=False)

    # one-to-many relationship with movie-reviews
    movie = db.relationship("Movie", back_populates="reviews")
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)

    # one-to-many relationship with user-reviews
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="reviews")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False) # 1= male, 2 = female, 3 = other
    account_creation_date = db.Column(db.DateTime, nullable=False)

    # one-to-many relationship with user-reviews
    reviews = db.relationship("Review", back_populates="user")
