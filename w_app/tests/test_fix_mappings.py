from django.test import TestCase
from ..fix_mapping import *

class TestFixMappings(TestCase):

    def test_side(self):
        self.assertEqual(Side.get('Buy'), 1)
        self.assertEqual(Side.get('Sell'), 2)

    def test_ordertype(self):
        self.assertEqual(OrderType.get('Market'), 1)
        self.assertEqual(OrderType.get('Limit'), 2)
        self.assertEqual(OrderType.get('Stop'), 3)
        self.assertEqual(OrderType.get('Stop limit'), 4)
