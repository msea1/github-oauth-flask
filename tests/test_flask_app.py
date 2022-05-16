from unittest import TestCase

from src.app import create_app


class AppFactoryTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_app()
