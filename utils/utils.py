from ast import Num
from tokenize import Number
from typing import Dict


from flask import jsonify, make_response
from itsdangerous import json
def send_respose(code:Num,data:Dict, message:str, err:str ):
    response = {
        'message':message,
        'data':data,
        'error':err
    }
    return jsonify(response), code
