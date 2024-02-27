import datetime

from dateutil import parser
import pprint
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
    #encoded = jsonable_encoder(log_item, custom_encoder={datetime.datetime: lambda date_obj: date_obj})
    encoded = log_item.model_dump()
    pprint.pprint(encoded)
    log = await db.insert_one(encoded)
    return log


def convert_to_datetime(key: str, value: str):
    if not key.endswith('_timestamp'):
        return value
    return parser.parse(value)


# TODO: that can be done by available packages with more generic approach, for this case it's enough to have custom func
def convert_dict_to_mongo_query(filters: Dict):
    if not filters:
        return filters
    pprint.pprint(filters)
    query = {'$and': []}
    for key, value in filters.items():
        if (len(value)) == 1:
            query['$and'].append({key: convert_to_datetime(key, value[0])})
            continue
        partial_filter = {'$or': []}
        for v in value:
            partial_filter['$or'].append({key: convert_to_datetime(key, v)})
        query['$and'].append(partial_filter)
    pprint.pprint(query)
    return query


async def get_log(filters: Dict, limit: int, db):
    query = convert_dict_to_mongo_query(filters)
    result = []
    async for log in db.find(query, limit=limit):
        pprint.pprint(log)
        result.append(log)
    return result
