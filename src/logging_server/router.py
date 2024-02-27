from fastapi import APIRouter, Response, status, Depends, Request

from src.logging_server.models import LogItem
from src.logging_server.database import add_log, get_db_session
from urllib.parse import parse_qs

router = APIRouter()


@router.put("/log/")
async def create_log(item: LogItem, db=Depends(get_db_session)):
    await add_log(item, db)
    return Response(status_code=status.HTTP_200_OK)


@router.get("/log/")
async def fetch_logs(request: Request, limit: int = 10):
    # Parse request params that can be duplicated into dict to be used in db query
    q_params = parse_qs(request.url.query, keep_blank_values=True)
    d = dict((k, v if len(v) > 1 else v[0])
             for k, v in q_params.items())
    print(request.query_params)
    print(d)
    print(limit)
    return Response(status_code=status.HTTP_200_OK)
