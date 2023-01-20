import os

import openai
import requests
import json
from flask import Flask, request, render_template, session
import uuid
from datetime import datetime
from PIL import Image
from io import BytesIO
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
openai.api_key = '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'
SHOP_ID = 6427144
upload_image_endpoint = 'https://api.printify.com/v1/uploads/images.json'
get_image_endpoint = 'https://api.printify.com/v1/uploads.json'
create_product_endpoint = 'https://api.printify.com/v1/shops/6427144/products.json'
get_products_endpoint = 'https://api.printify.com/v1/shops/6427144/products.json'
upload_image_key = '6d207e02198a847aa98d0a2a901485a5'
printify_api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6IjczY2JhYmM0YTczMDE1YWE5MTJkMmRhZGVhYjkxMDQ2ZGZlYTUyODkzMjM3NmZmZDM0OWE2NWYzMTkzYWVlMGVkZTI0N2YyZWM0NGViMjFmIiwiaWF0IjoxNjcyODQ2Nzk5Ljk4NjA3NywibmJmIjoxNjcyODQ2Nzk5Ljk4NjA3OSwiZXhwIjoxNzA0MzgyNzk5Ljk2MzU3Miwic3ViIjoiMTEyNTk1MDUiLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIl19.AP_p_fjY4alfm5nsaARDmyKx0GoFpfFMFRnAlSfe5B0HGkOD-J13JLBqulB9DVKDBH3fDNghOIL6hfGsGYA'

@app.route("/", methods=["GET", "POST"])
def generate_image():
    product_dict = {}
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )

        image_url = response['data'][0]['url']
        create_image = cloudinary.uploader.upload(image_url, public_id = "my_image", width=500, height=380, crop="scale")

        og_image_url = cloudinary.CloudinaryImage(create_image["url"]).build_url()

        unique_filename = str(datetime.now())
        data={'file_name': unique_filename, 'url': og_image_url}
        header = {'Authorization': 'Bearer ' + printify_api_key}
        headers={'Authorization': 'Bearer ' + printify_api_key, 'Content-type': 'application/json'}
        r = requests.post(upload_image_endpoint, json=data, headers=headers)
        x = requests.get(get_image_endpoint, headers=header)
        xjson = x.json()
        image_id = 0
        for image in xjson["data"]:
            if image["file_name"] == unique_filename:
                image_id = image["id"]

  #       product_data = {
  #   "title": "White T-Shirt ",
  #   "description": prompt + " on T-Shirt" ,
  #   "blueprint_id": 5,
  #   "print_provider_id": 61,
  #   "variants": [
  #         {
  #             "id": 17643,
  #             "price": 400,
  #             "is_enabled": True
  #         }
  #     ],
  #     "print_areas": [
  #       {
  #         "variant_ids": [17643],
  #         "placeholders": [
  #           {
  #             "position": "front",
  #             "images": [
  #                 {
  #                   "id": image_id, 
  #                   "x": 0.5, 
  #                   "y": 0.5, 
  #                   "scale": 1,
  #                   "angle": 0
  #                 }
  #             ]
  #           }
  #         ]
  #       }
  #     ]
  # }
        
  #       poster_data = {
  #   "title": "Premium Matte Vertical Poster ",
  #   "description": prompt + " poster" ,
  #   "blueprint_id": 282,
  #   "print_provider_id": 2,
  #   "variants": [
  #         {
  #             "id": 62103,
  #             "price": 400,
  #             "is_enabled": True
  #         },

  #         {
  #           "id": 43135,
  #             "price": 400,
  #             "is_enabled": True
  #         },

  #         {
  #           "id": 43138,
  #             "price": 400,
  #             "is_enabled": True
  #         },

  #         {
  #           "id": 43141,
  #             "price": 400,
  #             "is_enabled": True
  #         },

  #         {
  #           "id": 43144,
  #             "price": 400,
  #             "is_enabled": True
  #         },

  #         {
  #           "id": 43147,
  #             "price": 400,
  #             "is_enabled": True
  #         },

  #         {
  #           "id": 43150,
  #             "price": 400,
  #             "is_enabled": True
  #         }
  #     ],
  #     "print_areas": [
  #       {
  #         "variant_ids": [62103, 43135, 43138, 43141, 43144, 43147, 43150],
  #         "placeholders": [
  #           {
  #             "position": "front",
  #             "images": [
  #                 {
  #                   "id": image_id, 
  #                   "x": 0.5, 
  #                   "y": 0.5, 
  #                   "scale": 1,
  #                   "angle": 0
  #                 }
  #             ]
  #           }
  #         ]
  #       }
  #     ]
  # }
        
  #       notebook_data = {
  #   "title": "Notebook ",
  #   "description": prompt + " on notebook" ,
  #   "blueprint_id": 1194,
  #   "print_provider_id": 94,
  #   "variants": [
  #         {
  #             "id": 91850,
  #             "price": 400,
  #             "is_enabled": True
  #         }
  #     ],
  #     "print_areas": [
  #       {
  #         "variant_ids": [91850],
  #         "placeholders": [
  #           {
  #             "position": "front",
  #             "images": [
  #                 {
  #                   "id": image_id, 
  #                   "x": 0.5, 
  #                   "y": 0.5, 
  #                   "scale": 1,
  #                   "angle": 0
  #                 }
  #             ]
  #           }
  #         ]
  #       }
  #     ]
  # }
        
        
  #       post_product = requests.post(create_product_endpoint, json=product_data, headers=headers)
  #       post_poster_product = requests.post(create_product_endpoint, json=poster_data, headers=headers)
  #       post_mug_product = requests.post(create_product_endpoint, json=notebook_data, headers=headers)

        canvas_data = {
    "title": "Matte Canvas (12 inches x 9 Inches) ",
    "description": prompt + " artwork" ,
    "blueprint_id": 937,
    "print_provider_id": 105,
    "variants": [
          {
              "id": 82218,
              "price": 3299,
              "is_enabled": True
          }
      ],
      "print_areas": [
        {
          "variant_ids": [82218],
          "placeholders": [
            {
              "position": "front",
              "images": [
                  {
                    "id": image_id, 
                    "x": 0.5, 
                    "y": 0.5, 
                    "scale": 1,
                    "angle": 0
                  }
              ]
            }
          ]
        }
      ]
  }
        
        post_canvas = requests.post(create_product_endpoint, json=canvas_data, headers=headers)
        get_products = requests.get(get_products_endpoint, headers=header)
        get_products_json = get_products.json()

        for x in range(1):
          product_id = get_products_json["data"][x]["id"]
          product_image_url = get_products_json["data"][x]["images"][0]["src"]
          product_title = get_products_json["data"][x]["title"]
          product_dict.update({"product" + str(x): {"product_id": product_id, "product_image_url": product_image_url, "product_title": product_title}})

        return render_template("index.html", image_url=image_url, product_dict=product_dict)
    return render_template("index.html", product_dict=product_dict)

@app.route("/add_to_cart/<product_id>")
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(product_id)
    return "Product added to cart!"

@app.route("/cart")
def cart():
    cart_items = []
    header = {'Authorization': 'Bearer ' + printify_api_key}
    get_products = requests.get(get_products_endpoint, headers=header)
    get_products_json = get_products.json()
    if "cart" in session:
      for product_id in session["cart"]:
          for x in range(3):
            if product_id == get_products_json["data"][x]["id"]:
              cart_items.append(product_id)
    else:
      return render_template("cart.html")
    return render_template("cart.html", cart_items=cart_items)


if __name__ == "__main__":
    app.run()

