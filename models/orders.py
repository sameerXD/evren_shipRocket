from datetime import date, datetime
from sqlalchemy import func
from sqlite3 import Date
from db import db

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,nullable=False)
    buyer_id = db.Column(db.Integer,nullable=False)
    store_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.Integer,default=1)
    status_message = db.Column(db.String(100))
    total_order_amount = db.Column(db.Float, nullable=False)
    other_charges = db.Column(db.Float, default=0)
    discount = db.Column(db.Float, default=0)
    tax = db.Column(db.Float)
    payment_mode = db.Column(db.String(20))
    item_length = db.Column(db.Float)
    item_width = db.Column(db.Float)
    item_height = db.Column(db.Float)
    order_weight = db.Column(db.Float)
    number_of_products = db.Column(db.Integer)

    # For return orders
    order_type = db.Column(db.Integer,default=0)
    parent_order_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        try:
            self.user_id = kwargs["user_id"]
            self.buyer_id = kwargs["buyer_id"]
            self.store_id = kwargs["store_id"]
            self.other_charges = kwargs["other_charges"]
            self.discount = kwargs["discount"]
            self.tax = kwargs["tax"]
            self.total_order_amount = kwargs["total_order_amount"]
            self.payment_mode = kwargs["payment_mode"]
            self.item_length = kwargs["item_length"]
            self.item_width = kwargs["item_width"]
            self.item_height = kwargs["item_height"]
            self.order_weight = kwargs["order_weight"]
            self.number_of_products = kwargs["number_of_products"]

        except:
            db.session.rollback()
            return None

    # Order Status:
    # 0 = cancelled/deleted
    # 1 = new order
    # 2 = ready_for_pickup
    # 3 = picked_up
    # 4 = completed

    def json(self):
        self_dict = self.__dict__
        kyc_dict = {x:self_dict[x] for x in self_dict.keys() if not x.startswith("_")}
        return (kyc_dict)

    def save_order(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()

    @classmethod
    def fetch_orders_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def fetch_orders_by_user_id_and_status(cls, user_id, status):
        return cls.query.filter_by(user_id=user_id, status=status).all()

    @classmethod
    def update_status_by_order_id(cls, order_id, new_status):
        order = cls.query.filter_by(id = order_id).first()
        order.status = new_status
    