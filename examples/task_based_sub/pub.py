from gces import EventPublisher


ept = EventPublisher('gces')
ept.notify('EXAMPLE_RUN_FUNCTION_PROCCESS', {})
ept.notify('EXAMPLE_RUN_TASK_PROCCESS', {})
ept.notify('EXAMPLE_RUN_DISCARD', {})
