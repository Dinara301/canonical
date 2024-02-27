import pytest

def fill_in_test_collection(test_app):
    events = ["create", "create", "delete", "update"]
    events_timestamp = ["2024-02-22T08:47:36.869Z", "2023-02-22T08:47:36.869Z", "2024-01-22T08:47:36.869Z",
                        "2024-02-22T08:47:36.869Z"]
    service_ids = ["098c0a6d-c5b6-410d-b1ae-2942cc581dda", "93b05549-4a11-42d0-b11e-4adc70f308bc",
                   "b354036a-ca60-483f-9e57-1da5707b56e8", "351e321a-cd75-4f58-a0a5-3f7a92288bdf"]
    for i, id in enumerate(service_ids):
        test_app.put("/log", json={"service_id": service_ids[i],
                                   "customer_id": service_ids[i],
                                   "event_type": events[i],
                                   "event_timestamp": events_timestamp[i],
                                   "description": "test"})

@pytest.fixture()
def clean_collection(test_setup):
    """Clean test collection after each test"""
    yield
    test_app, test_collection = test_setup
    test_collection.delete_many({})

@pytest.mark.asyncio
async def test_log_fetch(test_setup, clean_collection):
    test_app, test_collection = test_setup
    fill_in_test_collection(test_app)
    response = test_app.get("/log/?limit=20&event_timestamp=2024-02-22T08:47:36.869Z")
    assert response.status_code == 200
