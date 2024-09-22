from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

products_bp = Blueprint('products', __name__)

mongo_url = 'mongodb://mongo:27017/'
client = MongoClient(mongo_url)
db = client.crud

def sanitize_product_data(request):
    allowed_fields = ['name', 'description', 'price', 'category', 'quantity', 'status', 'imageUrl']
    return {field: request[field] for field in allowed_fields if field in request}

@products_bp.route('/products', methods=['GET'])
def list_products():
    collection = db.products
    products = list(collection.find({}))
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products)

@products_bp.route('/products/<id>', methods=['GET'])
def get_product(id):
    collection = db.products
    product = collection.find_one({'_id': ObjectId(id)})
    if product is None:
        return jsonify({"message": "Product not found"}), 404
    product['_id'] = str(product['_id'])
    return jsonify(product)

@products_bp.route('/products', methods=['POST'])
def create_product():
    collection = db.products
    request_data = request.json
    product = sanitize_product_data(request_data)
    exist_product = collection.find_one({"name": product["name"]})
    if exist_product:
        return jsonify({"message": "Product already exists"}), 400
    result = collection.insert_one(product)
    if result.inserted_id is None:
        return jsonify({"message": "Product creation failed"}), 500
    inserted_id = str(result.inserted_id)
    return jsonify({"_id": inserted_id, "message": "Product created successfully"}), 201

@products_bp.route('/products/<id>', methods=['PUT'])
def update_product(id):
    collection = db.products
    request_data = request.json
    product = sanitize_product_data(request_data)
    if not collection.find_one({"_id": ObjectId(id)}):
        return jsonify({"message": "Product not found"}), 404
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': product})
    if result.modified_count == 0:
        return jsonify({"message": "Product update failed"}), 500
    return jsonify({"message": "Product updated successfully"}), 200

@products_bp.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    collection = db.products
    product = collection.find_one({'_id': ObjectId(id)})
    if product is None:
        return jsonify({"message": "Product not found"}), 404
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"message": "Product deleted failed"}), 500
    return jsonify({"message": "Product deleted successfully"}), 200