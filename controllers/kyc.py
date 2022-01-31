from flask import jsonify
from cerberus import Validator
from models.kyc import KYC
from models.bank import Banks
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

        if status==db_code.kyc_status.rejected:
            return send_respose(200,{},'KYC already submitted and got rejected!!',"")

        if status==db_code.kyc_status.verified:
            return send_respose(200,kyc.json(),'Kyc already verified!!',"")

        if status==db_code.kyc_status.under_review:
            return send_respose(200,kyc.json(),'Details are under review',"")

    # Now if details doesn't exist for supplied user id, then try to submit data
    v1 = Validator(kyc_schema)

    if v1.validate(data):
        # create an instance of bank model
        bank_data = Banks(**data)
        bank_data.save_bank_data()

        # If instance creation was successful, then create a kyc instance
        if bank_data:
            #now insert the bank_id generated into the input data
            data["bank_id"] = bank_data.id
            kyc_data = KYC(**data)
            
            if kyc_data:
                # try to add kyc data, but if it fails then make sure to remove the bank details
                try:
                    kyc_data.save_kyc_data()
                    resp = {
                        "kyc_id" : kyc_data.id,
                        "aadhar" : kyc_data.aadhar_card,
                        "pancard" : kyc_data.pancard,
                        "bank_id" : kyc_data.bank_id,
                        "status" : kyc_data.status_code
                    }
                    return send_respose(200,kyc_data.json(),"KYC details submitted successfully.","")
                except Exception as e:
                    print("fuck" ,e)
                    return send_respose(401,{},"","Details were not submitted!!")
            else:
                return send_respose(401,{},"","Error in KYC data!!")

        else:
            return send_respose(401,{},"","Error in Bank Details!!")
            

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

