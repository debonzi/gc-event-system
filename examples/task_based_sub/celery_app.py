from celery import Celery
from celery.signals import worker_init

app = Celery()
app.config_from_object('celery_conf')

@app.task(bind=True, queue='gces_task_example')
def example_run_subscriber_task(self, data):
    pass

