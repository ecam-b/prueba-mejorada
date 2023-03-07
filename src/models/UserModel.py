from database.db import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class UserModel(db.Model):
  __tablename__ = "user"


  id = db.Column(db.Integer, primary_key=True, nullable=False)
  username = db.Column(db.String(50))
  password = db.Column(db.String(500))
  email = db.Column(db.String(100))


  def __init__(self, username, password, email):
    self.username = username
    self.password = password
    self.email = email


class UserSchema(ma.Schema):
  class Meta:
    fields = ("id", "password", "email")