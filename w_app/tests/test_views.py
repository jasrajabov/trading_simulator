from django.test import TestCase
from ..views import *

class ViewsTestCases(TestCase):

    def test_whatever_list_view(self):
        """Test homepage is successful"""
        url = 'http://localhost:8000/'
        resp = self.client.get(url)
        # import ipdb; ipdb.set_trace()

        self.assertEqual(resp.status_code, 200)

    def test_order_page(self):
        """Testing order page"""
        url = 'http://localhost:8000/blotter/?name=&_TraderId=444&_Side=Buy&_OrderType=Limit&_Quantity=1&_Price=1'
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_time_converter(self):
        """Test time convert from date to unixtime"""
        date = '2020-01-01'
        time = time_converter(date)
        self.assertEqual(time, '1577854800')
