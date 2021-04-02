"""
Unit tests for the lepton module.
"""

# unit test imports
import unittest

# project imports
from core.lepton import (Lepton,
                         to_celsius,
                         to_fahrenheit,
                         to_kelvin)


class TestLeptonModule(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
