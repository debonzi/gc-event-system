# -*- encoding: utf-8 -*-
import celery
from celery.utils.log import get_task_logger
from kombu import Exchange, Queue

from minicache import cache

from gces import EventPublisher


logger = get_task_logger(__name__)


GCES_PUBLISHER_QUEUE = '__gces__queue__.__dispatcher__'
GCES_PUBLISHER_NAME = '__gces_dispatch__'

class EventPublisherTask(object):
    def __init__(self, topic_name):
        self.topic_name = topic_name

    def notify(self, event_name, data):
        _event_publisher_task.delay(self.topic_name, event_name, data)



def _send_notification(topic_name, event_name, data):
    epub = cache.get(topic_name) or EventPublisher(topic_name)
    cache.update(topic_name, epub)
    return epub.notify(event_name, data)



@celery.shared_task(bind=True, name=GCES_PUBLISHER_NAME, queue=GCES_PUBLISHER_QUEUE, acks_late=True)
def _event_publisher_task(self, topic_name, event_name, data):
    try:
        return _send_notification(topic_name, event_name, data)
    except Exception as exc:
        cache.clear(topic_name)
        try:
            raise self.retry(exc)
        except celery.exceptions.MaxRetriesExceededError:
            # Send event to a dead letter queue.
            _event_publisher_task.apply_async(
                (topic_name, event_name, data),
                queue='{}.__deadletter__'.format(GCES_PUBLISHER_QUEUE)
            )


def _register_celery_3(celery_app, queue):
    if celery_app.conf.CELERY_QUEUES:
        celery_app.conf.CELERY_QUEUES.append(queue)
    else:
        celery_app.conf.CELERY_QUEUES = [queue]


def _register_celery_4(celery_app, queue):
    if celery_app.conf.task_queues:
        celery_app.conf.task_queues.append(queue)
    else:
        celery_app.conf.task_queues = [queue]


def register_publisher(celery_app):
    queue = Queue(
        GCES_PUBLISHER_QUEUE,
        Exchange(GCES_PUBLISHER_QUEUE),
        routing_key=GCES_PUBLISHER_QUEUE
    )
    if not hasattr(celery_app.conf, 'task_queues'):  # Celery 3
        _register_celery_3(celery_app=celery_app, queue=queue)
    else:                                            # Celery 4
        _register_celery_4(celery_app=celery_app, queue=queue)
