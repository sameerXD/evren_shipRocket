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
from routes.orders import orders_page
from routes.wallet import wallet

# register blueprints
app.register_blueprint(user_page)
app.register_blueprint(kyc_page)
app.register_blueprint(stores_page)
app.register_blueprint(bank_page)
app.register_blueprint(orders_page)
app.register_blueprint(wallet)


# tell the location of database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql6469394:e4jx2Gvypu@sql6.freesqldatabase.com/sql6469394'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('postgres://cwopiuxircrysg:913b906ac9fa271d1af16ace398ad6d745c08087ad22e8d650e68115af78b1b3@ec2-34-205-46-149.compute-1.amazonaws.com:5432/d588klnuohlpti','mysql+pymysql://sql6469394:e4jx2Gvypu@sql6.freesqldatabase.com/sql6469394')
# turns off the flask sqlalchemy tracker ,as sqlalchemy modification tracker is better
# Host: sql6.freesqldatabase.com
# Database name: sql6469394
# Database user: sql6469394
# Database password: e4jx2Gvypu
# Port number: 3306
# turns off the flask sqlalchemy tracker ,as sqlalchemy modification tracker is better
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True

# bcrypt configuration
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SECURITY_PASSWORD_HASH'] = os.environ.get("SECURITY_PASSWORD_HASH")
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT")

# mail config
# configuration of mail
app.config['MAIL_SERVER']='smtp.office365.com'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL")
app.config['MAIL_PASSWORD'] = os.environ.get("PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True 
mail= Mail()


if __name__=="__main__":
    from db import db
    db.init_app(app)
    mail.init_app(app)
    bcrypt =Bcrypt(app)
    app.run(debug=True) 