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
    """Saves a new chat message to db and distributes msg to connected users
    """
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
    """Sends connected client list of currently active users in the chatroom
    """
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
    """An Asyncio Task is created for every new websocket client connection
    that is established. This coroutine listens to messages from the connected
    client and routes the message to the proper queue.

    This coroutine can be thought of as a producer.
    """

    # Get users name from the path
    username = urllib.parse.unquote(path[1:])

    # Persist users connection, associate user w/a unique ID
    ws_connections[websocket] = (username, str(uuid.uuid4()))

    # While the websocket is open, listen for incoming messages/events
    # if unable to listening for messages/events, then disconnect the client
    try:
        while websocket.open:
            data = yield from websocket.recv()
            if not data: continue
            logger.debug(data)
            try:
                yield from router.MessageRouter(data)()
            except Exception as e:
                logger.error('could not route msg', e)

    except websockets.exceptions.InvalidState:  # User disconnected
        pass
    finally:
        del ws_connections[websocket]
