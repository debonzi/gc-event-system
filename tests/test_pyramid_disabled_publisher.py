import pytest
from google.auth.exceptions import DefaultCredentialsError

from gces.ext.pyramid import DisabledPublisher, includeme, to_bool


def test_to_bool():
    assert to_bool('true') is True
    assert to_bool('True') is True
    assert to_bool('TRUE') is True
    assert to_bool('false') is False
    assert to_bool('False') is False
    assert to_bool('FALSE') is False
    assert to_bool('Anything') is False


def test_disabled_publisher():
    event_publisher = DisabledPublisher('topic_name')
    assert isinstance(event_publisher.notify, DisabledPublisher)
    assert event_publisher.notify('event_name', {1: 2}) is None
    assert event_publisher.any_method('any_args1', 2, {1: 2}, kwarg=123) is None
    assert event_publisher.any_method.any_method_method() is None


def test_pyramid_disabled_event_publisher(pyramid_config):
    pyramid_config.registry.settings = {
        'gces.event_publisher.topic_name': 'tracking.events',
        'gces.ext.pyramid.event_publisher.disabled': True
    }

    includeme(pyramid_config)
    from gces.ext.pyramid import event_publisher
    assert isinstance(event_publisher._pub, DisabledPublisher)


def test_pyramid_exception_when_fallback_disabled(pyramid_config):
    pyramid_config.registry.settings = {
        'gces.event_publisher.topic_name': 'tracking.events',
        'gces.ext.pyramid.event_publisher.disabled': False
    }

    with pytest.raises(DefaultCredentialsError):
        includeme(pyramid_config)


def test_pyramid_publisher_disabled_when_fallback_enabled(pyramid_config):
    pyramid_config.registry.settings = {
        'gces.event_publisher.topic_name': 'tracking.events',
        'gces.ext.pyramid.event_publisher.disabled': False,
        'gces.ext.pyramid.event_publisher.fallback_to_disabled': True
    }

    includeme(pyramid_config)
    from gces.ext.pyramid import event_publisher
    assert isinstance(event_publisher._pub, DisabledPublisher)
