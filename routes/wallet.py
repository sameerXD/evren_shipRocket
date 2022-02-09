from controllers.wallet import homepage,paymenthandler, create_wallet, get_ballance

from flask import Blueprint , request

import requests

from utils.security import token_required

wallet = Blueprint('wallet',__name__)

@wallet.route('/api/wallet/createOrder', methods=["GET"])
def create_order():
    return homepage()

@wallet.route('/api/wallet/paymenthandler/', methods=["POST"])
@token_required
def handle_payment(user):
    return paymenthandler(request.form,user)

@wallet.route('/api/wallet/getBallance/', methods=["GET"])
@token_required
def get_wallet_ballance(user):
    return get_ballance(user)


@wallet.route('/api/wallet/testTrans', methods=["GET"])
def create_wallet_user():
    return requests.get("https://api.genderize.io/?name=luc").content