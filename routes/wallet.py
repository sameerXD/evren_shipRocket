from controllers.wallet import homepage,paymenthandler

from flask import Blueprint , request

wallet = Blueprint('wallet',__name__)

@wallet.route('/api/createOrder', methods=["GET"])
def create_order():
    return homepage()

@wallet.route('/api/paymenthandler/', methods=["POST"])
def handle_payment():
    return paymenthandler(request.form)