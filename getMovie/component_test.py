import os
import requests
import pytest
from fastapi.testclient import TestClient
from main import app

# Инициализация клиента для тестирования FastAPI-приложения
client = TestClient(app)

# Базовый URL для тестирования
base_url = 'http://localhost:80/'


# Тестирование корневого эндпоинта приложения на корректность данных
def test_root_get():
    with TestClient(app) as client:
        # Отправляем GET-запрос на корневой эндпоинт
        response = client.get("/")
        # Проверяем, что статус код ответа - 200 (Успешный запрос)
        assert response.status_code == 200
        # Проверяем, что ответ является списком и содержит необходимые ключи 'url' и 'id' в первом элементе списка
        data = response.json()
        assert 'url' in data[0]
        assert 'id' in data[0]


# Тестирование корневого эндпоинта приложения на наличие списка и его непустоту
def test_root_endpoint():
    # Отправляем GET-запрос на корневой эндпоинт
    response = client.get("/")
    # Проверяем, что статус код ответа - 200 (Успешный запрос)
    assert response.status_code == 200
    # Проверяем, что ответ является списком
    assert isinstance(response.json(), list)
    # Проверяем, что список не пустой
    assert len(response.json()) > 0
    # Дополнительные проверки для каждого элемента в списке могут быть добавлены по необходимости


# Тестирование корневого эндпоинта приложения с учетом переменной limit, которая определяет количество отображаемых данных
@pytest.mark.parametrize("limit", [1, 5, 10])
def test_root_endpoint_with_cat_api_limit(limit):
    # Отправляем GET-запрос на корневой эндпоинт с указанием переменной limit
    response = client.get(f"/?limit={limit}")
    # Проверяем, что статус код ответа - 200 (Успешный запрос)
    assert response.status_code == 200
    # Проверяем, что ответ является списком
    assert isinstance(response.json(), list)
    # Проверяем, что количество элементов в списке не превышает значение переменной limit
    assert len(response.json()) <= limit
    # Проверяем, что каждый элемент в списке содержит ключ "url"
    for item in response.json():
        assert "url" in item  # Замените "url" на соответствующий ключ в вашем JSON-ответе
