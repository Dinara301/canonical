from datetime import datetime
from typing import List

from fastapi import APIRouter, Response, status, Depends, Request

from src.logging_server.models import LogItem
from src.logging_server.database import add_log, get_db_session, get_log
from urllib.parse import parse_qs

router = APIRouter()


@router.put("/log/")
async def create_log(item: LogItem, db=Depends(get_db_session)):
    await add_log(item, db)
    return Response(status_code=status.HTTP_200_OK)


# TODO: only basic filtering is implemented on equality for string types.
#  Range filtering, other more complicated filters can be added, ordering, prefix search etc

# TODO: add fields validation

# TODO: For pagination last datetime from the previous query is used, it can lead to duplicates
@router.get("/log/")
async def fetch_logs(request: Request, limit: int = 10, last_seen_datetime: datetime = None, db=Depends(get_db_session), response_model=List[LogItem]):
    query_params = parse_qs(request.url.query)
    print(limit)
    print(last_seen_datetime)
    query_params.pop('limit', None)
    query_params.pop('last_seen_datetime', None)
    response = await get_log(query_params, limit, last_seen_datetime, db)
    return response
