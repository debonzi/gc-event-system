from unittest import mock
from gces import EventPublisher

@mock.patch('gces.pub_events.Publisher')
def test_event_publisher(publisher_mock):
    publisher_mock.pub = mock.MagicMock()
    ept = EventPublisher('gces')
    ept.notify('TEST_EVENT', {})
    assert ept.publisher.pub.called is True  # pylint: disable=E1101
