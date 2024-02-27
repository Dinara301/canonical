import asyncio

import motor
import pytest
from starlette.testclient import TestClient

from src.logging_server.database import get_db_session
from src.main import app

# TODO mongo for tests should use tmp directory
MONGO_DETAILS = "mongodb://localhost:27017/test"
db_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db_client.get_io_loop = asyncio.get_event_loop
database = db_client.test_log
test_collection = database.get_collection("test")


def get_testing_db():
    return test_collection


@pytest.fixture(scope="module")
def test_setup():
    app.dependency_overrides[get_db_session] = get_testing_db
    client = TestClient(app)
    yield client, test_collection
    # remove testing db and close connection once testing is done
    db_client.drop_database("test_log")
    db_client.close()
