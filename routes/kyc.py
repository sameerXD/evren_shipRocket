@app.route("/api/user/kyc",methods=["POST"])
@token_required
def kyc(user):
    if user.kyc_verified:
        return "KYC already verified"
    if details_submitted(user):
        return "Details already submitted"
    if request.method == "POST":
        return post_kyc(user, request.json)