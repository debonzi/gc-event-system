from gces.ext.celery import EventPublisherTask

from celery_app import app

ept = EventPublisherTask('gces')
ept.notify('EXAMPLE_RUN_FUNCTION_PROCCESS', {})
ept.notify('EXAMPLE_RUN_TASK_PROCCESS', {})
ept.notify('EXAMPLE_RUN_DISCARD', {})
