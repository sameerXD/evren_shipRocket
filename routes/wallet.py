from controllers.wallet import homepage,paymenthandler, create_wallet

from flask import Blueprint , request

from utils.security import token_required

wallet = Blueprint('wallet',__name__)

@wallet.route('/api/wallet/createOrder', methods=["GET"])
def create_order():
    return homepage()

@wallet.route('/api/wallet/paymenthandler/', methods=["POST"])
@token_required
def handle_payment(user):
    return paymenthandler(request.form,user)

@wallet.route('/createWallet')
@token_required
def create_wallet_user(user):
    return create_wallet(user)