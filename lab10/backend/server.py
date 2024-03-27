from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

def load_products():
    with open('products.json', 'r') as file:
        return json.load(file)["products"]
    
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

@app.route("/product-images/<path:filename>")
def get_image(filename):
    return send_from_directory("product-images", filename)

if __name__ == "__main__":
    app.run(debug=True)
