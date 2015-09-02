import asyncio
import json
import logging
import urllib
import uuid
import websockets

from django.template.defaultfilters import date as dj_date

from chat import channels, models, router


logger = logging.getLogger('apps.chat')
ws_connections = {}


@asyncio.coroutine
def fanout_message(connections, payload):
    """distributes payload (message) to all connected ws clients
    """
    for conn in connections:
        try:
            yield from conn.send(json.dumps(payload))
        except Exception as e:
            logger.debug('could not send', e)


@asyncio.coroutine
def new_messages_handler(stream):
    while True:
        packet = yield from stream.get()

        # Save the message
        msg = models.ChatMessage.objects.create(
            username=packet['username'],
            message=packet['message']
        )

        packet['created'] = dj_date(msg.created, "DATETIME_FORMAT")

        # Create new message
        yield from fanout_message(ws_connections.keys(), packet)


@asyncio.coroutine
def users_changed_handler(stream):
    while True:
        yield from stream.get()

        # Get list list of current active users
        users = [
            {'username': username, 'uuid': uuid_str}
            for username, uuid_str in ws_connections.values()
        ]

        # Make packet with list of new users (sorted by username)
        packet = {
            'type': 'users-changed',
            'value': sorted(users, key=lambda i: i['username'])
        }
        logger.debug(packet)
        yield from fanout_message(ws_connections.keys(), packet)


@asyncio.coroutine
def main_handler(websocket, path):
    username = urllib.parse.unquote(path[1:])
    ws_connections[websocket] = (username, str(uuid.uuid4()))

    try:
        while websocket.open:
            data = yield from websocket.recv()
            if not data: continue
            logger.debug(data)
            try:
                yield from router.MessageRouter(data)()
            except Exception as e:
                logger.debug('could not route msg', e)

    except websockets.exceptions.InvalidState:  # User disconnected
        pass
    finally:
        del ws_connections[websocket]
