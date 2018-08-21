import pytest


@pytest.fixture
def pyramid_config():
    class Registry(object):
        def __init__(self):
            self.settings = {}

    class Config(object):
        def __init__(self):
            self.registry = Registry()
    
    return Config()
