from datetime import datetime, timedelta
from functools import wraps
from models.user import User
import os
from flask import request,jsonify

# import jwt for authentication
import jwt

def create_user_token(user):
    token = jwt.encode({
        "user_id":user.id,
        'exp' : datetime.utcnow() + timedelta(minutes = 30)
    },os.environ.get("SECRET_KEY_USER"))
    return token.decode('UTF-8')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        #jwt is sent by headers
        if 'access_token' in request.headers:
            token = request.headers['access-token']
            try:
                # decoding the payload to fetch the stored details
                data = jwt.decode(token, os.environ.get("SECRET_KEY_USER"))
                current_user = User.get_user_by_id(data["user_id"])
            except:
                return jsonify({
                    'message' : 'Token is invalid !!',
                }), 401
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401    
        return f(current_user,*args, **kwargs)
    return decorated    




