from datetime import date, datetime
from sqlalchemy import func
from sqlite3 import Date
from db import db

class Buyers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,nullable=False)
    name = db.Column(db.String(100),nullable=False)
    address = db.Column(db.Text,nullable=False)
    city = db.Column(db.String(100),nullable=False)
    state = db.Column(db.String(100),nullable=False)
    pincode = db.Column(db.String(10),nullable=False)
    country = db.Column(db.String(100),nullable=False)
    country_code = db.Column(db.String(5),nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100),unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    last_transaction_date = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        try:
            self.user_id = kwargs["user_id"]
            self.name = kwargs["name"]
            self.address = kwargs["address"]
            self.city = kwargs["city"]
            self.state = kwargs["state"]
            self.pincode = kwargs["pincode"]
            self.country = kwargs["country"]
            self.country_code = kwargs["country_code"]
            self.mobile_number = kwargs["mobile_number"]
            try:
                self.email = kwargs["email"]
            except:
                pass
        except:
            db.session.rollback()
            return None

    def add_buyer(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()

    @classmethod
    def fetch_buyer_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def fetch_all_buyers_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def update_last_txn_date(self):
        self.last_transaction_date = datetime.now()
        db.session.commit()