from app import app
from db import db

db.init_app(app)

# we can create the db and tables using sql alchemy 
@app.before_first_request
def create_table():
    db.create_all()