from datetime import date, datetime
from sqlite3 import Date
from db import db

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,default=datetime.now())
    balance = db.Column(db.DECIMAL(19, 4))

    def save_wallet(self):
        db.session.add(self)
        db.session.flush()

    def json(self):
        self_dict = self.__dict__
        store_dict = {x:self_dict[x] for x in self_dict.keys() if not x.startswith("_")}
        return store_dict

    @classmethod
    def get_wallet_by_user_id(cls,user_id):
        return cls.query.filter_by(user_id=user_id).first()

    def commit_row():
        db.session.commit()



