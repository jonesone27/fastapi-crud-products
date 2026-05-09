from fastapi import FastAPI, HTTPException
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

@app.get("/products/{id}", response_model=Product)
def read_product(id: int):
    product = storage.products.get(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # return the following response to client:
    return product
    
@app.get("/products", response_model=dict[int, Product])
def read_all_products(min_price: Decimal | None = None):
    
    if min_price is None:
        return storage.products
        
    filtered_products = {}

    for key, product in storage.products.items():
        if product.price >= min_price:
            filtered_products[key] = product            
    return filtered_products

    

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
    
    # try:
    #     for field, name in updated_product.items():
                        
    #         if (current_product.name != updated_product["name"] and (updated_product["name"] != "string"):
    #             current_product.name = updated_product["name"]
    #         else: print(f"Entered mandatory value for 'name' is identical or not valid!")
    #         if (current_product.price != updated_product["price"] and (updated_product["price"] >= 0):
    #             current_product.price = updated_product["price"]
    #         else: print(f"Entered mandatory value for 'price' is identical or not valid!")
    #         if current_product.is_offer != updated_product["is_offer"]:
    #             current_product.price = updated_product["price"]        
    #         if (current_product.tags != []) and (current_product.tags != updated_product["tags"]:
    #             current_product.tags.clear
    #             current_product.tags.extend(updated_product["tags"]
    #         if (updated_product["supplier"]["name"]) is not None and updated_product["supplier"]["name"]) != "string") and (current_product.supplier.name != updated_product["supplier"]["name"])):
    #             current_product.supplier.name = updated_product["supplier"]["name"])
    #         else: print(f"Entered value for 'supplier name' is identical or not valid!")
    #         if (updated_product["supplier"]["contact_email"]) is not None and updated_product["supplier"]["contact_email"]) !="string") and (current_product.supplier.contact_email != updated_product["supplier"]["contact_email"])):
    #             current_product.supplier.contact_email = updated_product["supplier"]["contact_email"])
    #         else: print(f"Entered value for 'supplier e-mail address' is identical or not valid!")
    #         storage.save_products()
    #     # return storage.products[key]
    #     return current_product               

# DOES THIS WORK???
# See: https://realpython.com/ref/builtin-functions/setattr/
                if field == "price":
                    setattr(current_product, field, value)
             and value != "string":
                current_product.name = value
            else: print(f"Entered mandatory value for 'name' is identical or not valid!")
            if (current_product.price != updated_product["price"] and (updated_product["price"] >= 0):
                current_product.price = updated_product["price"]
            else: print(f"Entered mandatory value for 'price' is identical or not valid!")
            if current_product.is_offer != updated_product["is_offer"]:
                current_product.price = updated_product["price"]        
            if (current_product.tags != []) and (current_product.tags != updated_product["tags"]:
                current_product.tags.clear
                current_product.tags.extend(updated_product["tags"]
            if (updated_product["supplier"]["name"]) is not None and updated_product["supplier"]["name"]) != "string") and (current_product.supplier.name != updated_product["supplier"]["name"])):
                current_product.supplier.name = updated_product["supplier"]["name"])
            else: print(f"Entered value for 'supplier name' is identical or not valid!")
            if (updated_product["supplier"]["contact_email"]) is not None and updated_product["supplier"]["contact_email"]) !="string") and (current_product.supplier.contact_email != updated_product["supplier"]["contact_email"])):
                current_product.supplier.contact_email = updated_product["supplier"]["contact_email"])
            else: print(f"Entered value for 'supplier e-mail address' is identical or not valid!")
            storage.save_products()
        # return storage.products[key]
        

# using a products dict
@app.delete("/products/{id}", response_model=Product)
def delete_product(id: int):
    if id not in storage.products:
    # k = products.keys()
    # if id not in k:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = storage.products.pop(id)
    storage.save_products()
    return deleted
    

