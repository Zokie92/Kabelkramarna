import unittest
import sys
import os

# Add parent directory to path so we can import the scanner module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Luddes_slask1 import parse_ports


class TestPortParser(unittest.TestCase):
    def test_single_port(self):
        self.assertEqual(parse_ports('80'), [80])

    def test_multiple_ports(self):
        self.assertEqual(parse_ports('22,80,443'), [22, 80, 443])

    def test_port_range(self):
        self.assertEqual(parse_ports('8000-8002'), [8000, 8001, 8002])

    def test_combined(self):
        self.assertEqual(
            parse_ports('22,80,8000-8002,443'), 
            [22, 80, 443, 8000, 8001, 8002]
        )

    def test_invalid_ports(self):
        with self.assertRaises(ValueError):
            parse_ports('abc')
        with self.assertRaises(ValueError):
            parse_ports('0')  # port 0 not allowed
        with self.assertRaises(ValueError):
            parse_ports('65536')  # > max port
        with self.assertRaises(ValueError):
            parse_ports('80-70')  # invalid range


if __name__ == '__main__':
    unittest.main()