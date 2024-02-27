from datetime import datetime

from fastapi import APIRouter, Response, status

from src.logging_server.models import LogItem
from src.logging_server.database import add_log

router = APIRouter()


@router.put("/log/")
async def create_log(item: LogItem):
    await add_log(item.dict())
    return Response(status_code=status.HTTP_200_OK)