[![Build Status](https://travis-ci.org/debonzi/gc-event-system.svg?branch=master)](https://travis-ci.org/debonzi/gc-event-system)
[![PyPI](https://img.shields.io/pypi/v/gces.svg)](https://github.com/debonzi/gc-event-system)
[![PyPI](https://img.shields.io/pypi/pyversions/gces.svg)](https://github.com/debonzi/gc-event-system)
[![Coverage Status](https://coveralls.io/repos/github/debonzi/gc-event-system/badge.svg)](https://coveralls.io/github/debonzi/gc-event-system)

# GCES - Google Cloud Event System

## Goals
This project aims make it easier to have a global Event Publisher/Event Subscriber system to be used accross services.

## Architecture
![Architecture](docs/overview.svg)

## Quick Event Notification Example
```python
from gces import EventPublisher

ept = EventPublisher('gces')
ept.notify('SIGNUP_EVENT', {'user_id': 1234})
ept.notify('LOGIN_EVENT', {'user_id': 4321})
```

## Quick Event Subscription Example
```python
import time
from gces import (
    EventSubscriber
)

def example_run_subscriber_function(data):
    print("Data Received: {}".format(data))


TOPIC_NAME = 'gces'
SUBSCRIBER_NAME = 'gces_example'


es = EventSubscriber(TOPIC_NAME, SUBSCRIBER_NAME)
es.register_fsub('EXAMPLE_RUN_FUNCTION_PROCCESS' example_run_subscriber_function)
es.start()

if __name__ == '__main__':
    try:
        while True:
            time.sleep(200)
    except KeyboardInterrupt:
        print('Bye!!!!')
```

## Google Cloud Credentials
 * Create  Credentials at [Google](https://console.cloud.google.com/apis/credentials/serviceaccountkey)
 * export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/<credentials_file>.json
