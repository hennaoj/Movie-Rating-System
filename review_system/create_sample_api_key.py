'''Functionality for api key creation'''
import click
from flask.cli import with_appcontext
from review_system.models import ApiKey
from review_system import db

def create_sample_key():
    '''create a sample api key for testing'''
    token = "ea4bfdbe683994744fd665f90ac1f393"

    db_key = ApiKey(
        key = token,
    )

    db.session.add(db_key)
    db.session.commit()

    print("API-Key: " + token)

@click.command("create-sample-api-key")
@with_appcontext
def create_sample_api_key():
    '''click command to generate api key for testing'''
    create_sample_key()
