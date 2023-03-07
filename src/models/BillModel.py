from database.db import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()


class BillModel(db.Model):
  __tablename__ = "bill"


  id = db.Column(db.Integer, primary_key=True, nullable=False)
  date_bill = db.Column(db.Date)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
