import requests
import json
import os
import pytest
import tempfile
from review_system import create_app, db
from review_system.create_sample_data import PopulateTestDb

@pytest.fixture(scope="function")
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

@pytest.fixture(scope="function")
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
        resp = client.get("/api/movies/")
        assert resp.status_code == 200
        listofmovies = json.loads(resp.data)
        assert len(listofmovies) == 3
        newmovie =  {"title":"The Godfather 2", "release_year":"1974", "description":"Part 2"}
        resp = client.post("/api/movies/", data=newmovie)
        assert resp.status_code == 415

class TestMovieItem(object):
    def test_get(self, client):
        resp = client.get("/api/movies/1/")
        assert resp.status_code == 200
        assert json.loads(resp.data)["title"] == "The Dark Knight"
    def test_put(self, client):
        resp = client.get("/api/movies/1/")
        assert resp.status_code == 200
        assert json.loads(resp.data)["release year"] == "2008"
        editedmovie =  {"title":"The Dark Knight", "release_year":2009}
        resp = client.put("/api/movies/1/", json=json.dumps(editedmovie))
        assert resp.status_code == 204
        resp = client.get("/api/movies/1/")
        assert resp.status_code == 200
        assert json.loads(resp.data)["release year"] == "2009"
        resp = client.post("/api/movies/", data=editedmovie)
        assert resp.status_code == 415
    def test_delete(self, client):
        resp = client.get("/api/movies/1/")
        assert resp.status_code == 200
        assert json.loads(resp.data)["title"] == "The Dark Knight"
        resp = client.delete("/api/movies/1/")
        assert resp.status_code == 200
        resp = client.get("/api/movies/1/")
        assert resp.status_code == 404

class TestGenreCollection(object):
    def test_get(self, client):
        resp = client.get("/api/genres/")
        assert resp.status_code == 200
        listofgenres = json.loads(resp.data)
        assert len(listofgenres) == 3
        for item in listofgenres:
            assert "name" in item
    def test_post(self, client):
        newgenre =  {"name":"Horror"}
        resp = client.post("/api/genres/", json=json.dumps(newgenre))
        assert resp.status_code == 201
        resp = client.get("/api/genres/")
        assert resp.status_code == 200
        listofgenres = json.loads(resp.data)
        assert len(listofgenres) == 4
        resp = client.post("/api/genres/", data=newgenre)
        assert resp.status_code == 415

class TestReviewCollection(object):
    def test_get(self, client):
        resp = client.get("/api/movies/1/reviews/")
        assert resp.status_code == 200
        listofreviews = json.loads(resp.data)
        assert len(listofreviews) == 2
        for item in listofreviews:
            assert "rating" in item
            assert "date" in item
    def test_post(self, client):
        newreview = {"rating":4}
        resp = client.post("/api/movies/1/reviews/", json=json.dumps(newreview))
        assert resp.status_code == 201
        resp = client.get("/api/movies/1/reviews/")
        assert resp.status_code == 200
        listofreviews = json.loads(resp.data)
        assert len(listofreviews) == 3
        assert listofreviews[-1]["rating"] == '4'
