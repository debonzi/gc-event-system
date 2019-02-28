import logging

from google.auth.exceptions import DefaultCredentialsError
from gces import EventPublisher as _EventPublisher


logger = logging.getLogger(__name__)


class DisabledPublisher(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        pass

    def __getattr__(self, item):
        return DisabledPublisher()


class EventPublisher(object):
    def setup(self, topic_name, disabled=False):
        self._pub = _EventPublisher(topic_name) if not disabled else DisabledPublisher()


    def __getattr__(self, item):
        return getattr(self._pub, item)

class NamelessTopicError(Exception):
    """Raised when configuration topic name is None"""

event_publisher = EventPublisher()

def to_bool(value):
    if isinstance(value, bool):
        return value
    return value in ['true', 'True', 'TRUE']

def includeme(config):  # pragma: no cover
    settings = config.registry.settings
    # Prevents the creation of a topic with name 'None'
    topic_name = settings['gces.event_publisher.topic_name']
    fallback = to_bool(settings.get('gces.ext.pyramid.event_publisher.fallback_to_disabled') or False)
    if not topic_name:
        error_msg = 'Add a name to "gces.event_publisher.topic_name" in your configuration environment'
        raise NamelessTopicError(error_msg)
    try:
        event_publisher.setup(
            topic_name,
            to_bool(settings['gces.ext.pyramid.event_publisher.disabled'])
        )
    except DefaultCredentialsError as exc:
        if fallback:
            event_publisher.setup(
                topic_name,
                disabled=True
            )
            logger.error('No Google Credentials envvar Found. Using DisabledPublisher for topic "%s"', topic_name)
        else:
            raise exc
