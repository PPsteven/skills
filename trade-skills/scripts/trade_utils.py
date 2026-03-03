#!/usr/bin/env python3
"""
Trade Skills Utilities
Provides trading hours checking and dominant contract lookup for China futures.
"""

from pathlib import Path
from typing import Tuple


class TradingHoursChecker:
    """Check if a futures contract is currently in trading hours"""

    def __init__(self, config_file: Path):
        self.config_file = config_file
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
