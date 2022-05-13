from unittest import TestCase

from src.app import create_app


class AppFactoryTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_app()

    def test_basic_hello_world(self):
        hello_resp = self.app.view_functions['hello_world']()
        self.assertEqual('<p>Hello, World!</p>', hello_resp)

    def test_basic_index(self):
        idx_resp = self.app.view_functions['index']()
        self.assertEqual('Found default', idx_resp)
