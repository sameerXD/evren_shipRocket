from controllers.orders import create_order, fetch_all_orders, generate_invoice
from flask import Blueprint , request
from utils.security import token_required

from flask_cors import CORS

cors = CORS()


orders_page = Blueprint('orders',__name__)
cors.init_app(orders_page, resources={r"/*": {"origins": "*", "supports_credentials": True}})


@orders_page.route("/api/orders/create_order",methods=["POST"])
@token_required
def add_orders(user):
    if request.method == "POST":
        request.json["user_id"] = user.id
        request.json["buyer"]["user_id"] = user.id
        return create_order(request.json)

@orders_page.route("/api/orders/fetch_all_orders",methods=["GET"])
@token_required
def fetch_all_orders(user):
    return fetch_all_orders(user.id)

@orders_page.route("/api/orders/generate_invoice", methods=["GET"])
def get_invoice():
    return generate_invoice(request.args.get("order_id"))