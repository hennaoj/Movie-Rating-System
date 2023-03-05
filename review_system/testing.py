import requests
import json
import os
import pytest
import tempfile
from app import db, app
from create_sample_data import PopulateTestDb


dictionary = {"release_year": 1974, "title": "The Godfather2"}
print(requests.put('http://127.0.0.1:5000/api/movies/2/', json = json.dumps(dictionary)))

dictionary = {"release_year": 1972, "title": "The Godfather"}
print(requests.put('http://127.0.0.1:5000/api/movies/2/', json = json.dumps(dictionary)))

dictionary = {"release_year": 1974, "title": "The Godfather 2"}
print(requests.post('http://127.0.0.1:5000/api/movies/', json = json.dumps(dictionary)))


@pytest.fixture
def client():
    print("opkl")
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["TESTING"] = True

    db.create_all()
    PopulateTestDb()

    yield app.test_client()

    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)