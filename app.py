from flask import Flask,request,jsonify
import os
from flask_bcrypt import Bcrypt

from flask_mail import Mail,Message


app = Flask(__name__)

# imports routes blueprint
from routes.user import user_page
from routes.kyc import kyc_page
from routes.stores import stores_page
from routes.bank import bank_page

# register blueprints
app.register_blueprint(user_page)
app.register_blueprint(kyc_page)
app.register_blueprint(stores_page)
app.register_blueprint(bank_page)


# tell the location of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/ship_rocket'
# turns off the flask sqlalchemy tracker ,as sqlalchemy modification tracker is better
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True

# bcrypt configuration
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SECURITY_PASSWORD_HASH'] = os.environ.get("SECURITY_PASSWORD_HASH")
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT")

# mail config
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "sameer.vashisth.egs@gmail.com"
app.config['MAIL_PASSWORD'] = "letsNotWorkAtEvren@123"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True 
mail= Mail()


# we can create the db and tables using sql alchemy 
@app.before_first_request
def create_table():
    db.create_all()


@app.route("/api/sendmail", methods=["GET"])
def sendMail():
    msg = Message(
        f'Ship Rocket Email Verefication',
        sender ="sameer.vashisth.egs@gmail.com",
        recipients = ["sameervashisht39@gmail.com"]
        )
    msg.body = f'Hello your otp is '
    mail.send(msg)
    return {"message":"mailsent"}



if __name__=="__main__":
    from db import db
    db.init_app(app)
    mail.init_app(app)
    bcrypt =Bcrypt(app)
    app.run(port=os.environ.get("BACKEND_PORT"),debug=True) 