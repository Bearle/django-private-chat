import asyncio
import websockets
from django.conf import settings
from django.core.management.base import BaseCommand
from django_private_chat import channels, handlers


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
        asyncio.async(handlers.gone_online(channels.online))
        asyncio.async(handlers.check_online(channels.check_online))
        asyncio.async(handlers.gone_offline(channels.offline))
        asyncio.async(handlers.is_typing_handler(channels.is_typing))
        loop = asyncio.get_event_loop()
        loop.run_forever()
