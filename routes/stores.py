from controllers.stores import add_store, all_stores, update_store_details, set_primary_store
from flask import Blueprint , request
from utils.security import token_required

stores_page = Blueprint('stores',__name__)

@stores_page.route("/api/add/store",methods=["POST"])
@token_required
def store(user):
    if request.method == "POST":
        request.json["user_id"] = user.id
        return add_store(request.json)


@stores_page.route("/api/show/stores",methods=["GET"])
@token_required
def myStores(user):
    if request.method == "GET":
        return all_stores(user.id)


@stores_page.route("/api/update/store/<store_id>", methods=["PUT"])
@token_required
def update_store(user,store_id):
    if request.method == "PUT":
        request.json["user_id"] = user.id
        request.json["store_id"] = store_id
        return update_store_details(request.json)


@stores_page.route("/api/set/primary/<store_id>", methods=["PUT"])
@token_required
def set_as_primary(user, store_id):
    if request.method == "PUT":
        return set_primary_store(user.id, store_id)



