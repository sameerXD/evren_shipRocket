from flask import render_template
from utils.utils import send_respose
from utils.config import db_code

from razorpay_third_party import razorpay

from models.wallet import Wallet
 
 
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
           return send_respose(200, wallet.json(), 'wallet already exist', '')
        else:
            return create_wallet(user,user_details)   
    except Exception as e:
        print(e)
        return  send_respose(400, {}, "payment failed drastically", str(e))   
  

def create_wallet(user, trans_det):
    try:
        
        data = {
            "user_id":user.id,
            "transaction_type":db_code.wallet.credit,
            "transaction_status":"succesfull",
            "balance_state":db_code.wallet.clear,
            "transaction_category":db_code.wallet.deposit_bank,
            "transaction_id":trans_det["id"]

        }
        wallet = Wallet(**data)
        wallet.save_wallet()
        return send_respose(200, {"user_details":trans_det["id"]}, "payment successful", '')
    except Exception as e:
        print(e)
        return  send_respose(400, {}, "wallet failed", str(e))  



