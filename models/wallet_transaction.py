from datetime import date, datetime
from sqlite3 import Date
from db import db

class Wallet_transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,default=datetime.now())
    transaction_type = db.Column(db.Integer)
    transaction_status = db.Column(db.String(100), nullable=False)
    transaction_category = db.Column(db.String(100), nullable=False)
    transaction_id = db.Column(db.String(100), nullable=False)
    balance_state = db.Column(db.Integer)
    balance = db.Column(db.DECIMAL(19, 4))
    final_balance = db.Column(db.DECIMAL(19, 4))

    def save_wallet(self):
        db.session.add(self)
        db.session.flush()

    def json(self):
        self_dict = self.__dict__
        store_dict = {x:self_dict[x] for x in self_dict.keys() if not x.startswith("_")}
        return store_dict

    @classmethod
    def get_wallet_by_user_id(cls,user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def commit_row():
        db.session.commit()



