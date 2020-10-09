from django.test import TestCase
from w_app.settings import api_key
from rest_framework.test import APIClient
import requests
import ipdb


class FinnhubApi(TestCase):

    def setUp(self):
        self.client = requests

    def test_finnhub_connection(self):
        """Test finnhub connection is successful"""
        resp = self.client.get('https://finnhub.io/api/v1/quote?symbol={}&token={}'.format('AAPL',api_key))
        # ipdb.set_trace()
        self.assertEqual(resp.status_code, 200)
