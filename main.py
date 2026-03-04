from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

items = {}

@app.get("/", tags=["Root"])
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to EverpayAPI!"}

@app.post("/items", response_model=Item, tags=["Item"])
async def create_item(item: Item):
    items[item.name] = item
    return item.dict()

@app.get("/items", response_model=list[Item], tags=["Item"])
async def get_all_items():
    return [item.dict() for item in items.values()]

@app.get("/items/{name}", response_model=Item, tags=["Item"])
async def read_item(name: str):
    if name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[name].dict()

@app.put("/items/{name}", response_model=Item, tags=["Item"])
async def update_item(name: str, item: Item):
    if name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[name] = item
    return item.dict()

@app.delete("/items/{name}", tags=["Item"])
async def delete_item(name: str):
    if name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[name]
    return {"detail": "Item deleted"}
