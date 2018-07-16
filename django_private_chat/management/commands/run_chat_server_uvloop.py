import asyncio
import ssl
import websockets
import uvloop
from django.conf import settings
from django.core.management.base import BaseCommand
from django_private_chat import channels_uvloop as channels
from django_private_chat import handlers
from django_private_chat.utils import logger

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Command(BaseCommand):
    help = 'Starts message center chat engine with uvloop'

    def add_arguments(self, parser):
        parser.add_argument('ssl_cert', nargs='?', type=str)

    def handle(self, *args, **options):
        if options['ssl_cert'] is not None:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(options['ssl_cert'])
        else:
            ssl_context = None

        asyncio.async(
            websockets.serve(
                handlers.main_handler,
                settings.CHAT_WS_SERVER_HOST,
                settings.CHAT_WS_SERVER_PORT,
                ssl=ssl_context
            )
        )

        logger.info('Chat server started')

        asyncio.async(handlers.new_messages_handler(channels.new_messages))
        asyncio.async(handlers.users_changed_handler(channels.users_changed))
        asyncio.async(handlers.gone_online(channels.online))
        asyncio.async(handlers.check_online(channels.check_online))
        asyncio.async(handlers.gone_offline(channels.offline))
        asyncio.async(handlers.is_typing_handler(channels.is_typing))
        asyncio.async(handlers.read_message_handler(channels.read_unread))
        loop = asyncio.get_event_loop()
        loop.run_forever()
