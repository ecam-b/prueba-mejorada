from flask import Blueprint, request, jsonify
# models
from models.UserModel import UserModel, UserSchema
for_him = UserSchema()
for_them = UserSchema(many=True)
# database 
from database.db import db
# security
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from config import SECRET_KEY
# time
from datetime import datetime, timedelta

user_bp = Blueprint("user", __name__)


@user_bp.route("/")
def get_all_users():
  try:
    users = UserModel.query.all()
    result = for_them.dump(users)
    return jsonify(result)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400


@user_bp.route("/login", methods=["POST"])
def login():
  try:
    data = request.json
    username = data["username"]
    password = data["password"]

    user = UserModel.query.filter_by(username = username)
    if user != None:
      return jsonify({"message": "Usuario no encontrado. Por favor realice el registro de un nuevo usuario."}), 400
    
    if check_password_hash(user.password, password):
      token = jwt.encode(
        {"id": user.id, "exp": datetime.utcnow + timedelta(minutes=60)},
        SECRET_KEY,
        algorithm="HS256"
      )
      return jsonify({"token": token})
    return jsonify({"message": "Contraseña incorrecta. Vuelva a intertarlo."}), 400

  except Exception as ex:
    return jsonify({"message": str(ex)})
  

@user_bp.route("/signup", methods=["POST"])
def signup():
  try:
    data = request.json
    username = data["username"]
    password = generate_password_hash(data["password"])
    email = data["email"]

    user = UserModel(username, password, email)
    db.session.add(user)
    db.session.commit()

    return for_him.jsonify(user)

  except Exception as ex:
    return jsonify({"message": str(ex)}), 400