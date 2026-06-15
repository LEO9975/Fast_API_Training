from fastapi import FastAPI

app = FastAPI()

@app.get("/user")
def get_user(name: str = None):
    return {"name": name}

 #http://127.0.0.1:8000/user?name=amol if name is given in the url in this format, it will print the name, but if input is not given it will show null