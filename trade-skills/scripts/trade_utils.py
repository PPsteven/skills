#!/usr/bin/env python3
"""
Trade Skills Utilities
Provides trading hours checking and dominant contract lookup for China futures.
"""

from pathlib import Path
from typing import Tuple, Dict
from datetime import time, datetime
import json


class TradingHoursChecker:
    """Check if a futures contract is currently in trading hours"""

    def __init__(self, config_file: Path):
        self.config_file = config_file
        if config_file:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def parse_symbol(self, symbol: str) -> Tuple[str, str]:
        """
        Parse symbol like 'SHFE.rb2601' into (exchange, variety)
        Returns: ('SHFE', 'rb')
        """
        if '.' not in symbol:
            raise ValueError(
                f"Invalid symbol format: {symbol}. "
                f"Expected: EXCHANGE.SYMBOL (e.g., SHFE.rb2601)"
            )

        parts = symbol.split('.')
        if len(parts) != 2:
            raise ValueError(
                f"Invalid symbol format: {symbol}. "
                f"Expected exactly one dot."
            )

        exchange = parts[0].upper().strip()
        variety_with_month = parts[1].strip()

        if not exchange or not variety_with_month:
            raise ValueError(
                f"Invalid symbol format: {symbol}. "
                f"Exchange and variety cannot be empty."
            )

        # Extract variety code (remove month digits)
        variety = ''.join(c for c in variety_with_month if not c.isdigit())

        if not variety:
            raise ValueError(
                f"Invalid symbol format: {symbol}. "
                f"Variety code cannot be all digits."
            )

        return exchange, variety

    def parse_time_range(self, time_range: str) -> Tuple[time, time]:
        """
        Parse time range like '09:00-10:15' into (start_time, end_time)
        """
        start_str, end_str = time_range.split('-')
        start_hour, start_min = map(int, start_str.split(':'))
        end_hour, end_min = map(int, end_str.split(':'))

        return time(start_hour, start_min), time(end_hour, end_min)

    def is_cross_midnight(self, start: time, end: time) -> bool:
        """Check if time range crosses midnight (e.g., 21:00-01:00)"""
        return start > end

    def is_in_time_range(self, current: time, time_range: str) -> bool:
        """Check if current time is within the time range"""
        start, end = self.parse_time_range(time_range)

        if self.is_cross_midnight(start, end):
            # Crosses midnight: 21:00-01:00
            return current >= start or current <= end
        else:
            # Normal range: 09:00-10:15
            return start <= current <= end

    def check_trading(self, symbol: str) -> Dict:
        """
        Check if contract is currently trading.

        Args:
            symbol: Contract symbol like 'SHFE.rb2601'

        Returns:
            {
                "symbol": "SHFE.rb2601",
                "trading": True/False,
                "session": "day"/"night"/None,
                "next_session": {...}  # Optional
            }
        """
        exchange, variety = self.parse_symbol(symbol)

        # Get config for this exchange and variety
        if exchange not in self.config:
            raise ValueError(f"No config for exchange: {exchange}")

        if variety not in self.config[exchange]:
            raise ValueError(
                f"No config for variety: {variety} on {exchange}"
            )

        variety_config = self.config[exchange][variety]
        current_time = datetime.now().time()

        # Check day session
        if variety_config.get("day"):
            for time_range in variety_config["day"]:
                if self.is_in_time_range(current_time, time_range):
                    return {
                        "symbol": symbol,
                        "trading": True,
                        "session": "day"
                    }

        # Check night session
        if variety_config.get("night"):
            for time_range in variety_config["night"]:
                if self.is_in_time_range(current_time, time_range):
                    return {
                        "symbol": symbol,
                        "trading": True,
                        "session": "night"
                    }

        # Not trading
        return {
            "symbol": symbol,
            "trading": False,
            "session": None
        }
