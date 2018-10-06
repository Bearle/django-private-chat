========
Messages
========


Application provides the following message channels:

.. code-block:: python

    'new-message',
    'new-user',
    'online',
    'offline',
    'check-online',
    'is-typing',
    'read_message'


which are pretty self-explanatory.

Here is detailed explanation of what each channel does and data types:

``new-message``
    Example from js:

    .. code-block:: javascript

        {
            type: 'new-message',
            session_key: '{{ request.session.session_key }}',
            username: opponent_username,
            message: message
        }

    In the handler, a new Message object is created and the received packet
    along with the additional parameters is sene to the other user's websocket (if present)

    .. code-block:: python

        packet['created'] = msg.get_formatted_create_datetime()
        packet['sender_name'] = msg.sender.username
        packet['message_id'] = msg.id



``new-user``
    Sends connected client list of currently active users.

    .. code-block:: python

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


``online``
    Informs the users when someone of other has gone online.

    {'type': 'gone-online', 'usernames': [user_owner.username]}


``offline``
    Distributes the users 'gone offline' status to everyone he has dialog with
    {'type': 'gone-offline', 'username': user_owner.username}


``check-online``
    Same as online, except that it is used to provide the user that
    has gone online with information about who of his dialogs' users is online.


``is-typing``
    Shows message to opponent if the user is typing a message

    {'type': 'opponent-typing', 'username': user_opponent}


``read_message``
    Send message to user if the opponent has read the message
    Also sets the message.read to `True`.

    {'type': 'opponent-read-message', 'username': user_opponent, 'message_id': message_id}

