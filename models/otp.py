from db import db
from utils.config import db_code
import datetime
from random import randint

class Otp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    OTP = db.Column(db.String(100))
    email = db.Column(db.String(100))
    valid_till = db.Column(db.DateTime)

    @classmethod
    def get_by_Id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_otp(self):
        db.session.add(self)
        db.session.commit()

    def delete_otp(self):
        db.session.delete(self)
        db.session.commit() 

    @classmethod
    def delete_many(cls,email):
        cls.query.filter_by(email = email).delete()
        # result = [x.delete_otp for x in otps]
        # print(result)
        db.session.commit()    

    def create_validity():
        # creating otp validate time (5 min = 300 sec)
        return datetime.datetime.now() + datetime.timedelta(seconds=db_code.user.otp_validity)    

    def create_otp():
        # create Otp object and save it to db
        return randint(1000,9999)    




          