import json
import tempfile
from unittest import TestCase

import pytest

from src.app import create_app


class AppFactoryTest(TestCase):
    @staticmethod
    def get_app():
        with tempfile.NamedTemporaryFile() as conf:
            # with open(conf.name, 'w') as conf_val:
            #     json.dump({'DEBUG': True, 'TESTING': True}, conf_val)
            app = create_app(conf.name)
            return app

    def test_basic_hello_world(self):
        basic_app = self.get_app()
        hello_resp = basic_app.view_functions['hello_world']()
        self.assertEqual('<p>Hello, World!</p>', hello_resp)
