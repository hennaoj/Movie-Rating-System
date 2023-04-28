import json
import os
import pytest
import tempfile

from review_system import create_app, db
from review_system.create_sample_data import populate_test_db
from review_system.create_sample_api_key import create_sample_key

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
        populate_test_db()
        create_sample_key()
        
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

        resp_body = json.loads(resp.data)
        assert len(resp_body["items"]) == 2
        for item in resp_body["items"]:
            assert "title" in item
            assert "release year" in item

    def test_post(self, client):
        new_movie =  {"title":"The Godfather 2", "release_year":1974, "description":"Part 2"}
        resp = client.post("/api/movies/", json=new_movie, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 201

        resp = client.post("/api/movies/", json={"title": "The Godfather 2"}, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 400

        resp = client.get("/api/movies/")
        assert resp.status_code == 200

        listofmovies = json.loads(resp.data)
        assert len(listofmovies) == 3

        #testing invalid release year
        new_movie =  {"title":"The Godfather 2", "release_year":"1974", "description":"Part 2"}
        resp = client.post("/api/movies/", data=new_movie, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 415

        #testing adding a movie with the same name
        new_movie =  {"title":"The Godfather 2", "release_year":1974, "description":"Part 2"}
        resp = client.post("/api/movies/", json=new_movie, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 201

class TestMovieItem(object):
    def test_get(self, client):
        resp = client.get("/api/movies/thedarkknight/")
        assert resp.status_code == 200
        assert json.loads(resp.data)["title"] == "The Dark Knight"

    def test_patch(self, client):
        resp = client.get("/api/movies/thedarkknight/")
        assert resp.status_code == 200
        assert json.loads(resp.data)["release year"] == "2008"

        edited_movie =  {"title":"The Dark Knight", "release_year":2009}
        resp = client.patch("/api/movies/thedarkknight/", json=edited_movie, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 204
        
        resp = client.get("/api/movies/thedarkknight/")
        assert resp.status_code == 200
        assert json.loads(resp.data)["release year"] == "2009"

        resp = client.post("/api/movies/", data=edited_movie, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 415

        #movie_with_genres = {"title":"The Dark Knight", "release_year":2009, "genres": ["Adventure", "Scifi"]}
        #resp = client.post("/api/movies/", json=movie_with_genres, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        #assert resp.status_code == 204

    def test_delete(self, client):
        resp = client.get("/api/movies/thedarkknight/")
        assert resp.status_code == 200
        assert json.loads(resp.data)["title"] == "The Dark Knight"

        resp = client.delete("/api/movies/thedarkknight/", headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 200

        resp = client.get("/api/movies/thedarkknight/")
        assert resp.status_code == 404

class TestGenreCollection(object):
    def test_get(self, client):
        resp = client.get("/api/movies/genres/")
        assert resp.status_code == 200

        resp_body = json.loads(resp.data)
        assert len(resp_body["items"]) == 3
        for item in resp_body["items"]:
            assert "name" in item

    def test_post(self, client):
        new_genre =  {"name":"Horror"}
        resp = client.post("/api/movies/genres/", json=new_genre, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 201

        resp = client.get("/api/movies/genres/")
        assert resp.status_code == 200

        resp_body = json.loads(resp.data)
        assert len(resp_body["items"]) == 4

        resp = client.post("/api/movies/genres/", data=new_genre, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 415

class TestGenreItem(object):
    def test_get(self, client):
        resp = client.get("/api/movies/genres/action/")
        assert resp.status_code == 200

class TestReviewCollection(object):
    def test_get(self, client):
        resp = client.get("/api/movies/thedarkknight/reviews/")
        assert resp.status_code == 200

        resp_body = json.loads(resp.data)
        assert len(resp_body["items"]) == 2
        for item in resp_body["items"]:
            assert "rating" in item
            assert "date" in item

    def test_post(self, client):
        resp = client.get("/api/movies/thedarkknight/")
        assert resp.status_code == 200

        movie = json.loads(resp.data)
        assert movie["average rating"] == "3.0"

        new_review = {"rating":4}
        resp = client.post("/api/movies/thedarkknight/reviews/", json=new_review, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 201

        resp = client.post("/api/movies/thedarkknight/reviews/", json=new_review)
        assert resp.status_code == 401

        resp = client.get("/api/movies/thedarkknight/reviews/")
        assert resp.status_code == 200

        resp_body = json.loads(resp.data)
        assert len(resp_body["items"]) == 3
        assert resp_body["items"][-1]["rating"] == '4'

        resp = client.get("/api/movies/thedarkknight/")
        assert resp.status_code == 200

        movie = json.loads(resp.data)
        assert movie["average rating"] == str(3 + 1/3)

        resp = client.post("/api/movies/thedarkknight/reviews/", json="", headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 415
        
        #test posting with invalid data
        bad_review = {"rating":"four"}
        resp = client.post("/api/movies/thedarkknight/reviews/", json=bad_review, headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        print(resp)

class TestReviewItem(object):
    def test_get(self, client):
        resp = client.get("/api/movies/thedarkknight/reviews/1/")
        assert resp.status_code == 200
        assert json.loads(resp.data)["comment"] == "This movie is awesome!"

    def test_delete(self, client):
        resp = client.delete("/api/movies/thedarkknight/reviews/1/", headers={"API-Key":"ea4bfdbe683994744fd665f90ac1f393"})
        assert resp.status_code == 200

        resp = client.get("/api/movies/thedarkknight/reviews/1/")
        assert resp.status_code == 404
