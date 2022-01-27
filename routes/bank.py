from controllers.bank import add_bank_account, show_bank_accounts
from flask import Blueprint , request
from utils.security import token_required

bank_page = Blueprint('bank',__name__)

@bank_page.route("/api/add/bank/account",methods=["POST"])
@token_required
def store(user):
    if request.method == "POST":
        request.json["user_id"] = user.id
        return add_bank_account(request.json)


@bank_page.route("/api/show/bank/accounts",methods=["GET"])
@token_required
def myStores(user):
    if request.method == "GET":
        return show_bank_accounts(user.id)
