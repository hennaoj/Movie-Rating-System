import requests
import json
import os
import pytest
import tempfile
from review_system import create_app, db
from review_system.create_sample_data import PopulateTestDb

@pytest.fixture(scope="session")
def app():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    app = create_app(config)
    with app.app_context():
        db.create_all()
        PopulateTestDb()
        
    yield app
    
    os.close(db_fd)
    os.unlink(db_fname)

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

class TestMovieCollection(object):
    def test_get(self, client):
        resp = client.get("/api/movies/")
        assert resp.status_code == 200
        listofmovies = json.loads(resp.data)
        assert len(listofmovies) == 2
        for item in listofmovies:
            assert "title" in item
            assert "release year" in item
    def test_post(self, client):
        newmovie =  {"title":"The Godfather 2", "release_year":1974, "description":"Part 2"}
        resp = client.post("/api/movies/", json=json.dumps(newmovie))
        assert resp.status_code == 201