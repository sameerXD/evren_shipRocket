from flask import jsonify
from cerberus import Validator
from models.bank import Banks
from flask_bcrypt import bcrypt

from schema.bank import schema as bank_schema

from utils.utils import send_respose
# from utils.config import db_code

def add_bank_account(data):
    # check if user already has 5 bank accounts
    counts = Banks.accounts_count_for_user(data["user_id"])
    if (counts.count)>=5:
        return send_respose(402, {}, "", "You can add a maximum of 5 bank accounts")

    v = Validator(bank_schema)
    if v.validate(data):
        try:
            bank = Banks(**data)
            if bank:
                response = {
                                'bank_id':bank.id,
                                'bank_name':bank.bank_name,
                                'added_at':bank.created_at,
                                'account_number':bank.account_number,
                                'beneficiary':bank.beneficiary_name,
                                'ifsc_code':bank.ifsc_code,
                                'accounts_count': counts.count+1
                                }
                return send_respose(200,response,"Bank account added successfully.","")
        except Exception as e:
            print(e)
            return send_respose(401,{},"","Bank account was not saved!!")
    else:
        return send_respose(401,{},"","Schema Validation Failed!!")


def show_bank_accounts(id):
    banks = Banks.banks_by_user_id(id)
    try:
        # need to create a nested dictionary for stores, with key as store_id
        resp = {}
        for bank in banks:
            resp[bank.bank_id] = bank.json()
        return send_respose(200,resp,"Banks fetched successfully", "")
    
    except:
        return send_respose(401,{},"","Error in fetching your accounts")


def set_primary_account(user_id, bank_id):
    status = Banks.set_primary(user_id,bank_id)

    if status=="error":
        return send_respose(401,{},"","Error to set as primary!!")

    else:
        return send_respose(200, {"details":status.json()},"Bank succesfully set as primary","")
