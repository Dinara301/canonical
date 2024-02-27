from datetime import datetime

from dateutil import parser
import pprint
from typing import Dict

import motor.motor_asyncio

from src.logging_server.models import LogItem

MONGO_DETAILS = "mongodb://mongodb:27017"
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
def convert_dict_to_mongo_query(filters: Dict, last_seen_datetime: datetime):
    if not filters and not last_seen_datetime:
        return filters
    pprint.pprint(filters)
    query = {'$and': []}
    if last_seen_datetime:
        query['$and'].append({'event_timestamp': {'$gt': last_seen_datetime}})
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


async def get_log(filters: Dict, limit: int, last_seen_datetime: datetime, db):
    query = convert_dict_to_mongo_query(filters, last_seen_datetime)
    result = []
    async for doc in db.find(query, limit=limit):
        # TODO: there're nicer ways to skip _id field (in Pydantic model)
        doc.pop('_id')
        result.append(doc)
    pprint.pprint(result)
    return result
