from fastapi import FastAPI

from src.logging_server import router

app = FastAPI()
app.include_router(router.router)
