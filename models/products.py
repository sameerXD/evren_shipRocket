from datetime import date, datetime
from sqlalchemy import func
from sqlite3 import Date
from db import db

class Products_Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    ordered_at = db.Column(db.DateTime, default=datetime.now())
    product_name = db.Column(db.String(100))
    hsn_code = db.Column(db.Integer,nullable=False)
    unit_price = db.Column(db.Float,nullable=False)
    units_ordered = db.Column(db.Integer,nullable=False)
    unit_used = db.Column(db.String(20))
    tax_rate = db.Column(db.Float,nullable=False)
    total_amount = db.Column(db.Float)

    def __init__(self,o_id,**kwargs):
        try:
            self.order_id = o_id
            self.product_name = kwargs["product_name"]
            self.hsn_code = kwargs["hsn_code"]
            self.unit_price = kwargs["unit_price"]
            self.units_ordered = kwargs["units_ordered"]
            self.tax_rate = kwargs["tax_rate"]
            self.total_amount = (self.unit_price - self.tax_rate*self.unit_price/100) * self.units_ordered
            try:
                self.unit_used = kwargs["unit_used"]
            except:
                pass

        except:
            db.session.rollback()
            return None

    def add_product(self):
        db.session.add(self)
    
    def save_product(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()

    @classmethod
    def commit_changes(cls):
        db.session.commit()

    @classmethod
    def rollback_changes(cls):
        db.session.rollback()

    @classmethod
    def fetch_products_by_order_id(cls, order_id):
        return cls.query.filter_by(order_id=order_id).all()