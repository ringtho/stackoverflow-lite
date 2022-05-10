import jwt
from flask import request, jsonify
import datetime
from functools import wraps

secret_key = "sringtho"

def encode_token(user_id, username):
    payload = {
        "uid": user_id,
        "unm": username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=1)
       
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
    return token

def ensure_token_available_and_clean():
    header_token = request.headers.get("Authorization")
    if not header_token:
        return jsonify({"status": 400, "Error":"Missing token!!"}),400
    elif "Bearer" not in header_token:
        return jsonify({"status": 400, "Error": "Token tampered with!!!"}),400
    token = header_token.split(" ")[1]
    return token 

def decode_token(token):
    """
        Decode the token back to original state before sending
    """
    decode = jwt.decode(token, secret_key, algorithms='HS256')
    return decode

def get_id_token():
    user_id = decode_token(ensure_token_available_and_clean())['uid']
    return user_id

def required_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = None
        try:
            token = decode_token(ensure_token_available_and_clean())
            response = func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            response = jsonify({
                "error": "Token has expired!!"
            }),401
        except jwt.InvalidTokenError:
            response = jsonify({
                "error": "Invalid token. Please provide a valid token"
            }),401
        return response
    return wrapper