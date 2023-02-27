from flask_sqlalchemy import SQLAlchemy
from app import app

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
    title = db.Column(db.String(64), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(512))
    average_rating = db.Column(db.Float) 

    # movie-genre relationship
    genres = db.relationship("Genre", secondary="movie_genre", back_populates="movies")

    # one-to-many relationship with movie-reviews
    reviews = db.relationship("Review", back_populates="movie")

    def UpdateRating(self):
        try:
            ratings = []
            for review in self.reviews:
                ratings.append(float(review.rating))
            if len(ratings) > 0:
                self.average_rating = sum(ratings)/len(ratings)
            return()
        except:
            return()

    def Serialize(self):
        moviedict = {
            "title": self.title,
            "release year": str(self.release_year),
            "description": self.description,
            "average rating": str(self.average_rating),
            "genres": ", ".join([genre.name for genre in self.genres]),
            "reviews": ", ".join([str(review.rating) for review in self.reviews])
        }
        return moviedict
        
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["title", "release_year"]
        }
        props = schema["properties"] = {}
        props["title"] = {
            "description": "Title of the movie",
            "type": "string"
        }
        props["release_year"] = {
            "description": "The release year of the movie",
            "type": "integer",
            "minimum": 1888,
            "maximum": 2023
        }
        props["description"] = {
            "description": "Summary/description of the movie",
            "type": "string"
        }
        props["average_rating"] = {
            "description": "Average rating based on movie reviews",
            "type": "integer"
        }
        props["genres"] = {
            "descriptions": "A list of genres the movie belongs to",
            "type": "array"
        }
        return schema

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    # many-to-many relationship with movies-genres
    movies = db.relationship("Movie", secondary="movie_genre", back_populates="genres")

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(512))
    date = db.Column(db.DateTime, nullable=False)

    # one-to-many relationship with movie-reviews
    movie = db.relationship("Movie", back_populates="reviews")
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)

    # one-to-many relationship with user-reviews
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="reviews")

    def Serialize(self):
        reviewdict = {
            "rating": str(self.rating),
            "comment": self.comment,
            "date": str(self.date),
            "movie": self.movie.title,
            "user": self.user.username
        }
        return reviewdict

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["rating"]
        }
        props = schema["properties"] = {}
        props["rating"] = {
            "description": "A 1-5 rating of the movie",
            "type": "integer",
            "minimum": 1,
            "maximum": 5
        }
        props["date"] = {
            "description": "The date/time the review was added",
            "type": "string",
            "pattern": "(\\d{4})-(\\d{2})-(\\d{2})[T](\\d{2}):(\\d{2}):(\\d{2})[+](\\d{2}):(\\d{2})"
        }
        props["comment"] = {
            "description": "Written review of the movie",
            "type": "string"
        }
        return schema

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False) # 1= male, 2 = female, 3 = other
    account_creation_date = db.Column(db.DateTime, nullable=False)

    # one-to-many relationship with user-reviews
    reviews = db.relationship("Review", back_populates="user")

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["username", "age", "gender", "account_creation_date"]
        }
        props = schema["properties"] = {}
        props["username"] = {
            "description": "The username of the user",
            "type": "string"
        }
        props["age"] = {
            "description": "The age of the user in years",
            "type": "integer",
            "minimum": 0,
            "maximum": 130
        }
        props["gender"] = {
            "description": "Gender of the insipired by ISO/IEC 5218",
            "type": "integer",
            "minimum": 1,
            "maximum": 3
        }
        props["account_creation_date"] = {
            "description": "The date/time when the user was added to the database",
            "type": "string",
            "pattern": "(\\d{4})-(\\d{2})-(\\d{2})[T](\\d{2}):(\\d{2}):(\\d{2})[+](\\d{2}):(\\d{2})"
        }
        return schema