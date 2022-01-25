from sqlalchemy import exc
from flask import jsonify,make_response
from cerberus import Validator
from models.user import User
from models.otp import Otp
from flask_bcrypt import bcrypt

from schema.user_register import schema as register_schema
from schema.user_signIn import schema as signIn_schema
from schema.otp_verification import schema as otp_schema
from schema.resend_otp import schema as resend_otp_schema
from schema.change_password import schema as change_password_schema

from utils.security import create_user_token
from utils.utils import send_respose
from utils.config import db_code


from flask_mail import Mail,Message

from random import randint

import os

import datetime

from werkzeug.security import safe_str_cmp

# instantiate Mail object
mail = Mail()



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
                
                generate_otp = save_otp(user)

                msg = Message(
                f'Ship Rocket Email Verefication',
                sender =os.environ.get("EMAIL"),
                recipients = ['samdragneal@gmail.com']
               )
                msg.body = f'Hello your otp is {generate_otp}'
                mail.send(msg)

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


    return send_respose(400,{},'unSuccessful signUp','schema validation failed')

def verify_email(data):
    v = Validator(otp_schema)
    if v.validate(data):
        try:
            otp = Otp.get_by_email(data["email"])
            # check if there is a otp in db associated with email
            if(otp):
                # check if the otp has expired
                if otp.valid_till<datetime.datetime.now():
                    otp.delete_otp()
                    return send_respose(200,{},'unSuccessful verification','OTP expired')
                
                # comparing the use input with the otp from db
                if not safe_str_cmp(otp.OTP,data["OTP"]):
                    return send_respose(200,{},'unSuccessful verification','OTP didnt match')

                # find user associated to otp and update email verification
                user = User.get_user_by_email(otp.email)
                user.email_verified = db_code.user.email_verified
                user.save_user()

                # creating jwt token for the user
                token = create_user_token(user)

                # delete the used token 
                otp.delete_otp()

                return send_respose(200,{'access_token':token},'Successful verification','')
                
            # if otp was not found in table
            return send_respose(404,{},'unSuccessful verification','no OTP found associated to this email')
            
        except Exception as e:
            return send_respose(500,{},'unSuccessful verification','Internal server error')
            
    return send_respose(400,{},'unSuccessful verification','schema validation failed')
            

def resend_otp_for_user(email:str):
    v = Validator(resend_otp_schema)
    if not v.validate({"email":email}):
        return send_respose(400,{},'unSuccessful','schema validation failed')
    try:
        user = User.get_user_by_email(email)

        if not user:
            return send_respose(404,{},'unSuccessful','user not found')

        if user.email_verified == db_code.user.email_verified:
            return send_respose(200,{},'unSuccessful','user already verified')

        # delete already existing otps
        Otp.delete_many(user.email)

        # generate 5 digit random number
        generate_otp =  Otp.create_otp()

        # creating otp validate time (5 min = 300 sec)
        validity = Otp.create_validity()

        # create Otp object and save it to db
        otp = Otp(user_id=user.id,email = user.email, OTP=generate_otp,valid_till=validity)

        otp.save_otp()    

        msg = Message(
        f'Ship Rocket Email Verefication',
        sender =os.environ.get("EMAIL"),
        recipients = ['samdragneal@gmail.com']
        )
        msg.body = f'Hello your otp is {generate_otp}'
        mail.send(msg)


        return send_respose(200,{email:user.email},'OTP sent','')
    except Exception as e:
        print(e)
        return send_respose(500,{},'unSuccessful','Internal server error')


def req_change_password(email):
    v = Validator(resend_otp_schema)
    if not v.validate({"email":email}):
        return send_respose(400,{},'unSuccessful','schema validation failed')
    try:
        user = User.get_user_by_email(email)
        if not user:
            return send_respose(404,{},'unSuccessful','user not found')

        # delete already existing otps
        Otp.delete_many(user.email)

        generate_otp = save_otp(user)
        url = f"http://127.0.0.1:5000/api/change_password?email={user.email}&OTP={generate_otp}"

        msg = Message(
        f'Ship Rocket Request Password Change',
        sender =os.environ.get("EMAIL"),
        recipients = ['samdragneal@gmail.com']
        )
        msg.body = f'copy the link to your browser {url}'
        mail.send(msg)
        
        return send_respose(200,{"email":user.email},'Mail sent','')
    
    except Exception as e:
        print(e)
        return send_respose(500,{},'unSuccessful','Internal server error')

def change_password(data):
    v = Validator(change_password_schema)

    if not v.validate(data):
        return send_respose(400,{},'unSuccessful','schema validation failed')
    try:
        user = User.get_user_by_email(data["email"])
        if not user:
            return send_respose(404,{},'unSuccessful','user not found')

        otp = Otp.get_by_email(data["email"])
            # check if there is a otp in db associated with email

        if(not otp):
            return send_respose(500,{},'unSuccessful verification','OTP do not exist')
        
        # check if the otp has expired
        if otp.valid_till<datetime.datetime.now():
            otp.delete_otp()
            return send_respose(200,{},'unSuccessful verification','OTP expired')
                
        # comparing the use input with the otp from db
        if not safe_str_cmp(otp.OTP,data["OTP"]):
            return send_respose(200,{},'unSuccessful verification','OTP didnt match')

        user.enc_password = bcrypt.hashpw(data["password"].encode('utf8'),bcrypt.gensalt())
        user.save_user()
        return send_respose(200,{"email":user.email},'Successful password change','')
        
    except Exception as e:
        print(e)
        return send_respose(500,{},'unSuccessful','Internal server error')

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
 
def save_otp(user:User):
    # generate 5 digit random number
    generate_otp =  Otp.create_otp()

    # creating otp validate time (5 min = 300 sec)
    validity = Otp.create_validity()

    # create Otp object and save it to db
    otp = Otp(user_id=user.id,email = user.email, OTP=generate_otp,valid_till=validity)

    otp.save_otp()

    return generate_otp