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
```
cd review_system

python init_database.py

python create_sample_data.py
```

**Run API**
```
flask run
```
Server is open at `http://localhost:5000`


## Queries
**Routes**
- /api/movies/
- /api/movies/{id}
- /api/movies/{id}/reviews/
- /api/movies/{id}/reviews/<id}
- /api/genres/
- /api/genres/{id}/


<!-- __Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__ -->
