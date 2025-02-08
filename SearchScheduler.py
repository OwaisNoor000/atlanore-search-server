import os
import dotenv
import requests
import time
from getColors import getColors
import copy
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import re



class SearchScheduler:
    def __init__(self):
        self.productsDBPath = "data/products.txt"
        self.productIndexesPath = "productIndexes"
        self.productImagePath = "sock_images"
        
        dotenv.load_dotenv()
        self.SHOPIFY_STORE = os.getenv("SHOPIFY_STORE")
        self.SHOPIFY_ACCESS_TOKEN = os.getenv('ADMINTOKEN')
        self.PRODUCTS_URL = f"https://{self.SHOPIFY_STORE}/admin/api/2023-10/products.json?limit=250"

        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        # create new log
        self.today = time.strftime("%Y-%m-%d")

    def _products(self):
        product = []

        temp_product_url = copy.deepcopy(self.PRODUCTS_URL)
        
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.SHOPIFY_ACCESS_TOKEN
        }

        response = requests.get(temp_product_url,headers=headers)
        product.extend(response.json()["products"])
        
        while True:
            last_id = product[-1]["id"]
            temp_product_url += f"&since_id={last_id}"
            response = requests.get(temp_product_url,headers=headers)
            print(len(response.json()["products"]))
            if len(response.json()["products"])==0:
                break
            product.extend(response.json()["products"])

        return product

    def _convert_shopify_url(self,url):
        return re.sub(r"https://cdn\.shopify\.com/s/files/\d+/\d+/\d+/files/", "/cdn/shop/files/", url)

    def updateProducts(self):

        logs = []

        logs.append("running updateProducts process") 
        print("running updateProducts process") 

        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.SHOPIFY_ACCESS_TOKEN
        }
        products = self._products()


        #persist product details
        details = {}
        for product in products:
            name = product["title"]
            img_url = product["image"]["src"]
            img_url = self._convert_shopify_url(img_url)
            current_price = product["variants"][0]["price"]
            old_price = product["variants"][0]["compare_at_price"]
            variant = product["handle"]

            details[name] = [name,img_url,current_price,old_price,variant]


        with open('data/product_details.json', 'w') as f:
            json.dump(details, f, indent=4)  # indent=4 for pretty printing

        logs.append(f"Retrived products: {len(products)}")
        print(f"Retrived products: {len(products)}")

        products = [product for product in products if product["status"] == "active"]

        logs.append(f"Found {len(products)} active products")
        print(f"Found {len(products)} active products")

        with open(self.productsDBPath,"w",encoding="UTF-8") as file:
            for product in products:
                file.write(product["title"]+"\n")

        logs.append("Wrote products to productsDB")
        print("Wrote products to productsDB")

        # write the logs
        with open(f"logs/{self.today}.log","a",encoding="UTF-8") as file:
            for log in logs:
                file.write(log+"\n")
            file.write("\n\n\n")

    # def indexProductsDB(self):

    #     logs = []
    #     logs.append("running indexProductDB process")
    #     print("running indexProductDB process")

    #     # read productsDB
    #     products = []
    #     with open("data/products.txt","r",encoding="UTF-8") as file:
    #         products = file.readlines()

    #     products = [product.replace("\n","") for product in products]

    #     logs.append(f"Read {len(products)} products from productsDB")
    #     print("running indexProductDB process")

    #     # Create documents
    #     # documents = []
    #     # for product in products:
    #     #     document = Document(text=product)
    #     #     documents.append(document)
    #     chunk_size = 2
    #     chunks = [products[i:i + chunk_size] for i in range(0, len(products), chunk_size)]
    #     documents = []
    #     for chunk in chunks:
    #         document = Document(text="\n".join(chunk))
    #         documents.append(document)

    #     logs.append(f"Created {len(documents)} documents")
    #     print(f"Created {len(documents)} documents")

    #     # create and persist the indexes
    #     index = VectorStoreIndex.from_documents(documents)
    #     index.storage_context.persist(persist_dir=self.productIndexesPath)


    #     logs.append(f"Persisted indexes to {self.productIndexesPath}")
    #     print(f"Persisted indexes to {self.productIndexesPath}")
    #     with open(f"logs/{self.today}.log","a",encoding="UTF-8") as file:
    #         for log in logs:
    #             file.write(log+"\n")
    #         file.write("\n\n\n")

    def embedProducts(self):
        logs = []
        logs.append("running embedProducts Process")
        print("running embedProducts Process")

        products = []
        with open("data/products.txt","r",encoding="UTF-8") as file:
            products = file.readlines()
        products = [product.replace("\n","") for product in products]
        logs.append(f"Read {len(products)} products from productsDB")
        print(f"Read {len(products)} products from productsDB")

        product_embeddings = self.model.encode(products)
        np.save("data/embeddings.npy", product_embeddings)
        logs.append(f"Saved embeddings of size {product_embeddings.shape} to data/embeddings.npy")
        print(f"Saved embeddings of size {product_embeddings.shape} to data/embeddings.npy")

        with open(f"logs/{self.today}.log","a",encoding="UTF-8") as file:
            for log in logs:
                file.write(log+"\n")
            file.write("\n\n\n")




    def updateProductImages(self):

        logs = []
        logs.append("Running updateProductColors process")
        print("Running updateProductColors process")
        
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.SHOPIFY_ACCESS_TOKEN
        }

        products = self._products()
        images_in_dir = os.listdir("sock_images")
        images_in_dir = [os.path.splitext(img)[0] for img in images_in_dir] # remove file extension

        logs.append(f"Retrieved {len(products)} products")
        print(f"Retrieved {len(products)} products")
        logs.append(f"read {len(images_in_dir)} existing product names")
        print(f"read {len(images_in_dir)} existing product names")

        for product in products:
            if product["title"] not in images_in_dir:
                logs.append(f"{product["title"]} doesnt exist in dir")
                print(f"checking product {product["title"]}")
                url = product["image"]["src"]
                response = requests.get(url)
                if response.status_code == 200:
                    # Open a file in write-binary mode to save the image
                    try:
                        with open(f"sock_images/{product["title"]}.jpg", "wb") as file:
                            file.write(response.content)
                    except Exception as e:
                        print(f"failed to download image {product["title"]}")
                        logs.append(f"failed to download image {product["title"]}")
                else:
                    logs.append("Failed to download the image. Status code:", product)
                    print(f"checking product {product["title"]}")

        with open(f"logs/{self.today}.log","a",encoding="UTF-8") as file:
            for log in logs:
                file.write(log+"\n")
            file.write("\n\n\n")

    def updateProductColors(self):
        print("getting colors from new images")
        getColors()
        print("getting colors from new images")

    def runBatchProcess(self):
        self.updateProducts()
        self.embedProducts()
        self.updateProductImages()
        self.updateProductColors()

sched = SearchScheduler()
sched.runBatchProcess()

