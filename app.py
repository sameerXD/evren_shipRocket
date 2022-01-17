from flask import Flask,request
import os
from flask_bcrypt import Bcrypt

# controller imports
from controllers.user import get_user, post_user

app = Flask(__name__)


# tell the location of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/ship_rocket'
# turns off the flask sqlalchemy tracker ,as sqlalchemy modification tracker is better
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True

# bcrypt configuration
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = b'$2b$12$wqKlYjmOfXPghx3FuC3Pu.'

# we can create the db and tables using sql alchemy 
@app.before_first_request
def create_table():
    db.create_all()

@app.route("/api/users", methods=["GET", "POST"])
def user():
    if request.method == "GET":
        return get_user(request.json["email"])
    if request.method == "POST":
        return post_user(request.json)

@app.route("/api/user/kyc",methods=["POST"])
def kyc():
    if request.method == "POST":
        return post_kyc(request.json)
  

if __name__=="__main__":
    from db import db
    db.init_app(app)
    bcrypt =Bcrypt(app)
    app.run(port=os.environ.get("BACKEND_PORT"),debug=True) 