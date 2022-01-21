from flask import jsonify
from cerberus import Validator
from models.kyc import KYC
from flask_bcrypt import bcrypt
from controllers.user import User

from schema.kyc import schema as kyc_schema

from utils.utils import send_respose
from utils.config import db_code

def post_kyc(data):
    # inserting the user id from user(arg.) into the json input of the request (i.e. data)
    v = Validator(kyc_schema)
    if v.validate(data):
        kyc_data = KYC(**data)
        if kyc_data:
            try:
                kyc_data.save_kyc_data()
                return send_response(200,{},"KYC details submitted successfully.","")
            except:
                return send_respose(401,{},"","Details were not submitted!!")

    return "Schema Validation failed!!"


def get_kyc_details(id):
    status = KYC.kyc_status(id)
    if status==db_code.kyc_status.rejected:
        return send_respose(200,{},'Your Kyc has been rejected',"")

    if(status==db_code.kyc_status.verified):
        details = KYC.get_details_by_user_id(id)
        return send_respose(200,{'kyc_id':details.kyc_id},'Kyc already verified',"")

    if(status==db_code.kyc_status.under_review):
        details = KYC.get_details_by_user_id(id)
        return send_respose(200,{'kyc_id':details.kyc_id},'Details are under review',"")


