from controllers.orders import create_order, fetch_all_orders
from flask import Blueprint , request
from utils.security import token_required

orders_page = Blueprint('orders',__name__)

@orders_page.route("/api/create/order",methods=["POST"])
@token_required
def add_orders(user):
    if request.method == "POST":
        request.json["user_id"] = user.id
        request.json["buyer"]["user_id"] = user.id
        return create_order(request.json)

@orders_page.route("/api/fetch/all/orders",methods=["GET"])
@token_required
def fetch_all_orders(user):
    return fetch_all_orders(user.id)