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
