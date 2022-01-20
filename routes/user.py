from controllers.user import get_user, post_user, signIn
from flask import Blueprint , request
from utils.security import token_required


user_page = Blueprint('user',__name__ )


@user_page.route("/api/users/signIn", methods=["POST"])
def user_signIn():
    return signIn(request.json)


@user_page.route("/api/users", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        return post_user(request.json)

@user_page.route("/api/user", methods=["GET"])
@token_required
def get_profile(user):
        return user.json()    