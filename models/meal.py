from database import db

class Meal(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String(300))
  on_diet = db.Column(db.Boolean(), nullable={False})
  created_at = db.Column(db.DateTime)
  updated_at = db.Column(db.DateTime)