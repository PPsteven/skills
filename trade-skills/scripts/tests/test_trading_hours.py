#!/usr/bin/env python3
"""Unit tests for TradingHoursChecker"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from trade_utils import TradingHoursChecker
from datetime import time
import json
import tempfile


def create_test_config():
    """Create temporary test config file"""
    config = {
        "SHFE": {
            "rb": {
                "name": "螺纹钢",
                "call_auction": ["20:55-21:00", "08:55-09:00"],
                "day": ["09:00-10:15", "10:30-11:30", "13:30-15:00"],
                "night": ["21:00-23:00"]
            },
            "cu": {
                "name": "铜",
                "call_auction": ["20:55-21:00", "08:55-09:00"],
                "day": ["09:00-10:15", "10:30-11:30", "13:30-15:00"],
                "night": ["21:00-01:00"]
            }
        },
        "CFFEX": {
            "IF": {
                "name": "沪深300指数",
                "call_auction": ["09:25-09:30"],
                "day": ["09:30-11:30", "13:00-15:00"],
                "night": None
            }
        }
    }

    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(config, temp_file)
    temp_file.close()
    return Path(temp_file.name)


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


class TestTimeRangeChecking(unittest.TestCase):

    def setUp(self):
        self.checker = TradingHoursChecker(None)

    def test_is_in_time_range_normal_inside(self):
        """Test time inside normal range"""
        result = self.checker.is_in_time_range(time(9, 30), "09:00-10:15")
        self.assertTrue(result)

    def test_is_in_time_range_normal_outside_before(self):
        """Test time before normal range"""
        result = self.checker.is_in_time_range(time(8, 30), "09:00-10:15")
        self.assertFalse(result)

    def test_is_in_time_range_normal_outside_after(self):
        """Test time after normal range"""
        result = self.checker.is_in_time_range(time(10, 30), "09:00-10:15")
        self.assertFalse(result)

    def test_is_in_time_range_cross_midnight_before_midnight(self):
        """Test time in cross-midnight range (before midnight)"""
        result = self.checker.is_in_time_range(time(22, 0), "21:00-01:00")
        self.assertTrue(result)

    def test_is_in_time_range_cross_midnight_after_midnight(self):
        """Test time in cross-midnight range (after midnight)"""
        result = self.checker.is_in_time_range(time(0, 30), "21:00-01:00")
        self.assertTrue(result)

    def test_is_in_time_range_cross_midnight_outside(self):
        """Test time outside cross-midnight range"""
        result = self.checker.is_in_time_range(time(10, 0), "21:00-01:00")
        self.assertFalse(result)


class TestCheckTrading(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_config_path = create_test_config()

    def test_check_trading_day_session(self):
        """Test during day session (10:00)"""
        from unittest.mock import patch
        with patch('trade_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value.time.return_value = time(10, 0)

            checker = TradingHoursChecker(self.test_config_path)
            result = checker.check_trading("SHFE.rb2601")

            self.assertEqual(result["trading"], True)
            self.assertEqual(result["session"], "day")
            self.assertEqual(result["symbol"], "SHFE.rb2601")

    def test_check_trading_night_session(self):
        """Test during night session (22:00)"""
        from unittest.mock import patch
        with patch('trade_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value.time.return_value = time(22, 0)

            checker = TradingHoursChecker(self.test_config_path)
            result = checker.check_trading("SHFE.rb2601")

            self.assertEqual(result["trading"], True)
            self.assertEqual(result["session"], "night")

    def test_check_trading_closed(self):
        """Test when market is closed (16:00)"""
        from unittest.mock import patch
        with patch('trade_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value.time.return_value = time(16, 0)

            checker = TradingHoursChecker(self.test_config_path)
            result = checker.check_trading("SHFE.rb2601")

            self.assertEqual(result["trading"], False)
            self.assertIsNone(result["session"])

    def test_check_trading_cross_midnight(self):
        """Test cross-midnight session (00:30 for copper)"""
        from unittest.mock import patch
        with patch('trade_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value.time.return_value = time(0, 30)

            checker = TradingHoursChecker(self.test_config_path)
            result = checker.check_trading("SHFE.cu2601")

            self.assertEqual(result["trading"], True)
            self.assertEqual(result["session"], "night")


if __name__ == "__main__":
    unittest.main()
