from db import db

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




          