from datetime import date, datetime
from sqlite3 import Date
from db import db

class Stores(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,default=datetime.now())
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100),nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Integer, default=1)
    primary = db.Column(db.Integer, default=0)

    def save_store(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        self_dict = self.__dict__
        store_dict = {x:self_dict[x] for x in self_dict.keys() if not x.startswith("_")}
        return store_dict

    @classmethod
    def get_stores_by_user_id(cls,user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_store_by_both_id(cls,user_id,store_id):
        return cls.query.filter_by(user_id=user_id, store_id=store_id).first()


    @classmethod
    def update_details(cls, data):
        row = cls.query.filter_by(user_id=data["user_id"], store_id=data["store_id"])
        # It checks if store exists or not - with the supplied user id and store id -- that's why both ids are taken to check
        if row:
            try:
                for attribute in data.keys():
                    row.attribute = data[attribute]
                db.session.commit()
                return "success"
            except:
                return "error"
        else:
            return "error"


    @classmethod
    def set_primary(cls, user_id, store_id):
        try:
            # unset the primary attribute for the store which is already primary
            store_primary = cls.query.filter_by(user_id=user_id,primary=1).first()
            if store_primary:
                store_primary.primary = 0

            # fetch store to be set as primary and then set its primary attribute as 1
            store = cls.query.filter_by(store_id=store_id, user_id=user_id).first()
            store.primary=1

            db.session.commit()
            return store
        except:
            return "error"

