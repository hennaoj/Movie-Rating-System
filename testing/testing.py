import requests
import json
import os
import pytest
import tempfile
from review_system import create_app, db
from review_system.create_sample_data import PopulateTestDb
from review_system.create_sample_api_key import CreateSampleKey

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
        CreateSampleKey()
        
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
        resp = client.post("/api/movies/", json=newmovie, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 201
        resp = client.post("/api/movies/", json={"title": "The Godfather 2"}, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 400
        resp = client.get("/api/movies/")
        assert resp.status_code == 200
        listofmovies = json.loads(resp.data)
        assert len(listofmovies) == 3
        newmovie =  {"title":"The Godfather 2", "release_year":"1974", "description":"Part 2"}
        resp = client.post("/api/movies/", data=newmovie, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
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
        resp = client.post("/api/movies/", data=editedmovie, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
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
        resp = client.post("/api/genres/", json=newgenre, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 201
        resp = client.get("/api/genres/")
        assert resp.status_code == 200
        listofgenres = json.loads(resp.data)
        assert len(listofgenres) == 4
        resp = client.post("/api/genres/", data=newgenre, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 415

class TestGenreItem(object):
    def test_get(self, client):
        resp = client.get("/api/genres/1/")
        assert resp.status_code == 200

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
        resp = client.get("/api/movies/1/")
        assert resp.status_code == 200
        movie = json.loads(resp.data)
        assert movie["average rating"] == "3.0"
        newreview = {"rating":4}
        resp = client.post("/api/movies/1/reviews/", json=newreview, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 201
        resp = client.post("/api/movies/1/reviews/", json=newreview)
        assert resp.status_code == 401
        resp = client.get("/api/movies/1/reviews/")
        assert resp.status_code == 200
        listofreviews = json.loads(resp.data)
        assert len(listofreviews) == 3
        assert listofreviews[-1]["rating"] == '4'
        resp = client.get("/api/movies/1/")
        assert resp.status_code == 200
        movie = json.loads(resp.data)
        assert movie["average rating"] == str(3 + 1/3)
        resp = client.post("/api/movies/1/reviews/", json="", headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 415
        #test posting with invalid data
        badreview = {"rating":"four"}
        resp = client.post("/api/movies/1/reviews/", json=badreview, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 400

class TestReviewItem(object):
    def test_get(self, client):
        resp = client.get("/api/movies/1/reviews/1/")
        assert resp.status_code == 200
        assert json.loads(resp.data)["comment"] == "This movie is awesome!"
