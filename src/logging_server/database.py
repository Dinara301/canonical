from typing import Dict

import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder

from src.logging_server.models import LogItem

MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.log
collection = database.get_collection("service_log")


def get_db_session():
    return collection


# Add a new log into to the database
async def add_log(log_item: LogItem, db) -> object:
    encoded = jsonable_encoder(log_item)
    print(encoded)
    log = await db.insert_one(encoded)
    return log
