import asyncio
import websockets

from django.conf import settings
from django.core.management.base import BaseCommand
from chat import channels, handlers


class Command(BaseCommand):
    help = 'Starts message center chat engine'

    def handle(self, *args, **options):
        asyncio.async(
            websockets.serve(
                handlers.main_handler,
                settings.CHAT_WS_SERVER_HOST,
                settings.CHAT_WS_SERVER_PORT
            )
        )

        asyncio.async(handlers.new_messages_handler(channels.new_messages))
        asyncio.async(handlers.users_changed_handler(channels.users_changed))
        loop = asyncio.get_event_loop()
        loop.run_forever()
