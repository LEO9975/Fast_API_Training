from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Address(BaseModel):
    city: str
    pincode: int

class User(BaseModel):
    name: str
    age: int
    add: Address #linking address model 

#creating route
@app.post("/create")
def create_user(user: User):
    return user