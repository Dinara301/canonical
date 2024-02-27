import pytest


@pytest.fixture(autouse=True)
def clean_collection(test_setup):
    """Clean test collection after each test"""
    yield
    test_app, test_collection = test_setup
    test_collection.delete_many({})


@pytest.mark.asyncio
async def test_log_put(test_setup):
    service_id = "6b5c6aa9-afc4-4010-9d1c-7090dddcdeac"
    customer_id = "aa8aea04-f8b3-4d9b-9938-b2a0441caa1e"
    test_app, test_collection = test_setup
    response = test_app.put("/log/", json={"service_id": service_id,
                                           "customer_id": customer_id,
                                           "event_type": "create",
                                           "event_timestamp": "2024-02-22T08:47:36.869Z",
                                           "description": "test1",
                                           "extra_field1": "5",
                                           "extra_field2": "6"}
                            )
    assert response.status_code == 200
    log_added = await test_collection.find_one({"$and": [{"service_id": service_id},
                                                    {"customer_id": customer_id},
                                                    {"extra_field1": "5"}, {"extra_field2": "6"}]})
    assert log_added


@pytest.mark.asyncio
async def test_invalid_data(test_setup):
    """
    No customer_id provided, request fails with 422 return code
    """
    service_id = "6b5c6aa9-afc4-4010-9d1c-7090dddcdeac"
    test_app, test_collection = test_setup
    response = test_app.put("/log/", json={"service_id": service_id,
                                           "event_type": "create",
                                           "event_timestamp": "2024-02-22T08:47:36.869Z",
                                           "description": "test1"},
                            )
    assert response.status_code == 422
    assert await test_collection.find_one({"$and": [{"service_id": service_id}]}) is None
