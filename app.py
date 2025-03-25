import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from db import db
from models import User, Item

app = Flask(__name__)

# MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0003@localhost/flask_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['JWT_SECRET_KEY'] = 'superjwtsecretkey'

# upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  

# database reset
db.init_app(app)
jwt = JWTManager(app)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200


# register point
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)

    with app.app_context():
        db.session.add(new_user)
        db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# Create new item
@app.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    current_user = get_jwt_identity()
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    new_item = Item(name=name, description=description, owner=current_user)

    with app.app_context():
        db.session.add(new_item)
        db.session.commit()

    return jsonify({"message": "Item created successfully"}), 201


# Read all
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    result = [{"id": item.id, "name": item.name, "description": item.description, "owner": item.owner} for item in items]
    return jsonify(result), 200


# Read One
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    result = {"id": item.id, "name": item.name, "description": item.description, "owner": item.owner}
    return jsonify(result), 200


# Update item
@app.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    current_user = get_jwt_identity()
    if item.owner != current_user:
        return jsonify({"error": "You do not have permission to update this item"}), 403

    data = request.get_json()
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)

    with app.app_context():
        db.session.commit()

    return jsonify({"message": "Item updated successfully"}), 200


# Delete item
@app.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    current_user = get_jwt_identity()
    
    with app.app_context():
        item = db.session.get(Item, item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    if item.owner != current_user:
        return jsonify({"error": "You do not have permission to delete this item"}), 403

    with app.app_context():
        db.session.delete(item)
        db.session.commit()

    return jsonify({"message": "Item deleted successfully"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # database table
    app.run(debug=True)