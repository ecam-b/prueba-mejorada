from database.db import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()


class BillModel(db.Model):
  __tablename__ = "bill"


  id = db.Column(db.Integer, primary_key=True, nullable=False)
  date_bill = db.Column(db.Date)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  value = db.Column(db.Numeric(9))
  type = db.Column(db.Integer)
  observation = db.Column(db.String(120))


  def __init__(self, date_bill, user_id, value, type, observation):
    self.date_bill = date_bill
    self.user_id = user_id
    self.value = value
    self.type = type
    self.observation = observation


class BillSchema(ma.Schema):
  class Meta:
    fields = ("id", "date_bill", "user_id", "value", "type", "observation")
