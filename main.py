from typing import Any
from fastapi import FastAPI, HTTPException, Response
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


@app.post("/items/",
          response_description="Add new item",
          response_model=ItemSchema)
async def create_item(item: ItemModel):
    item = jsonable_encoder(item)
    new_item = await item_collection.insert_one(item)
    created_item = await item_collection.find_one(
        {"_id": new_item.inserted_id})

    if created_item is not None:
        created_item = convert_object_id(created_item)
        return JSONResponse(
            status_code=201, content=jsonable_encoder(created_item))
    else:
        raise HTTPException(
            status_code=404, detail="Item not found after insertion")


@app.get("/items/",
         response_description="List all items",
         response_model=list[ItemSchema])
async def list_items():
    items = await item_collection.find().to_list(1000)
    items = convert_object_id(items)
    return items


@app.get("/items/{item_id}",
         response_description="Get a single item",
         response_model=ItemSchema)
async def show_item(item_id: str):
    item = await item_collection.find_one({"_id": ObjectId(item_id)})
    if item is not None:
        item = convert_object_id(item)
        return item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app.put("/items/{item_id}",
         response_description="Update an item",
         response_model=ItemSchema)
async def update_item(item_id: str, item: ItemModel):
    update_data = {k: v for k, v in item.dict().items() if v is not None}

    if update_data:  # Verificamos si hay datos para actualizar
        update_result = await item_collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_data})

        if update_result.modified_count == 1:
            updated_item = await item_collection.find_one(
                {"_id": ObjectId(item_id)})
            if updated_item is not None:
                updated_item = convert_object_id(updated_item)
                return updated_item

    existing_item = await item_collection.find_one({"_id": ObjectId(item_id)})
    if existing_item is not None:
        existing_item = convert_object_id(existing_item)
        return existing_item

    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app.delete("/items/{item_id}", response_description="Delete an item")
async def delete_item(item_id: str):
    delete_result = await item_collection.delete_one(
        {"_id": ObjectId(item_id)})

    if delete_result.deleted_count == 1:
        # Aquí devolvemos una respuesta 204 sin cuerpo explícito
        return Response(status_code=204)

    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
