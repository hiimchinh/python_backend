#!/usr/bin/env python
import os

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongo:27017")

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
