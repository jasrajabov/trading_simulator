from django.test import TestCase
from ..fix_messages import *
import ipdb
import sys
import ipdb

def fix_str(s):
    if sys.version_info[0] == 2:
        return bytes(s)
    return bytes(s, 'ASCII')


class TestFix(TestCase):

    def setUp(self):
        test_message=simplefix.FixMessage()

    def test_header(self):
        """Testing header of fix message"""
        header = create_fix_header('T')
        self.assertEqual(header.get(8), b"FIX.4.4")
        self.assertEqual(header.get(35), b"T")
        self.assertEqual(header.get(49), b"SENDER")
        self.assertEqual(header.get(56), b"TARGET")
        self.assertEqual(header.get(34), b'4684')
        self.assertIsNotNone(header.get(52))

    def test_header_count(self):
        """Testing count of tags in fix message header"""
        header = create_fix_header('TEST')
        self.assertEqual(header.count(), 6)

    def test_body(self):
        """Testing the body of fix message"""
        header = create_fix_header('T')
        body = create_body(header, 'FB', 1, 1, 1)
        self.assertEqual(body.get(55), b'FB')
        self.assertIsNotNone(body.get(60))
        self.assertEqual(body.get(54), b'1')
        self.assertEqual(body.get(40), b'1')
        self.assertEqual(body.get(38), b'1')
        # ipdb.set_trace()

    def test_body_count(self):
        """testing the count of body"""
        header = create_fix_header('T')
        body = create_body(header, 'FB', 1, 1, 1)
        self.assertEqual(body.count(), 11)

    def test_createNewOrderSinge(self):
        """Testing new order single message"""
        new_order = createNewOrderSinge('FB', 1, 1, 1)
        self.assertEqual(new_order.get(35), b'D')
        self.assertEqual(new_order.count(), 11)
