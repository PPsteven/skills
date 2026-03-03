#!/usr/bin/env python3
"""
Trade Skills Utilities
Provides trading hours checking and dominant contract lookup for China futures.
"""

from pathlib import Path
from typing import Tuple, Dict, Optional, List
from datetime import time, datetime, timedelta
import json
import subprocess
import os


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


class DominantContractManager:
    """Manage dominant contract configuration and lookup"""

    def __init__(self, config_file: str):
        """
        Initialize dominant contract manager

        Args:
            config_file: Path to dominant_contracts.json
        """
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict[str, str]:
        """Load dominant contracts from JSON file"""
        if not os.path.exists(self.config_file):
            return {}

        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_config(self):
        """Save current config to JSON file"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def get_dominant(self, variety: str) -> Optional[str]:
        """
        Get dominant contract for a variety

        Args:
            variety: Variety code like 'rb', 'i', 'SR'

        Returns:
            Dominant contract code like 'rb2505', or None if not found
        """
        return self.config.get(variety)

    def generate_contract_codes(
        self,
        variety: str,
        exchange: str = "SHFE",
        months: int = 6
    ) -> List[str]:
        """
        Generate contract codes for next N months

        Args:
            variety: Variety code like 'rb', 'SR'
            exchange: Exchange code (SHFE/DCE/CFFEX use 4 digits, CZCE uses 3)
            months: Number of months to generate

        Returns:
            List of contract codes like ['rb2503', 'rb2504', ...]
        """
        codes = []
        now = datetime.now()

        for i in range(months):
            future_date = now + timedelta(days=30 * i)
            year = future_date.year % 100  # Get last 2 digits
            month = future_date.month

            if exchange == "CZCE":
                # CZCE format: SR + YMM (e.g., SR503)
                code = f"{variety}{year % 10}{month:02d}"
            else:
                # SHFE/DCE/CFFEX format: rb + YYMM (e.g., rb2503)
                code = f"{variety}{year:02d}{month:02d}"

            codes.append(code)

        return codes


# Constants for file paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
TRADING_HOURS_FILE = DATA_DIR / "trading_hours.json"
DOMINANT_CONTRACTS_FILE = DATA_DIR / "dominant_contracts.json"


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Trade Skills Utilities - Trading hours and dominant contracts"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # is-trading command
    is_trading_parser = subparsers.add_parser(
        "is-trading",
        help="Check if a contract is currently in trading hours"
    )
    is_trading_parser.add_argument(
        "symbol",
        help="Contract symbol (e.g., SHFE.rb2601, CFFEX.IF2603)"
    )

    # dominant-contract command
    dominant_parser = subparsers.add_parser(
        "dominant-contract",
        help="Get dominant contract for a variety"
    )
    dominant_parser.add_argument(
        "variety",
        help="Variety code (e.g., rb, cu, IF)"
    )

    # update-dominant command
    update_parser = subparsers.add_parser(
        "update-dominant",
        help="Update dominant contracts database"
    )
    update_parser.add_argument(
        "--varieties",
        help="Comma-separated list of varieties to update (default: all)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "is-trading":
            checker = TradingHoursChecker(TRADING_HOURS_FILE)
            result = checker.check_trading(args.symbol)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "dominant-contract":
            manager = DominantContractManager(DOMINANT_CONTRACTS_FILE)
            result = manager.get_dominant(args.variety)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "update-dominant":
            print("Error: update-dominant not yet implemented", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
