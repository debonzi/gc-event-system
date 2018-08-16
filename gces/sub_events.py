import logging
from collections import namedtuple

from . subscriber import Subscriber
from .message import Message


logger = logging.getLogger(__name__)

RegistryEntry = namedtuple('RegistryEntry', ['function', 'type', 'ack_late'])

class EventSubscriber(object):
    def __init__(self, topic_name, name, gcloud_project_id=None):
        self.gcloud_project_id = gcloud_project_id
        self.topic_name = topic_name
        self.name = name
        self._register = {}
        self._obj_desc = "{} {} ({})".format(
            self.__class__.__name__,
            name,
            topic_name
        )

        logger.info('{} Created.'.format(self._obj_desc))

    def start(self):
        self.subscriber = Subscriber(
            self.topic_name, self.name, self._callback, self.gcloud_project_id
        )
        logger.info('{} Started.'.format(self._obj_desc))


    def _callback(self, message):
        message = Message(message)
        reg = self._register.get(message.event)
        if reg:
            if not reg.ack_late:
                message.ack()

            if reg.type == 'function':
                reg.function(message.data)
            elif reg.type == 'task':
                reg.function.delay(message.data)
            logger.info('Event {} processed with "{}" callback.'.format(message.event, reg.function.__name__))
        else:
            logger.info('Event {} Ignored.'.format(message.event))
        message.ack()

    def register_fsub(self, event_name, function, ack_late=True):
        self._register[event_name] = RegistryEntry(
            function=function,
            ack_late=ack_late,
            type='function'
        )
        logger.info(
            '{}: Event listener function "{}" registered for {}.'.format(
                self._obj_desc,
                function.__name__,
                event_name
            )
        )

    def register_tsub(self, event_name, function, ack_late=True):
        self._register[event_name] = RegistryEntry(
            function=function,
            ack_late=ack_late,
            type='task'
        )
        logger.info(
            '{}: Event listener task "{}" registered for {}.'.format(
                self._obj_desc,
                function.__name__,
                event_name
            )
        )
