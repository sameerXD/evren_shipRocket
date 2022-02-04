from datetime import datetime
from db import db
from sqlalchemy import or_
# from flask_sqlalchemy import 



class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.Integer,nullable=False)
    sender = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,default=datetime.now())
    txn_type = db.Column(db.Integer, nullable=False)
    kind_of_txn = db.Column(db.Integer)
    order_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.DECIMAL(19, 4))

    def save_transaction(self):
        db.session.add(self)
        db.session.flush()

    def json(self):
        self_dict = self.__dict__
        store_dict = {x:self_dict[x] for x in self_dict.keys() if not x.startswith("_")}
        return store_dict

    @classmethod
    def get_transaction_by_user_id(cls,user_id):
        return cls.query.filter(or_(sender = user_id, recipient = user_id )).all()

    def commit_row():
        db.session.commit()


