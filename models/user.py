from datetime import date, datetime
from sqlite3 import Date
from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    country_code = db.Column(db.String(5), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    enc_password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))
    country = db.Column(db.String(100))
    organization_name = db.Column(db.String(100))
    wallet_balance = db.Column(db.Integer,default=0)
    created_at = db.Column(db.DateTime, nullable=False, default = datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False,default = datetime.now())
    kyc_verified = db.Column(db.Boolean, default=False)
    active = db.Column(db.Integer, default=1)


    def json(self):
         return {"name":self.name,"email":self.email }

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user(cls,email):
        # return User.query.filter_by(email=email).all()
        return cls.query.filter_by(email=email).first()
