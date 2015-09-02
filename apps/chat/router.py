import asyncio
import json
import logging

from chat import channels

logger = logging.getLogger('apps.chat')


class MessageRouter(object):
    MESSAGE_QUEUES = {
        'new-message': channels.new_messages,
        'new-user': channels.users_changed,
        # 'is-typing': new_users_sender,
    }

    def __init__(self, data):
        try:
            self.packet = json.loads(data)
        except Exception as e:
            logger.debug('could not load json: {}'.format(str(e)))

    def get_packet_type(self):
        return self.packet['type']

    @asyncio.coroutine
    def __call__(self):
        logger.debug('routing message: {}'.format(self.packet))
        send_queue = self.get_send_queue()
        yield from send_queue.put(self.packet)

    def get_send_queue(self):
        return self.MESSAGE_QUEUES[self.get_packet_type()]
