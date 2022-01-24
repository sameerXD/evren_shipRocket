from flask import jsonify
from cerberus import Validator
from models.stores import Stores
from flask_bcrypt import bcrypt

from schema.stores import schema as store_schema

from utils.utils import send_respose
# from utils.config import db_code

def add_store(data):
    v = Validator(store_schema)
    if v.validate(data):
        store = Stores(**data)
        if store:
            try:
                store.save_store()
                response = {
                            'store_id':store.store_id,
                            'name':store.user_name,
                            'created_at':store.created_at,
                            'address':store.address,
                            'city':store.city,
                            'state':store.state,
                            'country':store.country
                            }
                return send_respose(200,response,"Store created successfully.","")
            except:
                return send_respose(401,{},"","Store was not saved!!")
    else:
        return send_respose(401,{},"","Schema Validation Failed!!")


def all_stores(id):
    stores = Stores.get_stores_by_user_id(id)
    try:
        # need to create a nested dictionary for stores, with key as store_id
        resp = {}
        for store in stores:
            resp[store.store_id] = store.json()
        return send_respose(200,resp,"Stores fetched successfully", "")
    
    except:
        return send_respose(401,{},"","Error in fetching stores")


def update_store_details(data):
    store = Stores.get_store_by_both_id(data["user_id"], data["store_id"])

    if store:
        temp = Stores.update_details(data)
        if temp=="success":
            return send_respose(200,{},'Deatils updated successfully',"")
        else:
            return send_respose(401,{},"",'Details were not updated')
    else:
        return send_respose(401,{},"","Store doesn't exist")


def set_primary_store(user_id, store_id):
    temp = Stores.set_primary(user_id,store_id)

    if temp=="error":
        return send_respose(401,{},"","Error to set as primary!!")

    else:
        return send_respose(200, {"details":temp.json()},"Store succesfully set as primary","")
    

