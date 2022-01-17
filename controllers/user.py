from flask import jsonify
from cerberus import Validator
from models.user import User
from flask_bcrypt import bcrypt

schema = {
    'name':{'type':'string','required': True},
    'email':{'type':'string','required': True},
    'country_code':{'type':'string','required': True},
    'mobile_number':{'type':'string','required': True},
    'enc_password':{'type':'string','required': True},
    'address':{'type':'string','required': True},
    'city':{'type':'string','required': True},
    'state':{'type':'string','required': True},
    'pincode':{'type':'string','required': True},
    'country':{'type':'string','required': True},
    'organization_name':{'type':'string','required': True},
}

v = Validator(schema)


def get_user(email):
    user = User.get_user(email)
    if user:
        return {"name":user.name,
                "password":user.enc_password}
    else:
        return "Message Error!!"

def post_user(data):
    if v.validate(data):
        data["enc_password"] = bcrypt.hashpw(data["enc_password"].encode('utf8'),bcrypt.gensalt())
        user = User(**data)

        if user:
            try:
                user.save_user()
                return {"name":"{}, {}".format(data["name"], user.json())}
            except:
                return {"message":"Internal server err"}


    return {"message":"schema validation failed"}    


