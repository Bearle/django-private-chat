import asyncio

new_messages = asyncio.Queue()
users_changed = asyncio.Queue()
online = asyncio.Queue()
offline = asyncio.Queue()
check_online = asyncio.Queue()
is_typing = asyncio.Queue()
read_unread = asyncio.Queue()
