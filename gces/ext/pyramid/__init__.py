from gces import EventPublisher as _EventPublisher


class EventPublisher(object):
    def setup(self, topic_name):
        self._pub = _EventPublisher(topic_name)

    def __getattr__(self, item):
        return getattr(self._pub, item)


event_publisher = EventPublisher()

def includeme(config):  # pragma: no cover
    settings = config.registry.settings
    event_publisher.setup(settings['gces.event_publisher.topic_name'])
