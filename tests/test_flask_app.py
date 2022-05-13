from unittest import TestCase

from src.app import app


class AppFactoryTest(TestCase):

    def test_basic_index(self):
        idx_resp = app.view_functions['index']()
        self.assertEqual('Found default', idx_resp)
