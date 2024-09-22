from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

users_bp = Blueprint('users', __name__)

mongo_url = 'mongodb://mongo:27017/'
client = MongoClient(mongo_url)
db = client.crud

def sanitize_request_data(request):
    allowed_fields = ['address', 'avatar', 'email', 'gender', 'name', 'phone', 'rule', 'status']
    return {field: request[field] for field in allowed_fields if field in request}

@users_bp.route('/users/<id>')
def get_user(id):
    collection = db.users
    user = collection.find_one({'_id': ObjectId(id)})
    if user is None:
        return jsonify({"message": "User not found"}), 404
    user['_id'] = str(user['_id'])
    return jsonify(user)

@users_bp.route('/users', methods=['GET'])
def list_users():
    collection = db.users
    users = list(collection.find({}))
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

@users_bp.route('/users', methods=['POST'])
def create_user():
    collection = db.users
    request_data = request.json
    user = sanitize_request_data(request_data)
    exist_user = collection.find_one({"email": user["email"]})
    if exist_user:
        return jsonify({"message": "User already exists"}), 400
    result = collection.insert_one(user)
    if result.inserted_id is None:
        return jsonify({"message": "User created failed"}), 500
    inserted_id = str(result.inserted_id)
    return jsonify({"_id": inserted_id, "message": "User created successfully"}), 201

@users_bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    collection = db.users
    request_data = request.json
    user = sanitize_request_data(request_data)
    if not collection.find_one({"_id": ObjectId(id)}):
        return jsonify({"message": "User not found"}), 404
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': user})
    if result.modified_count == 0:
        return jsonify({"message": "User updated failed"}), 500
    return jsonify({"message": "User updated successfully"}), 200

@users_bp.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    collection = db.users
    result = collection.delete_one({'_id': ObjectId(id)})
    return jsonify(result)