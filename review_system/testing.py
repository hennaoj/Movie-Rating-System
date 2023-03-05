import requests
import json

dictionary = {"release_year": 1974, "title": "The Godfather2"}
print(requests.put('http://127.0.0.1:5000/api/movies/2/', json = json.dumps(dictionary)))

dictionary = {"release_year": 1972, "title": "The Godfather"}
print(requests.put('http://127.0.0.1:5000/api/movies/2/', json = json.dumps(dictionary)))

dictionary = {"release_year": 1974, "title": "The Godfather 2"}
print(requests.post('http://127.0.0.1:5000/api/movies/', json = json.dumps(dictionary)))
