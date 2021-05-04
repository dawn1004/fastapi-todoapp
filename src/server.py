from fastapi import FastAPI, HTTPException
from .schema import Todo
import uuid
import pymongo
from pymongo import MongoClient
import certifi

##connect to db
client = MongoClient("mongodb+srv://dawnhae:dawn12374@cluster0.hcrzr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
database = client["todo-list"]
collection = database["todo"]


app = FastAPI()

todos = []


@app.get("/todo/")
async def get_add_todos():
    todos = collection.find({})
    return list(todos)

@app.get("/todo/{id}")
async def get_todo(id: str):
    todo = collection.find_one({"_id": id})
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todo/")
async def add_todo(todo: Todo):
    todo.id = str(uuid.uuid4())
    collection.insert_one({
        "_id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "isDone": todo.isDone
    })
    return todo


@app.put("/todo/{id}")
async def update_todo(id: str):
    todo = collection.find_one({"_id": id})
    if todo:
        collection.update_one({"_id": id}, {"$set": {"isDone": not todo["isDone"]}})
        todo["isDone"] = not todo["isDone"]
        return todo

    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todo/{id}")
async def delete_todo(id: str):
    todo = collection.find_one({"_id": id})
    if todo:
        collection.delete_one({"_id": id})
        todos = collection.find({})
        return list(todos)
    raise HTTPException(status_code=404, detail="Todo not found")


