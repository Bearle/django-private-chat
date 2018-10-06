===================
Starting the server
===================


Application provides two managements commands, ``run_chat_server`` and ``run_chat_server_uvloop``.

That means that asyncio server is started SEPARATELY from the main Django application.
You can also supply optional "path/to/cert.pem" to the command to use wss.

What management command do is they simply get the asyncio/uvloop event loop,
add handlers for different message types to it and run the loop forever.
