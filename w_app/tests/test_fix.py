from django.test import TestCase
from ..fix_engine import *
import ipdb
import sys

def fix_str(s):
    if sys.version_info[0] == 2:
        return bytes(s)
    return bytes(s, 'ASCII')


class TestFix(TestCase):



    def setUp(self):
        test_message=simplefix.FixMessage()

    def test_header(self):
        """Testing header of fix message"""
        header = create_fix_header('TEST')
        self.assertEqual(header.get(8), b"FIX.4.4")
        self.assertEqual(header.get(35), b"TEST")
        self.assertEqual(header.get(49), b"SENDER")
        self.assertEqual(header.get(56), b"TARGET")
        self.assertEqual(header.get(34), b'4684')
        self.assertIsNotNone(header.get(52))

    def test_header_count(self):
        """Testing count of tags in fix message header"""
        header = create_fix_header('TEST')
        self.assertEqual(header.count(), 6)
