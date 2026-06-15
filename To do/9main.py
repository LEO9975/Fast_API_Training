#all http modules
#get- receiving data (searching)
#post- sending data (login userid and pass input)
#put- complete data change
#patch- partial data change
#delete- delete data

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

todos = [] #temporary in-memory database

#pydantic schema
class Todo(BaseModel):
    id: int
    title: str
    completed: bool

@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return{
        "message": "Todo added",
        "data": todo
    }

#fetch all todos
@app.get("/todos")
def get_todos():
    return todos

#Fetch a single todo by id
@app.get("/todos/{todo_id}")
def get_single_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return {"error":"Todo not found"}

#updating todos
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return {
                "message": "Data Updates",
                "data": updated_todo
            }
    return {"error": "Todo not found"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message": "Data deleted"}
    return {"error": "Todo not found"}