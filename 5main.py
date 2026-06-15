from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
def get_pro(limit: int = 0):
    return {"limit": 10}