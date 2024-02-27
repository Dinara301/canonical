import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder

from src.logging_server.models import LogItem

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.log

collection = database.get_collection("service_log")


# Add a new log into to the database
async def add_log(log_item: LogItem) -> object:
    log = await collection.insert_one(jsonable_encoder(log_item))
    return log
