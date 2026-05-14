from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List
# load the relevant classes and methods from the models and storage modules
from .models import Product, ProductCreate, ProductPatch
# load the storage file as an object from all files to prevent Python from loading the empty products dict from any files but only from storage.py (as object)
from . import storage
from contextlib import asynccontextmanager
from decimal import Decimal


# Lifespan, see https://fastapi.tiangolo.com/advanced/events/#async-context-manager
# FastAPI is about defining how your server exposes and enforces a contract over HTTP.
# load only the products dict from storage.py
async def lifespan(app: FastAPI):
    storage.load_products()
    yield

app = FastAPI(lifespan=lifespan)

# Defining argument data types in Python, see: https://www.geeksforgeeks.org/python/explicitly-define-datatype-in-a-python-function/


# using a products dict
@app.post("/products", response_model=Product, status_code=201)
def create_product(payload: ProductCreate):
    new_product = Product(id=storage.current_id, **payload.dict())
    print(f"Payload new_product: {new_product}")
    print(f"Payload as Dict new_product: {new_product.dict()}")
    storage.products[storage.current_id] = new_product
    # print(f"Type products: {type(products)}")
    print(f"Payload products: {storage.products}")
    storage.save_products()
    storage.current_id += 1    
    return new_product

@app.get("/")
def root():
    return {"message": "API is running"}

# @app.get("/products", response_model=dict[int, Product])
@app.get("/products", response_model=list[Product])
def read_all_products(min_price: Decimal | None = None, sorting_asc: bool | None=None, limit:int | None = None, offset:int | None=None):
    
    if (limit is not None and offset is not None):
        product_list = list(storage.products.values())
        filtered_list = product_list[offset:offset+limit]
        print(filtered_list)
        return filtered_list


# nur den Preis der Listen-Items ausgeben und dann mit min-price vergleichen!
    if (min_price is None and sorting_asc is None):
        prod_list = list(storage.products.values())
        print(prod_list)
        return prod_list

    if (min_price is not None and sorting_asc is None):
        prod_list = list(storage.products.values())
        min_list = []
        for product in prod_list:
            if product.price >= min_price:
                min_list.append(product)
        # for i in prod_list:
        #     print(prod_list[i])
        print(min_list)   
        return min_list
    

    if (min_price is None and sorting_asc is True):            
            sorted_products = sorted(storage.products.values(), key=lambda products: products.price)            
            print(sorted_products)            
            return sorted_products

#   if (min_price is None and sorting_asc is True):
#         sorted_products = sorted(storage.products.items(), key=lambda items: items[1].price)
#         print(jsonable_encoder(dict(sorted_products)))
#         return sorted_products


    #     filtered_products = {}

    #     for i in storage.products.values():
    #         if product.price >= min_price:
    #             filtered_products[key] = product
    #             print(product)            
    #     return list(filtered_products)


    # if (min_price is not None and sorting_asc is None):
    #     filtered_products = {}

    #     for key, product in storage.products.items():
    #         if product.price >= min_price:
    #             filtered_products[key] = product
    #             print(product)            
    #     return list(filtered_products)
# # Dict dorting works internally, but JSON object viewers may reorder dictionary keys because dictionaries (unlike lists) are not ideal ordered transport structures.
#   




@app.get("/products/{id}", response_model=Product)
def read_product(id: int):
    product = storage.products.get(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # return the following response to client:
    return product
    

    

# using a products dict
@app.put("/products/{id}", response_model=Product)
def update_product(id: int, payload: ProductCreate):
    if id not in storage.products:
           raise HTTPException(status_code=404, detail="Product not found")
    updated_product = Product(id=id, **payload.dict())
    storage.products[id] = updated_product        
            # return the following response to client in JSON (key-value) format:
    storage.save_products()
    return updated_product


# Regarding model_dump(), see https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump
# loop through values; if values of new =! old values -> replace, return product
@app.patch("/products/{id}", response_model=Product)
def update_product_fields(id: int, payload: ProductPatch):

    if id not in storage.products:
        raise HTTPException(status_code=404, detail="Product not found")
    current_product = storage.products[id]
    updated_product = payload.model_dump(exclude_unset=True)

    
    for field, value in updated_product.items():
        if value is not None:
            setattr(current_product, field, value)
    storage.save_products()
    return current_product 


# using a products dict
@app.delete("/products/{id}", response_model=Product)
def delete_product(id: int):
    if id not in storage.products:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = storage.products.pop(id)
    # ensure persistence
    storage.save_products()
    return deleted
    

