import datetime
import pytz

from gces.serializer import serialize
from gces.message import Message, Event

DATE = datetime.date.today()
DATETIME = datetime.datetime.now()
DATETIME_TZ = datetime.datetime.now(tz=pytz.timezone('America/Sao_Paulo'))

DATA = {
    'name': 'foo',
    'type': 'bar',
    'datetime': DATETIME,
    'date': DATE
}


class GcMessageMock(object):
    def __init__(self, data=None):
        self.data = serialize(
            {
                'event': 'DUMMY_EVENT',
                'data': {
                    'name': 'foo',
                    'type': 'bar',
                    'datetime': DATETIME,
                    'date': DATE
                }
            }
        ) if not data else data

    @property
    def message_id(self):
        return 1234

    def ack(self):
        return True


def test_message():
    gc_message = GcMessageMock()
    message = Message(gc_message)
    assert message.id == 1234
    assert message.event == 'DUMMY_EVENT'
    assert message.data == DATA


def test_event():
    event = Event('DUMMY_EVENT', DATA)
    assert event.body.decode('utf-8') == serialize(
        {
            'event': 'DUMMY_EVENT',
            'data': DATA
        }
    )


def test_event_to_message():
    event = Event('DUMMY_EVENT', DATA)
    message = Message(GcMessageMock(event.body.decode('utf-8')))
    assert message.id == 1234
    assert message.event == 'DUMMY_EVENT'
    assert message.data == DATA
