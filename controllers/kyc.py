from flask import jsonify
from cerberus import Validator
from models.kyc import KYC
from flask_bcrypt import bcrypt

schema = {
    'user_id':{'type':'string','required': True},
    'govt_id_type':{'type':'string','required': True},
    'govt_id_number':{'type':'string','required': True},
    'pan_card':{'type':'string','required': True},
    'profile_pic_url':{'type':'string','required': True},
    'bank_name':{'type':'string','required': True},
    'bank_account_number':{'type':'string','required': True},
    'bank_account_name':{'type':'string','required': True},
    'service_code':{'type':'string','required': True},
}