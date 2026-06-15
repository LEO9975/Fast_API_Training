#pydantic is a separate class used only for validation of data
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.post("/create")
def create_user(user: User):
    return {
        "msg":"User Created",
        "data": user
    }