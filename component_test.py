import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime

base_url = 'http://localhost:80/'


def test_root_get():
    res = requests.get(base_url).json()
    assert ('Title' in res.keys())
    assert ('Year' in res.keys())
    assert (type(res['Year']) == str)


def test_list_get():
    res = requests.get(base_url + 'list/?t=275')
    print(res)
    return
    res = res[0]
    assert (res['Title'] == 275)
    assert (res['Year'] == 2011)


test_list_get()