import unittest

from flask import url_for

import pytest


@pytest.mark.usefixtures('client_class')
class PingTests(unittest.TestCase):

    def test_ping(self):
        response = self.client.get(url_for('api.ping'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'pong')
