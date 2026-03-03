#!/usr/bin/env python3
"""Unit tests for TradingHoursChecker"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from trade_utils import TradingHoursChecker


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


if __name__ == "__main__":
    unittest.main()
