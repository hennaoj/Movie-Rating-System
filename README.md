#### PWP SPRING 2023
# Movie Rating System

## Group information
* Henna Ojala hennaojala99@gmail.com
* Joona Meriläinen jmerilai19@student.oulu.fi
* Joonas Sutinen jsutinen18@student.oulu.fi

## Setup
**Requirements**
- Python3 and PIP

### Repository setup
**Install required packages**
```
pip install -r requirements.txt
```

**Create sample data for testing**


on Windows:
```
set FLASK_APP=review_system
set FLASK_ENV=development
flask init-db
flask create-sample-data
flask create-sample-api-key
```
on Linux:
```
export FLASK_APP=review_system
export FLASK_ENV=development
flask init-db
flask create-sample-data
flask create-sample-api-key
```

**Run API**
```
flask run
```
Server is open at `http://localhost:5000`

**Run unit tests**
```
python -m pytest ./testing/testing.py
```
**Get unit test coverage**
```
coverage run -m pytest ./testing/testing.py
coverage html
```


## Queries
**Routes**
- /api/movies/
- /api/movies/{id}/
- /api/movies/{id}/reviews/
- /api/movies/{id}/reviews/{id}/
- /api/genres/
- /api/genres/{id}/

## Client
Start client
```
cd client
python revsys.py
```

<!-- __Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__ -->
