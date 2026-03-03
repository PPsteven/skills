#!/usr/bin/env python3
"""Unit tests for TradingHoursChecker"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from trade_utils import TradingHoursChecker
from datetime import time


class TestSymbolParsing(unittest.TestCase):

    def test_parse_symbol_with_exchange_prefix(self):
        """Test parsing SHFE.rb2601 format"""
        checker = TradingHoursChecker(None)
        exchange, variety = checker.parse_symbol("SHFE.rb2601")
        self.assertEqual(exchange, "SHFE")
        self.assertEqual(variety, "rb")

    def test_parse_symbol_cffex(self):
        """Test parsing CFFEX.IF2603 format"""
        checker = TradingHoursChecker(None)
        exchange, variety = checker.parse_symbol("CFFEX.IF2603")
        self.assertEqual(exchange, "CFFEX")
        self.assertEqual(variety, "IF")

    def test_parse_symbol_invalid_no_dot(self):
        """Test error on rb2601 without exchange"""
        checker = TradingHoursChecker(None)
        with self.assertRaises(ValueError) as context:
            checker.parse_symbol("rb2601")
        self.assertIn("Invalid symbol format", str(context.exception))

    def test_parse_symbol_empty_exchange(self):
        """Test error on empty exchange"""
        checker = TradingHoursChecker(None)
        with self.assertRaises(ValueError):
            checker.parse_symbol(".rb2601")

    def test_parse_symbol_empty_variety(self):
        """Test error on empty variety"""
        checker = TradingHoursChecker(None)
        with self.assertRaises(ValueError):
            checker.parse_symbol("SHFE.")

    def test_parse_symbol_multiple_dots(self):
        """Test error on multiple dots"""
        checker = TradingHoursChecker(None)
        with self.assertRaises(ValueError):
            checker.parse_symbol("SHFE.rb.2601")

    def test_parse_symbol_all_digits(self):
        """Test error on all-digit variety"""
        checker = TradingHoursChecker(None)
        with self.assertRaises(ValueError):
            checker.parse_symbol("SHFE.2601")


class TestTimeRangeParsing(unittest.TestCase):

    def setUp(self):
        self.checker = TradingHoursChecker(None)

    def test_parse_time_range_morning(self):
        """Test parsing 09:00-10:15"""
        start, end = self.checker.parse_time_range("09:00-10:15")
        self.assertEqual(start, time(9, 0))
        self.assertEqual(end, time(10, 15))

    def test_parse_time_range_night(self):
        """Test parsing 21:00-23:00"""
        start, end = self.checker.parse_time_range("21:00-23:00")
        self.assertEqual(start, time(21, 0))
        self.assertEqual(end, time(23, 0))

    def test_is_cross_midnight_false(self):
        """Test 09:00-10:15 does not cross midnight"""
        result = self.checker.is_cross_midnight(time(9, 0), time(10, 15))
        self.assertFalse(result)

    def test_is_cross_midnight_true(self):
        """Test 21:00-01:00 crosses midnight"""
        result = self.checker.is_cross_midnight(time(21, 0), time(1, 0))
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
