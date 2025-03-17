from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Configure CORS first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
database: Dict[int, dict] = {}

# Pydantic model
class Item(BaseModel):
    name: str
    description: str

# API Routes
@app.get("/items")
def get_items():
    return database

@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in database:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    database[item_id] = item.dict()
    return {"message": "Item created", "item": database[item_id]}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    database[item_id] = item.dict()
    return {"message": "Item updated", "item": database[item_id]}

@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: Item):
    if item_id not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    database[item_id].update(item.dict(exclude_unset=True))
    return {"message": "Item patched", "item": database[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    del database[item_id]
    return {"message": "Item deleted"}

# Mount static files LAST
app.mount("/", StaticFiles(directory="static", html=True), name="static")