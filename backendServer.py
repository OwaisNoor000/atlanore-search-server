from flask import Flask, jsonify, request
from flask_cors import CORS
import os,json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})
#CORS(app, resources={
 #   r"/*": {"origins": ["http://127.0.0.1:5500", "http://127.0.0.1:9292","https://atlanore.com/","https://atlanoresearch.raggleai.com"]}
#})Owais
CORS(app)

with open("data/product_details.json") as file:
    product_details = json.load(file)


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
products = []
with open("data/products.txt","r",encoding="UTF-8") as file:
    products = file.readlines()
products = [product.replace("\n","") for product in products]

def remove_duplicates(lst):
    unique_list = []
    
    for item in lst:
        if item not in unique_list:
            unique_list.append(item)
    
    return unique_list

@app.route('/')
def home():
    return "Welcome to the Flask App!"

@app.route("/feeling-llm-response",methods=['GET'])
def get_feeling_llm_response():

    referer = request.headers.get('Referer')
    origin = request.headers.get('Origin')
    print(f"Referer: {referer}")
    print(f"Origin: {origin}")

    #input
    query = request.args.get('query',default="Tired")
    print(query)

    #process
    products = []
    with open("data/products.txt","r",encoding="UTF-8") as file:
        products = file.readlines()
    products = [product.replace("\n","") for product in products]

    product_embeddings = np.load("data/embeddings.npy")
    keyword_embedding = model.encode([query])  # Single keyword query
    similarity_scores = cosine_similarity(keyword_embedding, product_embeddings)[0]  # Extract first row
    top_n = 20
    top_indices = np.argsort(similarity_scores)[::-1][:top_n]  # Sort in descending order
    result = []
    for idx in top_indices:
        result.append(products[idx])

    result = remove_duplicates(result)

    # output (list)
    print("this is the data we are sending from the server",result)
    details = [product_details[key] for key in result if key in product_details]
    data={
        'imgList': list(details)
    }

    return jsonify(data)

@app.route("/color-llm-response",methods=['GET'])
def get_color_llm_response():
    color1 = request.args.get('color1',default="white")
    # color2 = request.args.get('color2',default="black")

    with open('data/color.json', 'r',encoding="UTF-8") as file:
        color_data = json.load(file)

    colorsmatching = []
    for color in color_data:
        if color1 in color['colors']:
            colorsmatching.append(color['name'])

    details = [product_details[os.path.splitext(key)[0]] for key in colorsmatching if os.path.splitext(key)[0] in product_details]
    
    data = {
        "imgList" : details
    }

    print(data)

    return jsonify(data)


@app.route("/return-products-list")
def fetch_products_list():
    arg = request.args.get("products")
    products_list = arg.split(",")

    details = [product_details[key] for key in products_list if key in product_details]
    data = {
        "imgList":details
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run()
