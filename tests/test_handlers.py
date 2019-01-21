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
        'type': 'is_typing',
        'session_key': 1,
        'username': 'user',
        'typing': True
    }
    return data


@asyncio.coroutine
def mock_is_typing_handler_coro(stream):
    res = yield from stream.get()
    return res


@asyncio.coroutine
def mock_read_message_handler_coro(stream):
    res = yield from stream.get()
    return res


@asyncio.coroutine
def mock_new_messages_handler_coro(stream):
    res = yield from stream.get()
    return res


@asyncio.coroutine
def mock_gone_offline_handler_coro(stream):
    res = yield from stream.get()
    return res


@asyncio.coroutine
def mock_gone_online_handler_coro(stream):
    res = yield from stream.get()
    return res


@asyncio.coroutine
def mock_check_online_handler_coro(stream):
    res = yield from stream.get()
    return res


@asyncio.coroutine
def mock_users_changed_handler_coro(stream):
    res = yield from stream.get()
    return res


@pytest.mark.asyncio
@asyncio.coroutine
def test_is_typing_handler():
    data = get_typing_data()

    # put data in queue
    yield from channels.is_typing.put(data)
    assert channels.is_typing.empty() is False 

    # mock is_typing_handler
    mocked = Mock(handlers)
    mocked.is_typing_handler = mock_is_typing_handler_coro

    result = yield from mocked.is_typing_handler(channels.is_typing)
    assert result == data
    # assert mocked is called once with is_typing channels


@pytest.mark.asyncio
@asyncio.coroutine
def test_new_message_handler():
    yield from channels.new_messages.put(
        {
            'type': 'new_message'
        }
    )

    assert channels.new_messages.empty() == False 

    mocked = Mock(handlers)
    mocked.new_messages_handler = mock_new_messages_handler_coro

    result = yield from mocked.new_messages_handler(channels.new_messages)

    assert result is not None


@pytest.mark.asyncio
@asyncio.coroutine
def test_users_changed_handler():
    yield from channels.users_changed.put(
        {
            'type': 'users_changed'
        }
    )

    assert channels.users_changed.empty() is False

    mocked = Mock(handlers)
    mocked.users_changed_handler = mock_users_changed_handler_coro

    result = yield from mocked.users_changed_handler(channels.users_changed)

    assert result is not None
