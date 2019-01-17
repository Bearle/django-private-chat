import asyncio
import json
from unittest.mock import Mock
import pytest 
from django.contrib.auth import get_user_model
import websockets

from django_private_chat import handlers 
from django_private_chat import channels 


def get_typing_data():
    data = {
        'type':'is_typing',
        'session_key': 1,
        'username': 'user',
        'typing': True
    }
    return data

@asyncio.coroutine
def mock_is_typing_handler_coro(stream):
    res = yield from stream.get()
    return res

@pytest.mark.asyncio
@asyncio.coroutine
def test_is_typing_handler():
    data = get_typing_data()

    # put data in queue
    yield from channels.is_typing.put(data)
    assert channels.is_typing.empty() == False 

    # mock is_typing_handler 
    mocked = Mock(handlers)
    mocked.is_typing_handler = mock_is_typing_handler_coro

    result = yield from mocked.is_typing_handler(channels.is_typing)
    print('result', str(result))
    assert result == data
