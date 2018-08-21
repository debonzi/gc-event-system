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


event_publisher = EventPublisher()

def to_bool(value):
    if isinstance(value, bool):
        return value
    return value in ['true', 'True', 'TRUE']

def includeme(config):  # pragma: no cover
    settings = config.registry.settings
    event_publisher.setup(
        settings['gces.event_publisher.topic_name'],
        to_bool(settings['gces.ext.pyramid.event_publisher.disabled'])
    )
