#!/usr/bin/env python
import os

from flask import Flask
from pymongo import MongoClient
from flask import request

app = Flask(__name__)
mongo_url = 'mongodb+srv://chinh:575xQvf7lGNFuGFl@cluster-01.kz6vr.mongodb.net/'

client = MongoClient(mongo_url)

@app.route('/')
def todo():
    try:
        client.admin.command('ismaster')
    except:
        return "Server not available"
    return "Hello from the MongoDB client!\n"


@app.route('/users')
def list_users():
    db = client.crud
    collection = db.users
    users = collection.find()
    return f"Users: {', '.join([user['name'] for user in users])}\n"

@app.route('/users', methods=['POST'])
def create_user():

    db = client.crud
    collection = db.users
    user = request.json
    result = collection.insert_one(user)
    return f"User created with id: {result.inserted_id}\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
