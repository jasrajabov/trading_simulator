from django.test import TestCase
from ..views import *

class ViewsTestCases(TestCase):
    def test_time_converter(self):
        """Test time convert from date to unixtime"""
        date = '2020-01-01'
        time = time_converter(date)
        self.assertEqual(time, '1577854800')
