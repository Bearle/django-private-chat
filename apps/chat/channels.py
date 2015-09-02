import asyncio
import multiprocessing


new_messages = asyncio.Queue()
users_changed = asyncio.Queue()
