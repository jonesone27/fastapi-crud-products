import json
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from typing import List
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from fastapi import HTTPException





# FastAPI is about defining how your server exposes and enforces a contract over HTTP.
app = FastAPI()

products = []
current_id = 1

class Tags(Enum):
    FRUIT = 'fruit'
    FRESH = 'fresh'
    SNACK = 'snack'
    SWEET = 'sweet'
    DAIRY = 'dairy'
    VEGAN = 'vegan'
    MISC = 'misc'

class Supplier(BaseModel):
    name: str 
    contact_email: Optional[str] = None

class Product(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(..., max_length=20)
    price: Decimal = Field(max_digits=5, decimal_places=2)
    is_offer: bool = False
    tags: List[Tags] = Field(default_factory=list)
    supplier: Optional[Supplier] = None
# Regarding default_factory, see: https://dev.to/devasservice/python-trick-using-dataclasses-with-fielddefaultfactory-4159

# A field is required if and only if:
    # it has no default value
    # OR explicitly uses Field(...)
class ProductCreate(BaseModel):
    # model_config = ConfigDict(strict=True)    
    name: str = Field(..., max_length=20)
    price: Decimal = Field(max_digits=5, decimal_places=2)
    is_offer: bool = False
    # default for tags = empty list
    tags: List[Tags] = Field(default_factory=list)
    supplier: Optional[Supplier] = None

class ProductUpdate(BaseModel):
    # model_config = ConfigDict(strict=True)    
    name: str = Field(..., max_length=20)
    price: Decimal = Field(max_digits=5, decimal_places=2)
    is_offer: bool = False
    tags: List[Tags] = Field(default_factory=list)
    supplier: Optional[Supplier] = None

# Defining argument data types in Python, see: https://www.geeksforgeeks.org/python/explicitly-define-datatype-in-a-python-function/

@app.post("/products", response_model=Product, status_code=201)
def create_product(payload: ProductCreate):
    global current_id
    # Product requires an ID
    new_product = Product(id=current_id, **payload.dict())
    products.append(new_product)

    current_id += 1
    # return the following response to client:
    return new_product


# Function matches {id} with id argument in read_product(id: int)
@app.get("/products/{id}", response_model=Product)
def read_product(id: int):
    for product in products:
        if product.id == id:
            # return the following response to client:
            return product
    raise HTTPException(status_code=404, detail="Product not found")
    
@app.get("/products", response_model=List[Product])
def read_all_products():
    return products



@app.put("/products/{id}", response_model=Product)
def update_product(id: int, payload: ProductCreate):
    for i, product in enumerate(products):
        if product.id == id:
            updated_product = Product(id=id, **payload.dict())
            products[i] = updated_product
            # return the following response to client in JSON (key-value) format:
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{id}", response_model=Product)
def delete_product(id: int):
    for i, product in enumerate(products):
        if product.id == id:
            return products.pop(i)
    raise HTTPException(status_code=404, detail="Product not found")

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
