from datetime import date, datetime
from sqlite3 import Date
from db import db

class KYC(db.Model):
    kyc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    kyc_submission_date = db.Column(db.DateTime)
    govt_id_type = db.Column(db.String(20), nullable=False)
    govt_id_number = db.Column(db.String(50), nullable=False)
    pan_card = db.Column(db.String(10),nullable=False,unique=True)
    profile_pic_url = db.Column(db.String(100))
    bank_name = db.Column(db.String(100))
    bank_account_number = db.Column(db.String(50))
    bank_account_name = db.Column(db.String(100))
    # IFSC Code
    service_code = db.Column(db.String(20))
# updated_at, status_message, status_code

    def save_kyc_data(self):
        db.session.add(self)
        db.session.commit()
