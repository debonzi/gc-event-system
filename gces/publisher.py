import logging
from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

from .tools import get_project_id


logger = logging.getLogger(__name__)


class Publisher(object):
    def __init__(self, topic_name, gcloud_project_id=None):
        self.publisher = pubsub_v1.PublisherClient()
        self.gcloud_project_id = gcloud_project_id or get_project_id()
        self.topic_name = topic_name
        self.topic_path = self.publisher.topic_path(  #pylint: disable=E1101
            self.gcloud_project_id, self.topic_name)
        self._ensure_topic_exists()

    def _ensure_topic_exists(self):
        """Create a new Pub/Sub topic."""
        publisher = pubsub_v1.PublisherClient()
        try:
            topic = publisher.create_topic(self.topic_path)  #pylint: disable=E1101
        except AlreadyExists:
            topic = None

        log_msg = 'Topic "{}" Created.' if topic else 'Topic "{}" already exists.'
        log_msg = log_msg.format(self.topic_path)
        logger.info(log_msg)

    def pub(self, message):
        return self.publisher.publish(
            self.topic_path, data=message
        )
