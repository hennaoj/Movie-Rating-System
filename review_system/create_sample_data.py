from app import Movie, User, Genre, Review
from datetime import datetime
from app import db, app

ctx = app.app_context()
ctx.push()

# genres
g1 = Genre(name="Action")
g2 = Genre(name="Drama")
g3 = Genre(name="Crime")

def AddGenres(movie, genrelist):
    for genre in genrelist:
        movie.genres.append(genre)
    return()

def AddReviewToMovieAndUser(review, movie, user):
    movie.reviews.append(review)
    user.reviews.append(review)
    return()

# movies
m1 = Movie(
     title="The Dark Knight",
     release_year=2008,
     description="The Dark Knight follows the story of Batman (Christian Bale) as he faces a new threat in the form of the Joker (Heath Ledger), a criminal mastermind with a plan to bring chaos to Gotham City. "
)

m2 = Movie(
     title="The Godfather",
     release_year=1972
     )

# add genres to the movies
AddGenres(m1, [g1,g2,g3])
AddGenres(m2, [g2,g3])

# users
u1 = User(
    username="bob123",
    age=25,
    gender=1,
    account_creation_date=datetime.now()
)

u2 = User(
    username="123bob321",
    age=52,
    gender=3,
    account_creation_date=datetime(2015, 2, 2)
)

# reviews
r1 = Review(
    rating=5,
    comment="This movie is awesome!",
    date=datetime.now(),
)

r2 = Review(
    rating=1,
    comment="Bad movie",
    date=datetime(2015, 2, 3),
)

r3 = Review(
    rating=3,
    comment="Decent movie",
    date=datetime(2018, 5, 3),
)

AddReviewToMovieAndUser(r1, m1, u1)
AddReviewToMovieAndUser(r2, m1, u2)
AddReviewToMovieAndUser(r3, m2, u2)

m1.UpdateRating()

# add all objects to the database session
db.session.add(m1)
db.session.add(m2)
db.session.add(u1)
db.session.add(u2)
db.session.add(g1)
db.session.add(g2)
db.session.add(g3)
db.session.add(r1)
db.session.add(r2)
db.session.add(r3)

# commit the changes
db.session.commit()
ctx.pop()



