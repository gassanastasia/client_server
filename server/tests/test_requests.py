import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.requests.schemas import RequestCreate

@pytest.mark.asyncio
async def test_create_request(test_client, db_session: AsyncSession):
    request_data = {
        "text": "Test request",
        "request_date": "2023-12-19",
        "request_time": "15:30:00",
        "click_count": 1
    }
    
    response = test_client.post("/requests", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["text"] == request_data["text"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_requests(test_client):
    response = test_client.get("/requests")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "items" in data
    assert "total" in data

@pytest.mark.asyncio
async def test_request_validation(test_client):
    invalid_data = {
        "text": "A" * 600,
        "request_date": "invalid",
        "request_time": "15:30",
        "click_count": 0
    }
    
    response = test_client.post("/requests", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY