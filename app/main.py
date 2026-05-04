from fastapi import FastAPI, HTTPException
from typing import List
# load the relevant classes and methods from the models and storage modules
from .models import Product, ProductCreate
from .storage import products, current_id, save_products, load_products
from contextlib import asynccontextmanager


# FastAPI is about defining how your server exposes and enforces a contract over HTTP.
async def lifespan(app: FastAPI):
    load_products()
    yield
    
app = FastAPI()

# Defining argument data types in Python, see: https://www.geeksforgeeks.org/python/explicitly-define-datatype-in-a-python-function/


# using a products dict
@app.post("/products", response_model=Product, status_code=201)
def create_product(payload: ProductCreate):
    global current_id
    new_product = Product(id=current_id, **payload.dict())
    print(f"Payload new_product: {new_product}")
    print(f"Payload as Dict new_product: {new_product.dict()}")
    products[current_id] = new_product
    # print(f"Type products: {type(products)}")
    print(f"Payload products: {products}")
    save_products()
    current_id += 1    
    return new_product

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/products/{id}", response_model=Product)
def read_product(id: int):
    product = products.get(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # return the following response to client:
    return product
    

@app.get("/products", response_model=List[Product])
def read_all_products():
    return list(products.values()) 

# @app.get("/products", response_model=dict[int, Product])
# def read_all_products():
#     return products


# using a products dict
@app.put("/products/{id}", response_model=Product)
def update_product(id: int, payload: ProductCreate):
    if id not in products:
    # # k = products.keys()
    # # if id not in k:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = Product(id=id, **payload.dict())
    products[id] = updated_product        
            # return the following response to client in JSON (key-value) format:
    save_products()
    return updated_product

# using a products dict
@app.delete("/products/{id}", response_model=Product)
def delete_product(id: int):
    if id not in products:
    # k = products.keys()
    # if id not in k:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = products.pop(id)
    save_products()
    return deleted
    

