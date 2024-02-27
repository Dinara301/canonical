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
@router.get("/log/")
async def fetch_logs(request: Request, limit: int = 10, db=Depends(get_db_session)):
    print(request.query_params)
    print(parse_qs(request.url.query))
    print(limit)
    query_params = parse_qs(request.url.query)
    query_params.pop('limit')
    await get_log(query_params, limit, db)
    return Response(status_code=status.HTTP_200_OK)
