#get method
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "Welcome FastApi"}

@app.get("/about")
def about():
    return {"about":"This websitr is about ecommerce"}

@app.get("/contact")
def contact():
    return {"owner":"7020940430"}

@app.get("/search")
def search():
    return {"search":"type what you're looking for"}

@app.get("/product")
def product():
    return {"product":"Is this what you're searching for??"}