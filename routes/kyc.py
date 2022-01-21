from controllers.kyc import post_kyc, get_kyc_details
from flask import Blueprint , request
from utils.security import token_required

kyc_page = Blueprint('kyc',__name__)

@kyc_page.route("/api/user/kyc",methods=["POST"])
@token_required
def submit_kyc(user):
    if request.method == "POST":
        request.json.user_id = user.id
        return post_kyc(request.json)

@kyc_page.route("/api/user/kyc/details",methods=["GET"])
@token_required
def kyc_details(user):
    if request.method == "GET":
        id = user.id
        return get_kyc_details(id)

    # if user.kyc_verified:
    #     return "KYC already verified"
    # if details_submitted(user):
    #     return "Details already submitted"
    # if request.method == "POST":
    #     return post_kyc(user, request.json)