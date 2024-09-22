#!/usr/bin/env python
import os

from flask import Flask, jsonify
from pymongo import MongoClient
from flask import request
from bson import ObjectId
from products import products_bp
from users import users_bp
app = Flask(__name__)
app.register_blueprint(products_bp)
app.register_blueprint(users_bp)
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
