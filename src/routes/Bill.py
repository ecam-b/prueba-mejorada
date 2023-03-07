from flask import Blueprint, request, jsonify
# models and schemas
from models.BillModel import BillModel, BillSchema
for_him = BillSchema()
for_them = BillSchema(many=True)

bill_bp = Blueprint("bill", __name__)


@bill_bp.route("/")
def get_all_bills():
  try:
    bills = BillModel.query.all()
    result = for_them.dump(bills)
    return jsonify(result)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400