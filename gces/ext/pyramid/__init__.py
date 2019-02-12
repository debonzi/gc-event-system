from gces import EventPublisher as _EventPublisher


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
    if not topic_name:
        error_msg = 'Add a name to "gces.event_publisher.topic_name" in your configuration environment'
        raise NamelessTopicError(error_msg)
    event_publisher.setup(
        topic_name,
        to_bool(settings['gces.ext.pyramid.event_publisher.disabled'])
    )
