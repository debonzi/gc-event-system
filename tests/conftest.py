import os
import pytest


@pytest.fixture
def pyramid_config():
    class Registry(object):
        def __init__(self):
            self.settings = {}

    class Config(object):
        def __init__(self):
            self.registry = Registry()

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/__tmp__/__no_file__"

    return Config()
