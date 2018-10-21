import asyncio
import ssl
import websockets
from django.conf import settings
from django.core.management.base import BaseCommand
from django_private_chat import channels, handlers
from django_private_chat.utils import logger
import sys


class Command(BaseCommand):
    help = 'Starts message center chat engine'

    def add_arguments(self, parser):
        parser.add_argument('ssl_cert', nargs='?', type=str)

    def handle(self, *args, **options):
        if options['ssl_cert'] is not None:
            if sys.version_info >= (3, 6):
                protocol = ssl.PROTOCOL_TLS_SERVER
            elif sys.version_info >= (3, 4):
                protocol = ssl.PROTOCOL_TLSv1
            else:
                v = str(sys.version_info.major) + '.' + str(sys.version_info.minor)
                version_s = 'Version %s is not supported for wss!' % v
                raise Exception(version_s)
            ssl_context = ssl.SSLContext(protocol)
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
