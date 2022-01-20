
from sqlalchemy import exc
from flask import jsonify,make_response
from cerberus import Validator
from models.user import User
from flask_bcrypt import bcrypt

from schema.user_register import schema as register_schema
from schema.user_signIn import schema as signIn_schema

from utils.security import create_user_token
from utils.utils import send_respose

def get_user(email):
    user = User.get_user_by_email(email)
    if user:
        return {"name":user.name,
                "password":user.enc_password}
    else:
        return "Message Error!!"

def post_user(data):
    v = Validator(register_schema)
  
    if v.validate(data):
        data["enc_password"] = bcrypt.hashpw(data["enc_password"].encode('utf8'),bcrypt.gensalt())
        user = User(**data)

        if user:
            try:
                user.save_user()
                response_user = {
                    "name":user.name,
                    "email":user.email,
                    "address":user.address,
                    "created_at":user.created_at,
                    "id":user.id
                    }

                return send_respose(200,response_user,'successful signUp','')

            except exc.IntegrityError as e:
                # print(e.orig.args)
                # catching duplicate error
                if(e.orig.args[0]==1062):
                    return send_respose(409,{},'unSuccessful signUp',e.orig.args[1])
                return send_respose(400,{},'unSuccessful signUp','something went wrong')


    return {"message":"schema validation failed"}    


def signIn(data):
    v = Validator(signIn_schema)
    if v.validate(data):
        user = User.get_user_by_email(data["email"]) 
        # check if user exist and active
        if user and user.active == 1:
            # bcrypt check if hashed pass match to password sent by user
            if bcrypt.checkpw(data["password"].encode("UTF-8"), user.enc_password.encode("UTF-8")):
                token = create_user_token(user)
                return send_respose(200,{"access_token":token},'successful signIn',"")

            else:
                return send_respose(401,{},'unSuccessful signIn',"password does not match")
        else:
                return send_respose(404,{},'unSuccessful signIn',"user does not exist")   
    return send_respose(400,{},'unSuccessful signIn',"schema validation failed")   


def get_user_profile(user:User):
    return send_respose(200,user.json(),'successful fetch',"")   
 
