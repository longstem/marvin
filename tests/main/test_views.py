import unittest

from flask import url_for

import pytest


@pytest.mark.usefixtures('client_class')
class DontPanicTests(unittest.TestCase):

    def test_dont_panic(self):
        response = self.client.get(url_for('main.dont_panic'))
        self.assertEqual(response.status_code, 200)
