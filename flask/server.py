#!/usr/bin/env python
import os

from flask import Flask, jsonify
from pymongo import MongoClient
from flask import request
from bson import ObjectId

app = Flask(__name__)
mongo_url = 'mongodb+srv://chinh:575xQvf7lGNFuGFl@cluster-01.kz6vr.mongodb.net/'

client = MongoClient(mongo_url)
db = client.crud

@app.route('/')
def todo():
    try:
        client.admin.command('ismaster')
    except:
        return "Server not available"
    return "Hello from the MongoDB client!\n"

def sanitize_request_data(request):
    allowed_fields = ['address', 'avatar', 'email', 'gender', 'name', 'phone', 'rule', 'status']
    return {field: request[field] for field in allowed_fields if field in request}

@app.route('/users/<id>')
def get_user(id):
    collection = db.users
    user = collection.find_one({'_id': ObjectId(id)})
    if user is None:
        return "User not found", 404
    user['_id'] = str(user['_id'])
    return jsonify(user)

@app.route('/users', methods=['GET'])
def list_users():
    collection = db.users
    users = list(collection.find({}))
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    collection = db.users
    request_data = request.json
    user = sanitize_request_data(request_data)
    result = collection.insert_one(user)
    if result.inserted_id is None:
        return jsonify({"message": "User created failed"}), 500
    inserted_id = str(result.inserted_id)
    return jsonify({"_id": inserted_id, "message": "User created successfully"}), 201

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    collection = db.users
    request_data = request.json
    user = sanitize_request_data(request_data)
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': user})
    if result.modified_count == 0:
        return jsonify({"message": "User updated failed"}), 500
    return jsonify({"message": "User updated successfully"}), 200

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    collection = db.users
    result = collection.delete_one({'_id': ObjectId(id)})
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
