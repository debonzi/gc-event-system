import logging
from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

from .tools import get_project_id


logger = logging.getLogger(__name__)


class Subscriber(object):
    def __init__(self, topic_name, name, callback, gcloud_project_id=None):
        self.subscriber_name = "{}__{}".format(topic_name, name)
        self.gcloud_project_id = gcloud_project_id or get_project_id()
        self.callback = callback
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(  #pylint: disable=E1101
            self.gcloud_project_id, self.subscriber_name
        )
        self._ensure_subscription(topic_name)
        self.future = self.subscriber.subscribe(self.subscription_path, callback=callback)

    def _create_subscription(self, topic_name):
        topic_path = self.subscriber.topic_path(self.gcloud_project_id, topic_name)  #pylint: disable=E1101

        subscription = self.subscriber.create_subscription(  #pylint: disable=E1101
            self.subscription_path, topic_path)

        print('Subscription created: {}'.format(subscription))

    def _ensure_subscription(self, topic_name):
        try:
            self._create_subscription(topic_name)
        except AlreadyExists:
            pass
