from typing import Optional
from pydantic import BaseModel, Field

class Customer(BaseModel):
    customerId: int=Field()
    customerFName: str=Field(default=None)
    customerLName: str=Field(default=None)
    customerEmail: str=Field(default=None)
    customerPassword: str=Field(default=None)
    customerStreet: str=Field(default=None)
    customerCity: str=Field(default=None)
    customerState: str=Field(default=None)
    customerZipcode: str=Field(default=None)

    class Config():
        schema_extra = {
            "example": {
                "customerId": "1",
                "customerFName": "Mahmut",
                "customerLName": "Tuncer",
                "customerEmail": "mahmut.tuncer@vbo.local",
                "customerPassword": "Ankara06",
                "customerStreet": "Mecburiyet Street",
                "customerCity": "Adıyaman",
                "customerState": "DA",
                "customerZipcode": "02400"
            }
        }

class ShowCustomer(BaseModel):
    customerId: Optional[int] = None
    customerFName: Optional[str] = None
    customerLName: Optional[int] = None
    # If we want to use this as response model
    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class Showuser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True