import os
from datetime import datetime

from dateutil import parser
from typing import Dict

import motor.motor_asyncio

from src.constants import INDEX_NAME
from src.logging_server.models import LogItem

MONGO_DETAILS = os.environ.get("DATABASE_URL", "mongodb://mongodb:27017")
print(MONGO_DETAILS)
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.log
collection = database.get_collection("service_log")
# TODO: create better indexing
collection.create_index(INDEX_NAME, name="search_index", unique=False)


def get_db_session():
    return collection


async def add_log(log_item: LogItem, db) -> object:
    """
    Add log document to mongodb
    :param log_item: log item to be added, Pydantic LogItem type
    :param db: db collection to write logs
    :return: return inserted object
    """
    encoded = log_item.model_dump()
    log = await db.insert_one(encoded)
    return log


def convert_to_datetime(key: str, value: str) -> datetime:
    """
    Converts values with _timestamp postfix to actual datetime object
    :param key:
    :param value:
    :return:
    """
    if not key.endswith('_timestamp'):
        return value
    return parser.parse(value)


# TODO: that can be done by available packages with more generic approach, for this case it's enough to have custom func
def convert_dict_to_mongo_query(filters: Dict, last_seen_datetime: datetime) -> Dict:
    """
    Easy converter from dictionary request parameters to MongoDB query
    :param filters: Filters from request, return empty if it's empty
    :param last_seen_datetime:
    :return: Dictionary in the form of mongodb query
    """
    if not filters and not last_seen_datetime:
        return filters
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
    return query


async def get_log(filters: Dict, limit: int, last_seen_datetime: datetime, db):
    """
    Returns list of logs that meets filters
    :param filters: Dictionary of query params
    :param limit: Limit of log results in one request
    :param last_seen_datetime: Direct filter on event_timestamp for pagination support
    :param db: db collection
    :return: list of logs that meets requirements
    """
    query = convert_dict_to_mongo_query(filters, last_seen_datetime)
    result = []
    async for doc in db.find(query, limit=limit):
        # TODO: there're nicer ways to skip _id field (in Pydantic model)
        doc.pop('_id')
        result.append(doc)
    return result
