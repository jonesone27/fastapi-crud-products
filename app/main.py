from fastapi import FastAPI, HTTPException
from typing import List
# load the relevant classes and methods from the models and storage modules
from .models import Product, ProductCreate
from .storage import products, current_id, save_products, load_products

# FastAPI is about defining how your server exposes and enforces a contract over HTTP.
app = FastAPI()

# Defining argument data types in Python, see: https://www.geeksforgeeks.org/python/explicitly-define-datatype-in-a-python-function/



# @app.post("/products", response_model=Product, status_code=201)
# def create_product(payload: ProductCreate):
#     global current_id
#     # Product requires an ID
#     new_product = Product(id=current_id, **payload.dict())
#     products.append(new_product)
#     current_id += 1
#     # return the following response to client:
#     return new_product

#
# using a products list
# @app.post("/products", status_code=201)
# def create_product(payload: ProductCreate):
#     global current_id
#     new_product = Product(id=current_id, **payload.dict())
#     # print(f"Type new_product: {type(new_product)}")
#     # print(f"Payload new_product: {new_product}")
#     print(f"Payload as Dict new_product: {new_product.dict()}")
#     products.append(new_product)
#     # print(f"Type products: {type(products)}")
#     print(f"Payload products: {products}")
#     current_id += 1
#     return {"ok": True}

# using a products dict
@app.post("/products", status_code=201)
def create_product(payload: ProductCreate):
    global current_id
    new_product = Product(id=current_id, **payload.dict())
    print(f"Payload as Dict new_product: {new_product.dict()}")
    products.update({current_id:new_product})
    # print(f"Type products: {type(products)}")
    print(f"Payload products: {products}")
    save_products()
    current_id += 1    
    return {"ok": True}

@app.get("/")
def root():
    return {"message": "API is running"}

# Function matches {id} with id argument in read_product(id: int)
# # using a products list
# @app.get("/products/{id}", response_model=Product)
# def read_product(id: int):
#     for product in products:
#         if product.id == id:
#             # return the following response to client:
#             return product
#     raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/{id}", response_model=Product)
def read_product(id: int):
    product = products.get(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # return the following response to client:
    return product
    
# using a products list
# @app.get("/products", response_model=List[Product])
# def read_all_products():
#     return products

@app.get("/products", response_model=List[Product])
def read_all_products():
    return products 

# @app.get("/products", response_model=dict[int, Product])
# def read_all_products():
#     return products

# # using a products list
# @app.put("/products/{id}", response_model=Product)
# def update_product(id: int, payload: ProductCreate):
#     for i, product in enumerate(products):
#         if product.id == id:
#             updated_product = Product(id=id, **payload.dict())
#             products[i] = updated_product
#             return the following response to client in JSON (key-value) format:
#             return updated_product
#     raise HTTPException(status_code=404, detail="Product not found")

# using a products dict
@app.put("/products/{id}", response_model=Product)
def update_product(id: int, payload: ProductCreate):
    k = products.keys()
    if id not in k:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = Product(id=id, **payload.dict())
    products.update({id:updated_product})        
            # return the following response to client in JSON (key-value) format:
    save_products()
    return updated_product

# # using a products list
# @app.delete("/products/{id}", response_model=Product)
# def delete_product(id: int):
#     for i, product in enumerate(products):
#         if product.id == id:
#             deleted = products.pop(i)
#             save_products()
#             return deleted
#     raise HTTPException(status_code=404, detail="Product not found")

# using a products dict
@app.delete("/products/{id}", response_model=Product)
def delete_product(id: int):
    k = products.keys()
    if id not in k:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = products.pop(id)
    save_products()
    return deleted
    

# This is fine, but: lookup = O(n) (linear search); i.e. not scalable
# Later: dict or database; But don’t change it yet. You’re still learning the mechanics.

# NEXT: Implement PUT /products/{id} using a Python list without breaking your current logic (dict would also be possible but is avoided due to flatter learning curve for you).


# @app.put("/products/{id}", response_model=Product)
# def update_product(id: int, update_product: ProductCreate):
#     i = 0
#     for product in products:
#         if product.id == id:
#             product = Product(id=id, **update_product.dict())
#             products[i] = product
#             # return the following response to client in JSON (key-value) format:
#             return product
#         # increment i in any case until product is returned or exception is raised
#         i += 1
#     raise HTTPException(status_code=404, detail="Product not found")

# @app.delete("/products/{id}", response_model=Product)
# def delete_product(id: int):
#     i=0
#     for product in products:
#         if product.id == id:
#             products.pop(i)
#             # the pop() method by default return the deleted index
#             return products.pop(i)
#         i +=1
#     raise HTTPException(status_code=404, detail="Product not found")




# @app.patch("products/{id}")
# def update_fields(id: int, name | None = None, price | None = None, is_offer | None = None, tag_dict_items | None = None, supplier | None = None):
#     for product in products:
#         if product.id == id:
#             if name is not None:
#                 product.name = name
#             if price is not None:
#                 product.price = price
#             if is_offer is not None:
#                 product.is_offer = is_offer
#             if tag_dict_items is not None:
#                 product.tags = tag_dict_items
#             if name is not None:
#                 product.name = name
#             if supplier is not None:
#                 product.supplier = supplier
