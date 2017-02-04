import asyncio
import json
import logging
import urllib
import uuid
import websockets
from django.contrib.auth import get_user_model

from django.template.defaultfilters import date as dj_date

from apps.chat import channels, models, router

logger = logging.getLogger('apps.chat')
ws_connections = {}


@asyncio.coroutine
def target_message(conn, payload):
    """
    Distibuted payload (message) to one connection
    :param conn: connection
    :param payload: payload(json dumpable)
    :return:
    """
    try:
        yield from conn.send(json.dumps(payload))
    except Exception as e:
        logger.debug('could not send', e)


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
    # TODO: handle no user found exception
    while True:
        packet = yield from stream.get()
        user_set = get_user_model().objects.filter(first_name=packet['username'].split(' ')[0],
                                                   last_name=packet['username'].split(' ')[1])
        if len(user_set) > 0:
            user = user_set[0]
        else:
            user = None
        # Save the message
        msg = models.Message.objects.create(
            dialog=models.Dialog.objects.all()[0],
            sender=user,
            text=packet['message']
        )

        packet['created'] = dj_date(msg.created, "DATETIME_FORMAT")

        # Create new message
        yield from fanout_message(ws_connections.keys(), packet)

#TODO: use for online/offline status
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
    print(websocket,path)
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
                yield from router.MessageRouter(data)() #TODO: WTF
            except Exception as e:
                logger.error('could not route msg', e)

    except websockets.exceptions.InvalidState:  # User disconnected
        # TODO: alert the other user that this user went offline
        pass
    finally:
        del ws_connections[websocket]
