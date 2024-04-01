import pytest
from main import app
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert 'id' in response.json()[0]  # Проверяем, что ответ содержит ключ 'id'

# @pytest.mark.asyncio
# async def test_list():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/list/")
#         assert response.status_code == 200
#         assert isinstance(response.json(), list)  # Проверяем, что ответ является списком

@pytest.mark.asyncio
async def test_list_with_query():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/list/?q=1")
        assert response.status_code == 200
        assert isinstance(response.json(), list)  # Проверяем, что ответ является списком
