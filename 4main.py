#default value parameter
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
def get_user(name: str = None, price: int = 0):
    return {"name": name, 
            "price": price}

#http://127.0.0.1:8000/items?name=Prathama will print default price value will be printed

#http://127.0.0.1:8000/items?name=Prathama&price=1000 will print price = 1000