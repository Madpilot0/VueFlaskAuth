from backend.lib.Database import UserDatabase
from backend.lib.Config import Config

import jwt
import re
import bcrypt
import json
from datetime import datetime, timedelta
from flask import current_app, request

class Users:
  def __init__(self):
    self.db = UserDatabase()
    self.config = Config().getConfig()
    self.rounds = 10

  def authenticate(self, data):
    cur = self.db.query("SELECT user, pass, firstname, lastname FROM users WHERE user = %s",[data["username"]])
    r = cur.fetchone()
    loginOffset = 0
    if r:
      if data["stayin"]:
        loginOffset = 99999999999
      username, password, firstname, lastname = r
      pwbytes = data["password"].encode('utf-8')
      saltbytes = password.encode('utf-8')
      if bcrypt.hashpw(pwbytes, saltbytes) == saltbytes:
        token = jwt.encode({
          'sub': username,
          'iat': datetime.utcnow(),
          'exp': datetime.utcnow() + timedelta(seconds=self.config["server"]["login_exp"] + loginOffset),
          'src': request.remote_addr,
          'fln': firstname+" "+lastname,
          'kau': data["stayin"]
        },
        current_app.config["SECRET_KEY"])
        return {
          "token": token.decode('UTF-8')
        }
    return None

  def verify_user(self, data):
    cur = self.db.query("SELECT COUNT(*) FROM users WHERE user = %s",[data['sub']])
    if cur.fetchone()[0] > 0:
      if data['src'] == request.remote_addr:
        return data
    return None

  def refresh_token(self, old_token):
    data = jwt.decode(old_token, current_app.config['SECRET_KEY'])
    if data['src'] != request.remote_addr:
        return None
    cur = self.db.query("SELECT firstname, lastname FROM users  WHERE user = %s",[data["sub"]])
    r = cur.fetchone()
    if r:
      loginOffset = 0
      if data['kau']:
        loginOffset = 99999999999
      firstname, lastname = r
      new_token = jwt.encode({
        'sub': data["sub"],
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=self.config["server"]["login_exp"] + loginOffset),
        'fln': firstname+" "+lastname,
        'src': request.remote_addr,
        'kau': data['kau']
      },
    current_app.config['SECRET_KEY'])
    else:
      new_token = None
    
    self.db.query("UPDATE users SET lastseen = NOW(), lastip = %s WHERE user = %s",[request.remote_addr,data["sub"]])
    return new_token

  def getUserInfo(self, data):
    username = data['sub']
    cur = self.db.query("""
      SELECT firstname, lastname, email
      FROM users
      WHERE user = %s""",[username])
    userInfo = cur.fetchone()
    if len(userInfo) == 0:
      return {"error": "Nothing found"}
    ret = {
      "username": username,
      "firstname": userInfo[0],
      "lastname": userInfo[1],
      "email": userInfo[2]
    }
    return ret

  def postUserInfo(self, data, form):
    form = json.loads(form)
    
    if len(form['password']) > 5:
      password = bcrypt.hashpw(form["password"].encode('utf-8'), bcrypt.gensalt(self.rounds))
      self.db.query("UPDATE users SET pass = %s WHERE user = %s",[password, form["username"]])

    return {"result": "success"}