from flask import jsonify
from cerberus import Validator
from models.kyc import KYC
from flask_bcrypt import bcrypt
from controllers.user import User

from schema.kyc import schema as kyc_schema

from utils.utils import send_respose
from utils.config import db_code

def post_kyc(data):
    # first we need to check whether deatils are already submitted or not
    kyc = KYC.get_details_by_user_id(data["user_id"])
    # if details exist in the table, then check whether kyc is verified or are under review
    if kyc:
        status = KYC.kyc_status(data["user_id"])

        if status==db_code.kyc_status.verified:
            return send_respose(200,kyc.json(),'Kyc already verified',"")

        if status==db_code.kyc_status.under_review:
            return send_respose(200,kyc.json(),'Details are under review',"")

    # Now if details doesn't exist for supplied user id, then try to submit data
    v = Validator(kyc_schema)
    if v.validate(data):
        kyc_data = KYC(**data)
        if kyc_data:
            try:
                kyc_data.save_kyc_data()
                return send_respose(200,{},"KYC details submitted successfully.","")
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


def update_details(data):
    kyc = KYC.get_details_by_user_id(data["user_id"])
    if kyc and KYC.kyc_status(data["user_id"])== db_code.kyc_status.rejected:
        temp = KYC.update_details(data)
        if temp=="success":
            return send_respose(200,{},'Deatils updated successfully',"")
        else:
            return send_respose(401,{},"",'Details were not updated')
    else:
        return send_respose(401,{},"","KYC is incomplete")

