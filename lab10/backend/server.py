from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, origins=["http://example.com", "http://localhost:3000"])

def load_products():
    with open('products.json', 'r') as file:
        return json.load(file)["products"]

# ----------- GET specific or all --------------
@app.route("/products", methods = ["GET"])
@app.route("/products/<int:product_id>", methods = ["GET"])
def get_products(product_id = None):
    products = load_products()
    if product_id is None:
        '''This return statement creates and returns an object with all products
        with a key called products '''
        return jsonify({"products": products})
    else:
        product = next((p for p in products if p["id"] == product_id), None)
        '''
        if a specific product is requested we wrap that in an object then ship it off with 
        the key products
        '''
        return jsonify(product) if product else ("", 404)
    
# ----------- POST (create new product) ------------
@app.route("/products/add", methods=["POST"])
def add_product():
    new_product = request.json
    products = load_products()

    '''
    This way of handling ID number is pretty bad since it creates an issue where deleting a product
    then adding a product causes that new product to take the ID of the old deleted product
    I assume that isn't an issue for this lab but its useful for us to know and acknowledge
    '''
    new_product["id"] = len(products) + 1
    products.append(new_product)
    with open('products.json', 'w') as file:
        json.dump({"products": products}, file)
    return jsonify(new_product), 201

# ------ Get an image -----------
@app.route("/product-images/<path:filename>")
def get_image(filename):
    return send_from_directory("product-images", filename)

# ----------- PUT (update existing product) ----------
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    products = load_products()
    product_index = None
    for index, p in enumerate(products):
        if p["id"] == product_id:
            product_index = index
            break
    if product_index is not None:
        '''
        request.json is taking all the additional information we pass to the backend
        (like brand, price, quantity etc etc through postman) and converting that to json 
        format
        '''
        update_product = request.json 
        products[product_index].update(update_product)
        with open('products.json','w') as file:
            json.dump({"products": products}, file)
        return jsonify(products[product_index]), 200

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    products = load_products()
    product_index = None
    for index, product in enumerate(products):
        if product["id"] == product_id:
            product_index = index
            break
    if product_index is not None:
        '''
        products is like a copy of the backend so after the changes we need to dump
        it in order to have it persist
        '''
        products.pop(product_index)
        with open('products.json', 'w') as file:
            json.dump({"products": products}, file)
        """
        Return statements send information back to client. However with deletions there
        isn't anything to return back to client since we already updated the json on our backend
        with the deletion so we just send back nothing along with the status code
        """
        return "", 204
    else:
        return "", 404


if __name__ == "__main__":
    app.run(debug=True)
