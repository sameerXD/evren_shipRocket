from flask import jsonify, render_template
from utils.utils import send_respose
from utils.config import db_code

import json

from razorpay_third_party import razorpay

from models.wallet_transaction import Wallet_transaction
from models.wallet import Wallet
from models.transaction import Transaction
 
 
def homepage():
    order = razorpay.generate_order(db_code.wallet.wallet_init_amount)
    return render_template('index.html', content=order)


# POST request will be made by Razorpay
# and it won't have the csrf token.
def paymenthandler(request,user):
    try:
        user_details = razorpay.verify_payment(request,db_code.wallet.wallet_init_amount)
        print(user_details)

        
        # return send_respose(200, {"user_details":"user_details"}, "payment successful", '')
        wallet = Wallet.get_wallet_by_user_id(user.id)

        if wallet:
           return add_money(user, user_details)
        else:
            return create_wallet(user,user_details)   
    except Exception as e:
        print(e)
        return  send_respose(400, {}, "payment failed drastically", str(e))   
  


def create_wallet(user, trans_det):
    try:
        # flush wallet_transaction session
        # transaction added to wallet transaction table for users
        data = {
            "user_id":user.id,
            "transaction_type":db_code.wallet.credit,
            "transaction_status":"succesfull",
            "balance_state":db_code.wallet.clear,
            "transaction_category":db_code.wallet.deposit_bank,
            "transaction_id":trans_det["id"],
            "balance":trans_det["amount"],
            "final_balance":trans_det["amount"],

        }
        wallet_transaction = Wallet_transaction(**data)
        wallet_transaction.save_wallet()

        # add money to the wallet 
        wallet_data = {
            "user_id":user.id,
            "balance":trans_det["amount"]
        }

        wallet = Wallet(**wallet_data)
        wallet.save_wallet()

        # flush evren transaction session

        evren_trans_data = {
        "recipient" :db_code.Transaction.evren_user,
        "sender" :user.id,
        "txn_type" : db_code.Transaction.trans_type_credit,
        "kind_of_txn" : db_code.Transaction.kind_of_txn_deposit,
        "order_id" : trans_det["id"],
        "status" : db_code.Transaction.payment_auth,
        "amount" : trans_det["amount"]
        }
        trans = Transaction(**evren_trans_data)
        trans.save_transaction()
        
    except Exception as e:
        print(e)
        return  send_respose(400, {}, "wallet failed", str(e))  

    # commit if everything went well
    Wallet.commit_row()
    Transaction.commit_row()    
    Wallet_transaction.commit_row()
    
    return send_respose(200, {"payment_id":trans_det["id"]}, "payment successful", '')

def add_money(user, trans_det):
    try:
        wallet = Wallet.get_wallet_by_user_id(user.id)
        current_balance = wallet.balance

        # updating money to wallet object
        updated_balance = current_balance+trans_det["amount"]
        wallet.balance = updated_balance
        wallet.save_wallet()

        # adding transaction to wallet transaction
        wallet_trans_data = {
            "user_id":user.id,
            "transaction_type":db_code.wallet.credit,
            "transaction_status":"succesfull",
            "balance_state":db_code.wallet.clear,
            "transaction_category":db_code.wallet.deposit_bank,
            "transaction_id":trans_det["id"],
            "balance":trans_det["amount"],
            "final_balance":updated_balance

        }
        wallet_transaction = Wallet_transaction(**wallet_trans_data)
        wallet_transaction.save_wallet()

        # flush transaction session

        evren_trans_data = {
        "recipient" :db_code.Transaction.evren_user,
        "sender" :user.id,
        "txn_type" : db_code.Transaction.trans_type_credit,
        "kind_of_txn" : db_code.Transaction.kind_of_txn_deposit,
        "order_id" : trans_det["id"],
        "status" : db_code.Transaction.payment_auth,
        "amount" : trans_det["amount"]
        }
        trans = Transaction(**evren_trans_data)
        trans.save_transaction()

    except Exception as e:
        print(e)
        return  send_respose(400, {}, "adding money to wallet failed", str(e))  

    # commiting the changes
    Wallet.commit_row()
    Wallet_transaction.commit_row()
    Transaction.commit_row()
    return send_respose(200, {"payment_id":trans_det["id"]}, "money added to wallet", '')


def get_ballance(user):
    wallet = Wallet.get_wallet_by_user_id(user.id)
    response = {
        "id":user.id
    }
    if(not wallet):
        response["ballance"]= 0
    else:
        response["ballance"]= wallet.balance
    
    return send_respose(200, response, "money in wallet", '')

def get_wallet_transaction(user):
    get_wallet_transaction_data = Wallet_transaction.get_wallet_by_user_id(user.id)
    response = []
    
    for obj in get_wallet_transaction_data:
        response.append(obj.json())

    return send_respose(200, response, "wallet transactions", '')






# def test_transaction():
#     data = {
#     "recipient" :1,
#     "sender" :2,
#     "txn_type" : 0,
#     "kind_of_txn" : 1,
#     "order_id" : "db.Column(db.String(100), nullable=False)",
#     "status" : "db.Column(db.String(100), nullable=False)",
#     "amount" : 1200
#     }
#     trans = Transaction(**data)
#     trans.save_transaction()
#     Transaction.commit_row()
#     return send_respose(200, {"user_details":data["order_id"]}, "payment successful", '')
    
