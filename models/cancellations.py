from datetime import date, datetime
from sqlalchemy import func
from sqlite3 import Date
from db import db

# Those orders which are not picked up, but cancelled are inserted into this table to keep track of the refunds
class CancellationRefunds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pickup_id = db.Column(db.Integer)
    cancelled_at = db.Column(db.DateTime, default=datetime.now())
    refund_amount = db.Column(db.Float)
    refund_transaction_id = db.Column(db.Integer)
    refund_status = db.Column(db.Integer, default=0)


    def save_refund_entry(self):
        db.session.add(self)
        db.session.commit()