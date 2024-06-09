from flask import Flask, jsonify, request
from database import db
from datetime import datetime, timezone
from models.meal import Meal

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet'

db.init_app(app)

@app.route('/meal', methods=['POST'])
def register_meal():
  data = request.json
  name = data["name"]
  description = data["description"]
  created_at = datetime.now(timezone.utc)
  on_diet = data["on_diet"]
  
  if name and on_diet:
    meal = Meal(name=name, description=description, created_at=created_at, on_diet=on_diet)
    db.session.add(meal)
    db.session.commit()
    return jsonify({"message": "Meal has been successfully registered!"})
  
  return jsonify({"message": "Required fields are not filled"}), 400

@app.route('/meal/<int:id_meal>', methods=['PUT'])
def update_meal(id_meal):
  meal = db.session.get(Meal, id_meal)
  if not meal:  
    return jsonify({"message": "Meal not found"}), 404

  data = request.json
  name = data.get('name')
  on_diet = data.get('on_diet')

  if name is None or on_diet is None:
    return jsonify({"message": "Name and on diet fields are required!"}), 400

  meal.name = name
  meal.description = data.get('description')
  meal.on_diet = on_diet
  meal.updated_at = datetime.now(timezone.utc)

  db.session.commit()

  return jsonify({"message": f"Meal {id_meal} has been successfully updated!"})

@app.route('/meal/<int:id_meal>', methods=['DELETE'])
def delete_meal(id_meal):
  meal = db.session.get(Meal, id_meal)
  if not meal:
    return jsonify({"message": "Meal not found"}), 404
  
  db.session.delete(meal)
  db.session.commit()
  return jsonify({"message": f"Meal {id_meal} was successfully removed!"})


if __name__ == '__main__':
  app.run(debug=True)