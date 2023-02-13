from app import db, Movie, User, Genre, Review
from datetime import datetime
from app import app

ctx = app.app_context()
ctx.push()

# genres
g1 = Genre(name="Action")
g2 = Genre(name="Drama")
g3 = Genre(name="Crime")

# movies
m1 = Movie(
     title="The Dark Knight",
     year=2008,
     description="The Dark Knight follows the story of Batman (Christian Bale) as he faces a new threat in the form of the Joker (Heath Ledger), a criminal mastermind with a plan to bring chaos to Gotham City. "
)

# add genres to the movie
m1.genres.append(g1)
m1.genres.append(g2)
m1.genres.append(g3)

# users
u1 = User(
    username="bob123",
    age=25,
    gender=1,
    account_creation_date=datetime.now()
)

# reviews
r1 = Review(
    rating=9,
    comment="This movie is awesome!",
    date=datetime.now(),
)
m1.reviews.append(r1) # add the review to the movie
u1.reviews.append(r1) # add the review to the user

# add all objects to the database session
db.session.add(m1)
db.session.add(u1)
db.session.add(g1)
db.session.add(g2)
db.session.add(g3)

# commit the changes
db.session.commit()
ctx.pop()
