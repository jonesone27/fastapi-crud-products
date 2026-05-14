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

products = {}
current_id = 1

class Tags(Enum):
    FRUIT = 'fruit'
    VEGAN = 'vegan'
    BAKERY = 'bakery'
    WHOLEGRAIN = 'wholegrain'
    EGGS = 'eggs'
    ORGANIC = 'organic'
    DAIRY = 'dairy'
    CHEESE = 'cheese'
    VEGETABLE = 'vegetable'
    PANTRY = 'pantry'
    OIL = 'oil'
    PASTA = 'pasta'
    BEVERAGE = 'beverage'
    JUICE = 'juice'
    YOGURT = 'yogurt'
    SPREAD = 'spread'
    NUT = 'nut'
    LEGUMES = 'legumes'
    MEAT = 'meat'
    FRESH = 'fresh'
    COFFEE = 'coffee'
    BREAKFAST = 'breakfast'
    FISH = 'fish'
    TEA = 'tea'
    SNACK = 'snack'
    SWEET = 'sweet'
    HERB = 'herb'
    STARCH = 'starch'
    CITRUS = 'citrus'
    PROTEIN = 'protein'
    SWEETENER = 'sweetener'
    SALAD = 'salad'
    GRAIN = 'grain'
    TROPICAL = 'tropical'
    FROZEN = 'frozen'
    SEASONAL = 'seasonal'
    CONDIMENT = 'condiment'
    WATER = 'water'
    CAPSICUM = 'capsicum'
    MISC = 'misc'

class Supplier(BaseModel):
    name: str 
    contact_email: str | None

# Field(default_factory=list), i.e. create an empty list if no value is provided,
# Fields enable validation inside Pydantic models, see also https://fastapi.tiangolo.com/tutorial/body-fields/?h=field
class Product(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(..., max_length=50)
    price: Decimal = Field(max_digits=5, decimal_places=2)
    is_offer: bool = False
    tags: List[Tags] = Field(default_factory=list)
    supplier: Supplier | None 
# Regarding default_factory, see: https://dev.to/devasservice/python-trick-using-dataclasses-with-fielddefaultfactory-4159

# A field is required if and only if:
    # it has no default value
    # OR explicitly uses Field(...)
class ProductCreate(BaseModel):
    # model_config = ConfigDict(strict=True)    
    name: str = Field(..., max_length=50)
    price: Decimal = Field(max_digits=5, decimal_places=2)
    is_offer: bool = False
    # default for tags = empty list
    tags: List[Tags] = Field(default_factory=list)
    supplier: Supplier | None = Field(default=None)


class ProductPatch(BaseModel):
    name: str | None = Field(max_length=50, default=None) 
    price: Decimal | None = Field(max_digits=5, decimal_places=2, default=None) 
    is_offer: bool | None  = Field(default=None)
    tags: List[Tags] | None = Field(default=None)
    supplier: Supplier | None = Field(default=None)

# class ProductUpdate(BaseModel):
#     # model_config = ConfigDict(strict=True)    
#     name: str = Field(..., max_length=50)
#     price: Decimal = Field(max_digits=5, decimal_places=2)
#     is_offer: bool = False
#     tags: List[Tags] = Field(default_factory=list)
#     supplier: Optional[Supplier] = None

