========
Settings
========

You should specify settings in your settings.py like this::

    CHAT_WS_SERVER_HOST = 'localhost'
    CHAT_WS_SERVER_PORT = 5002
    CHAT_WS_SERVER_PROTOCOL = 'ws'
    DATETIME_FORMAT = "d.m.Y H:i:s"



Here's a list of available settings::

    CHAT_WS_SERVER_PROTOCOL - 'ws' or 'wss'
    CHAT_WS_SERVER_HOST - 'localhost' or ip or domain
    CHAT_WS_SERVER_PORT - websocket application port
    DATETIME_FORMAT - "d.m.Y H:i:s" - format for datetimes

