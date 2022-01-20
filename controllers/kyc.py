from flask import jsonify
from cerberus import Validator
from models.kyc import KYC
from flask_bcrypt import bcrypt
from controllers.user import User

from schema.kyc import schema as kyc_schema

def post_kyc(user,data):
    # inserting the user id from user(arg.) into the json input of the request (i.e. data)
    data["user_id"] = user.id

    v = Validator(kyc_schema)
    if v.validate(data):
        kyc_data = KYC(**data)
        if kyc_data:
            try:
                kyc_data.save_kyc_data()
                return("KYC details submitted successfully.")
            except:
                return("Details were not submitted!!")

    return "Schema Validation failed!!"

def details_submitted(user):
# checking if the details are already submitted and are under review
    Id = user.id
    details = User.query.filter_by(id=Id).first()
    if details:
        return True
    else:
        return False
