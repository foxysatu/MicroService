import pytest
from uuid import uuid4
from time import sleep
from datetime import datetime
from main import root, get_list
import json
import asyncio
from fastapi import Query


def test_root_get():
    res = asyncio.run(root())
    assert 'Title' in res.keys()
    assert 'Year' in res.keys()
    assert (type(res['Title']) == str)


def test_list_get():
    res = asyncio.run(get_list(q=[275]))
    res = res[0]
    assert (res['Title'] == '275')
    assert (res['Year'] == '2011')


