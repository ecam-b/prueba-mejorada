from flask import Blueprint, request, jsonify
# models and schemas
from models.BillModel import BillModel, BillSchema
for_him = BillSchema()
for_them = BillSchema(many=True)
# database
from database.db import db
# security
from token_required import token_required

bill_bp = Blueprint("bill", __name__)


@bill_bp.route("/", methods=["GET"])
@token_required
def get_all_bills(usuario_actual):
  """
  Obtener todos las Bills
  Obtener todas las Bills registradas en la base de datos.
  ---
  tags:
  - Bill
  parameters:
    - name: x-access-token
      in: header
      type: string
      required: true
      description: Token de autentificación.
  responses:
    200:
      description: OK
      schema:
        type: object
        properties:
          date_bill:
            type: date
            description: Fecha de creación de la bill.
          user_id: 
            type: integer
            description: Usuario que crea la bill.
          value: 
            type: integer
            description: Valor de la bill.
          type:
            type: integer
            description: Tipo de bill.
          observation: 
            type: string
            description: Observación adicional sobre la bill.
        example:
          date_bill: "12-12-12"
          user_id: 1
          value: 10
          type: 1
          observation: "Todo correcto"
    400:
      description: No se pueden mostrar la Bills.
    500:
      description: Error en el servidor.
  """
  try:
    bills = BillModel.query.all()
    result = for_them.dump(bills)
    return jsonify(result)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400
  

@bill_bp.route("/", methods=["POST"])
@token_required
def add_bill(usuario_actual):
  """
  Registrar una Bill
  Registrar una nueva bill en la base de datos.
  ---
  tags:
  - Bill
  parameters:
    - name: x-access-token
      in: header
      type: string
      required: true
      description: Token de autentificación.
    - name: bill
      in: body
      required: true
      description: Datos para registrar una nueva bill.
      schema:
        type: object
        properties:
          date_bill:
            type: date
            description: Fecha de creación de la bill.
          user_id: 
            type: integer
            description: Usuario que crea la bill.
          value: 
            type: integer
            description: Valor de la bill.
          type:
            type: integer
            description: Tipo de bill.
          observation: 
            type: string
            description: Observación adicional sobre la bill.
        example:
          date_bill: "12-12-12"
          user_id: 1
          value: 10
          type: 1
          observation: "Todo correcto"
  responses:
    200:
      description: OK
      schema:
        type: object
        properties:
          date_bill:
            type: date
            description: Fecha de creación de la bill.
          user_id: 
            type: integer
            description: Usuario que crea la bill.
          value: 
            type: integer
            description: Valor de la bill.
          type:
            type: integer
            description: Tipo de bill.
          observation: 
            type: string
            description: Observación adicional sobre la bill.
        example:
          date_bill: "12-12-12"
          user_id: 1
          value: 10
          type: 1
          observation: "Todo correcto"
    400:
      description: No se pueden mostrar la Bills.
    500:
      description: Error en el servidor.
  """
  try:
    data = request.json
    date_bill = data["date_bill"]
    user_id = data["user_id"]
    value = data["value"]
    type = data["type"]
    observation = data["observation"]

    bill = BillModel(date_bill, user_id, value, type, observation)
    db.session.add(bill)
    db.session.commit()

    return for_him.jsonify(bill)

  except Exception as ex:
    return jsonify({"message": str(ex)})
  

@bill_bp.route("/<id>", methods=["PUT"])
@token_required
def update_bill(usuario_actual, id):
  """
  Actualizar una Bill
  Actualizar una bill en la base de datos.
  ---
  tags:
  - Bill
  parameters:
    - name: x-access-token
      in: header
      type: string
      required: true
      description: Token de autentificación.
    - name: id
      in: path
      required: true
      description: ID de la Bill.
      type: integer
    - name: bill
      in: body
      required: true
      description: Datos para actualizar una bill.
      schema:
        type: object
        properties:
          date_bill:
            type: date
            description: Fecha de creación de la bill.
          user_id: 
            type: integer
            description: Usuario que actualiza la bill.
          value: 
            type: integer
            description: Valor de la bill.
          type:
            type: integer
            description: Tipo de bill.
          observation: 
            type: string
            description: Observación adicional sobre la bill.
        example:
          date_bill: "12-12-12"
          user_id: 1
          value: 10
          type: 1
          observation: "Todo correcto"
  responses:
    200:
      description: OK
      schema:
        type: object
        properties:
          date_bill:
            type: date
            description: Fecha de creación de la bill.
          user_id: 
            type: integer
            description: Usuario que actualiza la bill.
          value: 
            type: integer
            description: Valor de la bill.
          type:
            type: integer
            description: Tipo de bill.
          observation: 
            type: string
            description: Observación adicional sobre la bill.
        example:
          date_bill: "12-12-12"
          user_id: 1
          value: 10
          type: 1
          observation: "Todo correcto"
    400:
      description: No se pueden mostrar la Bills.
    500:
      description: Error en el servidor.
  """
  try:
    bill = BillModel.query.get(id)
    if not bill:
      return jsonify({"message": "Bill no encontrada."}), 400
    
    data = request.json
    if data["date_bill"]:
      bill.date_bill = data["date_bill"]
    if data["user_id"]:
      bill.user_id = data["user_id"]
    if data["value"]:
      bill.value = data["value"]
    if data["type"]:
      bill.type = data["type"]
    if data["observation"]:
      bill.observation = data["observation"]
    
    db.session.commit()
    return for_him.jsonify(bill)

  except Exception as ex:
    return jsonify({"message": str(ex)})


@bill_bp.route("/<id>", methods=["DELETE"])
@token_required
def delete_bill(usuario_actual, id):
  """
  Eliminar una Bill
  Eliminar una bill en la base de datos.
  ---
  tags:
  - Bill
  parameters:
    - name: x-access-token
      in: header
      type: string
      required: true
      description: Token de autentificación.
    - name: id
      in: path
      required: true
      description: ID de la Bill.
      type: integer
  responses:
    200:
      description: OK
      schema:
        type: object
        properties:
          date_bill:
            type: date
            description: Fecha de creación de la bill.
          user_id: 
            type: integer
            description: Usuario que actualiza la bill.
          value: 
            type: integer
            description: Valor de la bill.
          type:
            type: integer
            description: Tipo de bill.
          observation: 
            type: string
            description: Observación adicional sobre la bill.
        example:
          date_bill: "12-12-12"
          user_id: 1
          value: 10
          type: 1
          observation: "Todo correcto"
    400:
      description: No se pueden mostrar la Bills.
    500:
      description: Error en el servidor.
  """
  try:
    bill = BillModel.query.get(id)
    if not bill:
      return jsonify({"message": "Bill no encontrada."}), 400
    
    db.session.delete(bill)
    db.session.commit()
    return for_him.jsonify(bill)
  except Exception as ex:
    return jsonify({"message": str(ex)})