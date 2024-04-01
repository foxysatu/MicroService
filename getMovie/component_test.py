import os
import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data[0]  # Проверяем, что ответ содержит ключ 'id'


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        data = response.json()
        if data:
            assert isinstance(data, list)  # Проверяем, что ответ является списком
            assert isinstance(data[0], dict)  # Проверяем, что элементы списка являются словарями
        else:
            assert data == []  # Проверяем, что пустой список возвращается, если нет данных в базе