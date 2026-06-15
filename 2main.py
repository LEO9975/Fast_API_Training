#dynamic url
from fastapi import FastAPI

app = FastAPI()

@app.get("/user/{user_id}")
def  get_user(user_id: int): #int is used for inputing only int value.... this is called validation
    return {"user id": user_id}