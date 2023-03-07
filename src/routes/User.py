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
  """
  Inicio de sesión
  Inicio de sesión para un usuario existente.
  ---
  tags:
  - User
  parameters:
    - name: login
      in: body
      required: true
      description: Datos de inicio de sesión.
      schema:
        type: object
        properties:
          username:
            type: string
            description: Usuario.
          password:
            type: string
            description: Password del usuario.
        example:
          username: "Pablo"
          password: "12345" 
  responses:
    200:
      description: OK
      schema: 
        type: object
        properties:
          token:
            type: string
            description: Token de acceso.
        example:
          token "qwertyuiolkjhgfdsasxdcvb"
    400:
      description: Usuario o contraseña incorrecto.
    500:
      description: Error del servidor.
  """
  try:
    data = request.json
    username = data["username"]
    password = data["password"]

    user = UserModel.query.filter_by(username = data["username"]).first()
    if user == None:
      return jsonify({"message": "Usuario no encontrado. Por favor realice el registro de un nuevo usuario."}), 400
    
    if check_password_hash(user.password, password):
      token = jwt.encode(
        {"id": user.id, "exp": datetime.utcnow() + timedelta(minutes=60)},
        SECRET_KEY,
        algorithm="HS256"
      )
      return jsonify({"token": token})
    return jsonify({"message": "Contraseña incorrecta. Vuelva a intertarlo."}), 400

  except Exception as ex:
    return jsonify({"message": str(ex)})
  

@user_bp.route("/signup", methods=["POST"])
def signup():
  """
  Registro de usuario
  Registro de un nuevo usuario
  ---
  tags:
  - User
  parameters:
    - name: user
      in: body
      required: true
      description: Datos para el registro del usuario.
      schema:
        type: object
        properties:
          username: 
            type: string
            description: Nombre de Usuario.
          password:
            type: string
            description: Password del usuario.
          email:
            type: string
            description: Email del usuario.
        example:
          username: "Pablo"
          password: "12345"
          email: "pablo@gmail.com"
  responses:
    200:
      description: OK
      schema:
        type: object
        properties:
          username: 
            type: string
            description: Nombre de Usuario.
          password:
            type: string
            description: Password del usuario.
          email:
            type: string
            description: Email del usuario.
        example:
          username: "Pablo"
          password: "12345"
          email: "pablo@gmail.com"
    400:
      description: No es posible registrar este usuario.
    500:
      description: Error del servidor.
  """
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