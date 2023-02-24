from app import db
from app import app

# initialize the database
ctx = app.app_context()
ctx.push()
db.create_all()
ctx.pop()
