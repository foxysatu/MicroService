import os
import requests
import pytest
import asyncio
from main import root, get_list
from fastapi import Query

# Тестирование функции root на корректность возвращаемых данных
@pytest.mark.asyncio
async def test_root_get():
    # Вызываем функцию root
    res = await root()
    # Проверяем, что результат является списком
    assert isinstance(res, list)
    # Проверяем, что первый элемент списка является словарем
    assert isinstance(res[0], dict)
    # Проверяем, что в первом элементе словаря присутствуют ключи 'url' и 'id'
    assert 'url' in res[0].keys()
    assert 'id' in res[0].keys()


# Тестирование функции get_list с использованием параметра запроса (query)
@pytest.mark.asyncio
async def test_get_list_with_query():
    # Предполагаем, что у нас есть список ID для тестирования
    test_ids = [1, 2, 3]
    # Вызываем функцию get_list с передачей списка ID через параметр запроса (query)
    res = await get_list(q=test_ids)
    # Проверяем, что результат является списком
    assert isinstance(res, list)
    # Проверяем, что количество подсписков в результате соответствует количеству переданных ID
    assert len(res) == len(test_ids)
    # Проверяем каждый элемент в каждом подсписке: должен быть словарь с ключами 'url' и 'id'
    for sublist in res:
        assert isinstance(sublist, list)
        for item in sublist:
            assert isinstance(item, dict)
            assert 'url' in item
            assert 'id' in item
