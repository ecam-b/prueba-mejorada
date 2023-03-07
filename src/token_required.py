from flask import request, jsonify
from functools import wraps
import jwt
from config import SECRET_KEY
from models.UserModel import UserModel


def token_required(func):
  @wraps(func)
  def decorator(*args, **kwargs):
    token = None

    if "x-access-token" in request.headers:
      token = request.headers["x-access-token"]

    if token == None:
      return jsonify({"message": "Token no enviado."}), 400
    
    try:
      data = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"]
      )
      usuario_actual = UserModel.query.filter_by(id = data["id"]).first()
    except:
      return jsonify({"message": "Token no valido."}), 400
    return func(usuario_actual, *args, **kwargs)
  return decorator