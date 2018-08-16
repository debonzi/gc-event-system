import logging

from .publisher import Publisher
from .message import Event


logger = logging.getLogger(__name__)


class EventPublisher(object):
    def __init__(self, topic_name, gcloud_project_id=None):
        self.publisher = Publisher(topic_name, gcloud_project_id)
        self._obj_desc = '{} "{}"'.format(
            self.__class__.__name__,
            topic_name
        )
        logger.info('{} Created'.format(self._obj_desc))

    def notify(self, event_name, data):
        event = Event(event_name, data)
        pub = self.publisher.pub(event.body)
        logger.info(
            '{}: Event {} notification published.'.format(
                self._obj_desc, event_name
            )
        )
        return pub
