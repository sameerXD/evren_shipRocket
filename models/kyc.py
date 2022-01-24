from models.user import User
from datetime import date, datetime
from sqlite3 import Date
from db import db

class KYC(db.Model):
    kyc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime,default=datetime.now())
    pancard = db.Column(db.String(10),nullable=False,unique=True)
    pancard_url = db.Column(db.String(100),nullable=False)
    company_type = db.Column(db.String(20), nullable=False)
    business_proof_used = db.Column(db.String(50), nullable=False)
    business_proof_url = db.Column(db.String(100),nullable=False)
    has_gst_number = db.Column(db.Integer,nullable=False)
    gst_number = db.Column(db.String(15))
    status_code = db.Column(db.Integer, default=1)
    status_message = db.Column(db.Text)

    def save_kyc_data(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        self_dict = self.__dict__
        kyc_dict = {x:self_dict[x] for x in self_dict.keys() if not x.startswith("_")}
        return (kyc_dict)

    # 0->kyc rejected
    # 1->under review
    # 2->verified
    @classmethod
    def kyc_status(cls,user_id):
        status = cls.query.with_entities(cls.status_code).filter_by(user_id=user_id).first()
        return status.status_code

    @classmethod
    def get_details_by_user_id(cls,user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def update_details(cls, data):
        row = cls.query.filter_by(user_id=data["user_id"])
         
        # Now extract the input from json request i.e. data and update it on the desired row i.e. row
        try:
            for attribute in data.keys():
                row.attribute = data[attribute]
            db.session.commit()
            return "success"
        except:
            return "error"
