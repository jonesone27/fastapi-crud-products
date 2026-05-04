import json
from .models import Product
from fastapi.encoders import jsonable_encoder

# products = []
products = {}
current_id = 1

# for products as dict
def save_products():
    data = [p.dict() for p in products.values()]
    with open("data/products.json", "w") as f:
        json.dump(jsonable_encoder(data), f, indent=2)
# json.dump(indent) -> If a positive integer or string, JSON array elements and object members will be pretty-printed with that indent level. 



# for products as list
# def save_products():
#     data = [p.dict() for p in products]
#     with open("data/products.json", "w") as f:
#         json.dump(data, f, indent=2)


def load_products():
    global products, current_id
    try:
        with open("data/products.json", "r") as f:
            data = json.load(f)
            # add to products dict using "id" from Json as id
            products = {item["id"]: Product(**item) for item in data}
            current_id = max(products.keys(), default=0) + 1
            # The max() function returns the item with the highest value, or the item with the highest value in an iterable.
    except FileNotFoundError:
        print("File not found")
        products = {}
        current_id = 1
        