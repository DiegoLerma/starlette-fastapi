from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson import ObjectId
from models import ItemModel
from schemas import ItemSchema
from database import item_collection

app = FastAPI()


def convert_object_id(obj: Any) -> Any:
    if isinstance(obj, list):
        return [convert_object_id(item) for item in obj]
    if isinstance(obj, dict):
        return {k: convert_object_id(v) for k, v in obj.items()}
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj


@app.post("/items/", response_description="Add new item", response_model=ItemSchema)
async def create_item(item: ItemModel):
    item = jsonable_encoder(item)
    new_item = await item_collection.insert_one(item)
    created_item = await item_collection.find_one({"_id": new_item.inserted_id})

    if created_item is not None:
        created_item = convert_object_id(created_item)
        return JSONResponse(status_code=201, content=jsonable_encoder(created_item))
    else:
        raise HTTPException(status_code=404, detail="Item not found after insertion")


@app.get("/items/", response_description="List all items", response_model=list[ItemSchema])
async def list_items():
    items = await item_collection.find().to_list(1000)
    items = convert_object_id(items)
    return items


@app.get("/items/{id}", response_description="Get a single item", response_model=ItemSchema)
async def show_item(id: str):
    item = await item_collection.find_one({"_id": ObjectId(id)})
    if item is not None:
        item = convert_object_id(item)
        return item
    raise HTTPException(status_code=404, detail=f"Item {id} not found")


@app.put("/items/{id}", response_description="Update an item", response_model=ItemSchema)
async def update_item(id: str, item: ItemModel):
    if item := {k: v for k, v in item.dict().items() if v is not None}:
        update_result = await item_collection.update_one({"_id": ObjectId(id)}, {"$set": item})

        if update_result.modified_count == 1:
            updated_item = await item_collection.find_one({"_id": ObjectId(id)})
            if updated_item is not None:
                updated_item = convert_object_id(updated_item)
                return updated_item

    existing_item = await item_collection.find_one({"_id": ObjectId(id)})
    if existing_item is not None:
        existing_item = convert_object_id(existing_item)
        return existing_item

    raise HTTPException(status_code=404, detail=f"Item {id} not found")


@app.delete("/items/{id}", response_description="Delete an item")
async def delete_item(id: str):
    delete_result = await item_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=204, content="")

    raise HTTPException(status_code=404, detail=f"Item {id} not found")
