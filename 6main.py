#post method
from fastapi import FastAPI

app = FastAPI()

@app.post("/create")
def create_user(name: str, age: int, clg: str, sem: str):
    return {
        "msg": "User Creation",
        "data": {
            "name": name,
            "age": age,
            "clg": clg,
            "sem": sem
        }
    }

