import asyncio


new_messages = asyncio.Queue()
users_changed = asyncio.Queue()
start_dialog = asyncio.Queue()