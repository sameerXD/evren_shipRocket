from datetime import date, datetime
from sqlalchemy import func
from sqlite3 import Date
from db import db

class Banks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,nullable=False)
    bank_name = db.Column(db.String(100),nullable=False)
    account_type = db.Column(db.String(50),nullable=False)
    account_number = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    beneficiary_name = db.Column(db.String(100),nullable=False)
    ifsc_code = db.Column(db.String(50),nullable=False)
    status = db.Column(db.Integer, default=1)

    def __init__(self, **inp_data):
        self.user_id = inp_data["user_id"]
        self.bank_name = inp_data["bank_name"]
        self.account_type = inp_data["account_type"]
        self.account_number = inp_data["account_number"]
        self.beneficiary_name = inp_data["beneficiary_name"]
        self.ifsc_code = inp_data["ifsc_code"]

        db.session.add(self)
        db.session.commit()

    def rollback_bank_data(self):
        db.session.rollback()

    def json(self):
        self_dict = self.__dict__
        bank_dict = {x:self_dict[x] for x in self_dict.keys() if not x.startswith("_")}
        return (bank_dict)

    @classmethod
    def accounts_count_for_user(cls,user_id):
        return db.session.query(db.func.count(cls.id)).group_by(cls.user_id).first()

    @classmethod
    def get_banks_by_user_id(cls,user_id):
        return cls.query.filter_by(user_id=user_id).all()