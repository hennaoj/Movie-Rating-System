'''Functionality to create sample data for testing purposes'''
from datetime import datetime
import click
from flask.cli import with_appcontext
from review_system import db
from review_system.models import Movie, User, Genre, Review

def populate_test_db():
    '''Function that populates the database with sample data'''
    # genres
    g_1 = Genre(name="Action")
    g_2 = Genre(name="Drama")
    g_3 = Genre(name="Crime")

    def add_genres(movie, genrelist):
        for genre in genrelist:
            movie.genres.append(genre)
        return()

    def add_review_to_movie_and_user(review, movie, user):
        movie.reviews.append(review)
        user.reviews.append(review)
        return()

    # movies
    m_1 = Movie(
         title="The Dark Knight",
         release_year=2008,
         description="The Dark Knight follows the story of Batman (Christian Bale) as he"\
                     " faces a new threat in the form of the Joker (Heath Ledger)"\
                     ", a criminal mastermind with a plan to bring chaos to Gotham City. ",
         uri_id="thedarkknight"
    )

    m_2 = Movie(
         title="The Godfather",
         release_year=1972,
         uri_id = "thegodfather"
         )

    # add genres to the movies
    add_genres(m_1, [g_1,g_2,g_3])
    add_genres(m_2, [g_2,g_3])

    # users
    u_1 = User(
        username="bob123",
        age=25,
        gender=1,
        account_creation_date=datetime.now()
    )

    u_2 = User(
        username="123bob321",
        age=52,
        gender=3,
        account_creation_date=datetime(2015, 2, 2)
    )

    # reviews
    r_1 = Review(
        rating=5,
        comment="This movie is awesome!",
        date=datetime.now(),
    )

    r_2 = Review(
        rating=1,
        comment="Bad movie",
        date=datetime(2015, 2, 3),
    )

    r_3 = Review(
        rating=3,
        comment="Decent movie",
        date=datetime(2018, 5, 3),
    )

    add_review_to_movie_and_user(r_1, m_1, u_1)
    add_review_to_movie_and_user(r_2, m_1, u_2)
    add_review_to_movie_and_user(r_3, m_2, u_2)

    m_1.update_rating()
    m_2.update_rating()

    # add all objects to the database session
    db.session.add(m_1)
    db.session.add(m_2)
    db.session.add(u_1)
    db.session.add(u_2)
    db.session.add(g_1)
    db.session.add(g_2)
    db.session.add(g_3)
    db.session.add(r_1)
    db.session.add(r_2)
    db.session.add(r_3)

    # commit the changes
    db.session.commit()

@click.command("create-sample-data")
@with_appcontext
def create_sample_data():
    '''Click command for database population'''
    populate_test_db()
