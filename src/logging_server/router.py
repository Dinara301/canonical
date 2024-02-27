from datetime import datetime
from typing import List

from fastapi import APIRouter, Response, status, Depends, Request

from src.logging_server.models import LogItem
from src.logging_server.database import add_log, get_db_session, get_log
from urllib.parse import parse_qs

router = APIRouter()


# TODO: see Readme for better design
# TODO: add versioning
# TODO: logging of the service itself is needed for debugging
# TODO: error specific handlers for better client experience and easier debugging
@router.put("/log/")
async def create_log(item: LogItem, db=Depends(get_db_session)):
    """
    Async request handler for adding log
    :param item: Request body in Pydantic type LogItem
    :param db: mongodb collection dependency
    :return: basic Response
    """
    await add_log(item, db)
    return Response(status_code=status.HTTP_200_OK)


# TODO: only basic filtering is implemented on equality for string types.
#  Range filtering, other more complicated filters can be added, ordering, prefix search etc

# TODO: add fields validation

# TODO: For pagination last datetime from the previous query is used, it can lead to duplicates
# last_seen_datetime parameter is added directly
@router.get("/log/")
async def fetch_logs(request: Request, limit: int = 10, last_seen_datetime: datetime = None, db=Depends(get_db_session),
                     response_model=List[LogItem]):
    """
    Request handler fore retrieving logs that meet filters requirements
    :param request: request with all query parameters
    :param limit: limit for the number of logs returned, default 10
    :param last_seen_datetime: datetime of the last retrieved log, for pagination
    :param db: mongodb collection
    :param response_model: model that is expected in response
    :return:
    """
    query_params = parse_qs(request.url.query)
    print(limit)
    print(last_seen_datetime)
    query_params.pop('limit', None)
    query_params.pop('last_seen_datetime', None)
    return await get_log(query_params, limit, last_seen_datetime, db)
