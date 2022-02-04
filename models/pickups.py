from datetime import date, datetime
from sqlalchemy import func
from sqlite3 import Date
from db import db

class Pickups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    courier_assigned = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String, default=0)
    remarks = db.Column(db.String)
    transaction_id = db.Column(db.Integer,nullable=False)
    picked_up_at = db.Column(db.DateTime)  #valid only when status=1
    completed_at = db.Column(db.DateTime) #valid only when status=2
    shipping_charges = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

    def save_pickup(self):
        db.session.add(self)
        db.session.commit()




# Status
# 0 = not picked up
# 1 = picked up
# 2 = completed
# 3 = fail to pickup
