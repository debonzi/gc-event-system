# -*- coding: utf-8 -*-
from kombu import Exchange
from kombu import Queue

BROKER_URL = 'redis://localhost:6379/0'
CELERYD_CONCURRENCY = 1

CELERY_QUEUES = [
    Queue('gces_task_example', Exchange('gces_task_example'), routing_key='gces_task_example')
]
