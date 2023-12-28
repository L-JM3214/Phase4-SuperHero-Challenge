from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database-file.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    from models import Hero 
    heroes = Hero.query.all()
    return jsonify([{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes])

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
    return jsonify({'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers})

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([{'id': power.id, 'name': power.name, 'description': power.description} for power in powers])

@app.route('/powers/<int:power_id>', methods=['GET', 'PATCH'])
def get_or_patch_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    if request.method == 'GET':
        return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
    elif request.method == 'PATCH':
        data = request.get_json()
        if 'description' not in data:
            return jsonify({"error": "Description is required for PATCH"}), 400

        power.description = data['description']

        try:
            db.session.commit()
            return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if not all([hero_id, power_id, strength]):
        return jsonify({"error": "All fields are required"}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if not hero or not power:
        return jsonify({"error": "Hero or Power not found"}), 404

    hero_power = HeroPower(hero=hero, power=power, strength=strength)
    db.session.add(hero_power)

    try:
        db.session.commit()
        return jsonify(hero_power.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5555)
