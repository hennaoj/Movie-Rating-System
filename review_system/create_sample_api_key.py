from review_system.models import ApiKey
from review_system import db
import click
from flask.cli import with_appcontext

def CreateSampleKey():
    token = "ea4bfdbe683994744fd665f90ac1f393"

    db_key = ApiKey(
        key = token,
    )

    db.session.add(db_key)
    db.session.commit()

    print(token)

@click.command("create-sample-api-key")
@with_appcontext
def create_sample_api_key():
    CreateSampleKey()
