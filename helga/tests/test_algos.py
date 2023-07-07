import unittest

from helga.algos import gcd


class TestGCD(unittest.TestCase):
    def test_int(self):
        self.assertEqual(gcd(12, 18), 6)
        self.assertEqual(gcd(5, 7), 1)
