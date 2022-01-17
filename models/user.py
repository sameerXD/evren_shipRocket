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

    def __init__(self,name,email, country_code, mobile_number, enc_password, address,city,state,pincode,country,organization_name,created_at=None,updated_at=None, kyc_verified=None,active=None,_id=None,wallet_ballance=None):
        self.id = _id
        self.name = name
        self.email = email
        self.country_code = country_code
        self.mobile_number = mobile_number
        self.address = address
        self.city = city
        self.pincode = pincode
        self.country = country
        self.organization_name = organization_name
        self.created_at = created_at
        self.updated_at = updated_at
        self.kyc_verified = kyc_verified
        self.active = active
        self.state = state
        self.enc_password = enc_password


    def json(self):
         return {"name":self.name,"email":self.email }

    def save_user(self):
        db.session.add(self)
        db.session.commit()
