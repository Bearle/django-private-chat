import asyncio
# import json
from unittest.mock import Mock
import pytest
# from django.contrib.auth import get_user_model
# import websockets

from django_private_chat import handlers
from django_private_chat import channels


@pytest.mark.asyncio
@asyncio.coroutine
def test_is_typing_handler():
    data = {
        'type': 'is_typing',
        'session_key': 1,
        'username': 'user',
        'typing': True
    }

    yield from channels.is_typing.put(data)
    assert channels.is_typing.empty() is False

    # mock is_typing_handler
    @asyncio.coroutine
    def mock_is_typing_handler_coro(stream):
        res = yield from stream.get()
        return res

    mocked = Mock(handlers)
    mocked.is_typing_handler = mock_is_typing_handler_coro

    result = yield from mocked.is_typing_handler(channels.is_typing)
    assert result == data


@pytest.mark.asyncio
@asyncio.coroutine
def test_new_message_handler():
    data = {
        'type': 'new_message'
    }
    yield from channels.new_messages.put(data)

    assert channels.new_messages.empty() is False

    @asyncio.coroutine
    def mock_new_messages_handler_coro(stream):
        res = yield from stream.get()
        return res

    mocked = Mock(handlers)
    mocked.new_messages_handler = mock_new_messages_handler_coro

    result = yield from mocked.new_messages_handler(channels.new_messages)

    assert result == data


@pytest.mark.asyncio
@asyncio.coroutine
def test_users_changed_handler():
    data = {
        'type': 'users_changed'
    }
    yield from channels.users_changed.put(data)

    assert channels.users_changed.empty() is False

    @asyncio.coroutine
    def mock_users_changed_handler_coro(stream):
        res = yield from stream.get()
        return res

    mocked = Mock(handlers)
    mocked.users_changed_handler = mock_users_changed_handler_coro

    result = yield from mocked.users_changed_handler(channels.users_changed)

    assert result == data


@pytest.mark.asyncio
@asyncio.coroutine
def test_gone_online_handler():
    data = {
        'type': 'gone_online'
    }
    yield from channels.online.put(data)

    assert channels.online.empty() is False

    @asyncio.coroutine
    def mock_gone_online_handler_coro(stream):
        res = yield from stream.get()
        return res

    mocked = Mock(handlers)
    mocked.gone_online_handler = mock_gone_online_handler_coro

    result = yield from mocked.gone_online_handler(channels.online)

    assert result == data


@pytest.mark.asyncio
@asyncio.coroutine
def test_gone_offline_handler():
    data = {
        'type': 'gone_offline'
    }
    yield from channels.offline.put(data)

    assert channels.offline.empty() is False

    @asyncio.coroutine
    def mock_gone_offline_handler_coro(stream):
        res = yield from stream.get()
        return res

    mocked = Mock(handlers)
    mocked.gone_offline_handler = mock_gone_offline_handler_coro

    result = yield from mocked.gone_offline_handler(channels.offline)

    assert result == data


@pytest.mark.asyncio
@asyncio.coroutine
def test_check_online_handler():
    data = {
        'type': 'check_online'
    }
    yield from channels.check_online.put(data)

    assert channels.check_online.empty() is False

    @asyncio.coroutine
    def mock_check_online_handler_coro(stream):
        res = yield from stream.get()
        return res

    mocked = Mock(handlers)
    mocked.check_online_handler = mock_check_online_handler_coro

    result = yield from mocked.check_online_handler(channels.check_online)

    assert result == data
