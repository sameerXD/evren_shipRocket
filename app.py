from flask import Flask,request,jsonify
import os
from flask_bcrypt import Bcrypt

# controller imports
from controllers.user import post_user, signIn
from controllers.user import get_user
from utils.security import token_required
from controllers.kyc import post_kyc, details_submitted

# middlewares


app = Flask(__name__)



# tell the location of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/ship_rocket'
# turns off the flask sqlalchemy tracker ,as sqlalchemy modification tracker is better
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True

# bcrypt configuration
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SECURITY_PASSWORD_HASH'] = os.environ.get("SECURITY_PASSWORD_HASH")
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT")



# we can create the db and tables using sql alchemy 
@app.before_first_request
def create_table():
    db.create_all()

@app.route("/api/users", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        return post_user(request.json)

@app.route("/api/user", methods=["GET"])
@token_required
def get_profile(user):
        return user.json()


@app.route("/api/users/signIn", methods=["POST"])
def user_signIn():
    return (signIn(request.json))
    

@app.route("/api/user/kyc",methods=["POST"])
@token_required
def kyc(user):
    if user.kyc_verified:
        return "KYC already verified"
    if details_submitted(user):
        return "Details already submitted"
    if request.method == "POST":
        return post_kyc(user, request.json)


@app.route("/api/add/store",methods=["POST"])
@token_required
def store(user):
    if request.method == "POST":
        return add
  

if __name__=="__main__":
    from db import db
    db.init_app(app)
    bcrypt =Bcrypt(app)
    app.run(port=os.environ.get("BACKEND_PORT"),debug=True) 