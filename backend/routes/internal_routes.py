from flask import Blueprint, request, current_app
from backend.lib.Config import Config
from backend.lib.Users import Users

from functools import wraps
import json
import jwt

config = Config().getConfig()
users = Users()

internal_routes = Blueprint('internal_routes', __name__)

def token_required(f):
  @wraps(f)
  def _verify(*args, **kwargs):
    auth_headers = request.headers.get('Authorization', '')
    invalid_msg = {
      "message": "Invalid or expired token"
    }
    try:
        token = auth_headers.encode()
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        if not data["sub"] or not data["exp"] or not data["iat"]:
            return json.dumps({"message": "Token malformed"}), 401
        user = users.verify_user(data)
        if not user:
            return json.dumps({"message": "User not found"}), 401
        return f(user, *args, **kwargs)
    except jwt.exceptions.ExpiredSignatureError:
        return json.dumps(invalid_msg), 401
    except (jwt.InvalidTokenError, Exception) as e:
        print(e)
        return json.dumps(invalid_msg), 401
  return _verify

@internal_routes.after_request
def after(response):
  auth_headers = request.headers.get('Authorization', '')
  if not auth_headers:
    return response
  token = auth_headers.encode()
  r = json.loads(response.get_data())

  if "donotrefresh" in r:
    return response

  try:
    refreshed_token = users.refresh_token(token)
  except (jwt.exceptions.ExpiredSignatureError, jwt.InvalidTokenError) as e:
    print(e)
    return response
  
  try:
    r["token"] = refreshed_token.decode()
  except Exception as e:
    print("fail",e)
  response.set_data(json.dumps(r))
  return response

@internal_routes.route('/login',methods=["POST"])
def login():
  data = request.get_json()
  user = users.authenticate(data)
  if user:
    return json.dumps(user)
  return json.dumps({"message": "Failed to authenticate"}), 401

@internal_routes.route('/users/getUserInfo')
@token_required
def getUserInfo(data):
  return json.dumps(users.getUserInfo(data))

@internal_routes.route('/users/postUserInfo',methods=["POST"])
@token_required
def postUserInfo(data):
  r = users.postUserInfo(data, request.data)
  return json.dumps(r), (200 if r["result"] == "success" else 500)