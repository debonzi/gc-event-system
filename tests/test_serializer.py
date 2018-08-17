import datetime
import pytz
from gces.serializer import DateDateTimeDecoder, DateDateTimeEncoder
from gces.serializer import serialize, deserialize


def test_datetime_serializer():
    obj = {
        'name': 'foo',
        'type': 'bar',
        'date': datetime.datetime.now()
    }
    deserial = deserialize(serialize(obj))
    assert obj == deserial


def test_deep_datetime_serializer():
    obj = {
        'name': 'foo',
        'type': 'bar',
        'date': {
            'date': {
                'date': datetime.datetime.now()
            }
        }
    }
    deserial = deserialize(serialize(obj))
    assert obj == deserial


def test_tz_datetime_serializer():
    obj = {
        'name': 'foo',
        'type': 'bar',
        'date': datetime.datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    }
    deserial = deserialize(serialize(obj))
    assert obj == deserial

def test_date_serializer():
    obj = {
        'name': 'foo',
        'type': 'bar',
        'date': datetime.date.today()
    }
    deserial = deserialize(serialize(obj))
    assert obj == deserial


