from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://127.0.0.1:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)

# Base de datos
database = client.starlet_db

# Colección
item_collection = database.get_collection("items")
