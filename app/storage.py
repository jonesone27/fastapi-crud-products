import json
from .models import Product

products = []
current_id = 1

def save_products():
    data = [p.dict() for p in products]
    with open("data/products.json", "w") as f:
        json.dump(data, f, indent=2)
# json.dump(indent) -> If a positive integer or string, JSON array elements and object members will be pretty-printed with that indent level. 


def load_products():
    global products, current_id
    try:
        with open("data/products.json", "r") as f:
            data = json.load(f)
            products = [Product(**item) for item in data]
            current_id = max([p.id for p in products], default=0) + 1
            # The max() function returns the item with the highest value, or the item with the highest value in an iterable.
    except FileNotFoundError:
        products = []
        current_id = 1