import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel('INFO')


import json, time
from gces import tools
from gces import (
    EventSubscriber
)

from celery_app import example_run_subscriber_task

def example_run_subscriber_function(data):
    pass

TOPIC_NAME = 'gces'
SUBSCRIBER_NAME = 'gces_example'


es = EventSubscriber(TOPIC_NAME, SUBSCRIBER_NAME)
es.register_fsub('EXAMPLE_RUN_FUNCTION_PROCCESS', example_run_subscriber_function)
es.register_tsub('EXAMPLE_RUN_TASK_PROCCESS', example_run_subscriber_task)

es.start()

if __name__ == '__main__':
    try:
        while True:
            time.sleep(200)
    except KeyboardInterrupt:
        print('Bye!!!!')
