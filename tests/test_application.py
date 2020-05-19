import pycodestyle

from django.test import TestCase


class TestApplication(TestCase):

    def test_style(self):
        """
        Test PEP 8 style conventions

        E501 - Line too long (82 > 79 characters)
        W504 - Line break occurred after a binary operator
        """

        style = pycodestyle.StyleGuide(ignore=['E501', 'W504'])
        result = style.check_files(['config/', 'v1/'])
        self.assertEqual(result.total_errors, 0)
