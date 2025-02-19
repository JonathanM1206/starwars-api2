"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Planet, Character,Favorite


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_user(): 
    user_db=User.query.all() 
    response_body =[]  
    for user in user_db:
        response_body.append(user.serialize())

    return jsonify(response_body), 200 

@app.route('/user<int:user_id>', methods=['GET'])
def get_user_id(): 
    user=User.query.get() 
    if not user: 
       return jsonify("no encontramos el ID user"),400 
    return jsonify(user.serialize()), 200 

@app.route('/planet', methods=['GET'])
def get_all_planet(): 
    planet_db=Planet.query.all() 
    response_body =[]  
    for planet in planet_db:
        response_body.append(planet.serialize())

    return jsonify(response_body), 200  

@app.route('/planet<int:planet_id>', methods=['GET'])
def get_planet_id(): 
    planet=Planet.query.get() 
    if not planet: 
       return jsonify("no encontramos el ID Planet"),400 
    return jsonify(planet.serialize()), 200  

@app.route('/character', methods=['GET'])
def get_all_character(): 
    character_db=Character.query.all() 
    response_body =[]  
    for character in character_db:
        response_body.append(character.serialize())

    return jsonify(response_body), 200   

@app.route('/character<int:character_id>', methods=['GET'])
def get_character_id(): 
    character=Character.query.get() 
    if not character: 
       return jsonify("no encontramos el ID Character"),400 
    return jsonify(character.serialize()), 200   

@app.route('/favorite', methods=['POST'])
def add_favorite(): 
    data=request.get_json() 
    user_id=data.get('user_id') 
    planet_id=data.get('planet_id') 
    character_id=data.get('character_id') 
    if not user_id or (not planet_id and not planet_id): 
        return jsonify({"ERROR":"useri_id y (elplanet_id o people_id)son rqueridos"}),400 
    new_favorite=Favorite(user_id=user_id,planet_id=planet_id,character_id=character_id) 
    db.session.add(new_favorite) 
    db.session.commit()
    return jsonify({"Favorite agregado"}), 200  

@app.route('/favorite', methods=['DELETE'])
def delete_favorite(): 
    data=request.get_json() 
    user_id=data.get('user_id') 
    planet_id=data.get('planet_id') 
    character_id=data.get('character_id') 
    
    if not user_id or (not planet_id and not planet_id): 
        return jsonify({"ERROR":"useri_id y (elplanet_id o people_id)son rqueridos"}),400  
    
    favorite=Favorite.query.filter_by(user_id=user_id,planet_id=planet_id,character_id=character_id).first()  
    if not favorite: 
            return jsonify({"Favorite not found"}), 400  
    
    db.session.delete(favorite) 
    db.session.commit()
    return jsonify({"Favorite deleted"}), 200 

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        db.session.commit()
        return jsonify('planeta borrado'), 200
    return jsonify('no se econtro al planeta'),404  

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character .query.get(character_id)
    if character:
        db.session.commit()
        return jsonify('personaje borrado exitosamente'), 200
    return jsonify('el personaje no existe ne la base de datos'),404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
