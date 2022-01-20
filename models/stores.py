from datetime import date, datetime
from sqlite3 import Date
from db import db

class Stores(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    store_address = db.Column(db.Text, nullable=False)
    store_city = db.Column(db.String(100),nullable=False)
    store_state = db.Column(db.String(100), nullable=False)
    store_pincode = db.Column(db.String(10), nullable=False)
    store_country = db.Column(db.String(100), nullable=False)
    delete = db.Column(db.Integer, default=0)

    def save_store(self):
        db.session.add(self)
        db.session.commit()

