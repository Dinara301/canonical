import asyncio
import os
import subprocess

PORT = "27017"
os.environ["DATABASE_URL"] = f"mongodb://localhost:{PORT}"

import motor
import pytest
from starlette.testclient import TestClient
from pathlib import Path
from src.logging_server.database import get_db_session
from src.main import app

MONGO_TEST_PATH = "/tmp/date/db_test/"
Path(MONGO_TEST_PATH).mkdir(parents=True, exist_ok=True)
mongod = subprocess.Popen(['mongod', '--dbpath', MONGO_TEST_PATH, '--port', PORT])
db_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("DATABASE_URL"))
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
    mongod.terminate()
