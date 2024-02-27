import pytest


@pytest.mark.asyncio
async def test_log_put(test_setup):
    test_app, test_collection = test_setup
    response = test_app.get("/log/?limit=20&prop1=50&prop2=str1&prop1=lll")
    assert response.status_code == 200
