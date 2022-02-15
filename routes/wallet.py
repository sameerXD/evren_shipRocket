from controllers.wallet import homepage,paymenthandler, create_wallet, get_ballance, get_wallet_transaction

from flask import Blueprint , request

import requests

from utils.security import token_required

from flask_cors import CORS

cors = CORS()

wallet_page = Blueprint('wallet',__name__)
cors.init_app(wallet_page, resources={r"/*": {"origins": "*", "supports_credentials": True}})

@wallet_page.route('/api/wallet/createOrder', methods=["GET"])
def create_order():
    return homepage()

@wallet_page.route('/api/wallet/paymenthandler/', methods=["POST"])
@token_required
def handle_payment(user):
    return paymenthandler(request.form,user)

@wallet_page.route('/api/wallet/getBallance/', methods=["GET"])
@token_required
def get_wallet_ballance(user):
    return get_ballance(user)

@wallet_page.route('/api/wallet/getWalletTransaction/', methods=["GET"])
@token_required
def get__user_wallet_transaction(user):
    return get_wallet_transaction(user)


@wallet_page.route('/api/wallet/testTrans', methods=["GET"])
def create_wallet_user():
    return requests.get("https://api.genderize.io/?name=luc").content