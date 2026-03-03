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

    def get_contract_open_interest(self, exchange: str, contract: str) -> Optional[int]:
        """
        Query open interest for a contract using tianqin-data
        Returns: open_interest value or None if failed
        """
        import sys
        symbol = f"{exchange}.{contract}"

        # Find tq_cli.py path
        tq_cli_path = SCRIPT_DIR.parent.parent / "tianqin-data" / "scripts" / "tq_cli.py"

        if not tq_cli_path.exists():
            print(f"Warning: tianqin-data not found at {tq_cli_path}", file=sys.stderr)
            return None

        try:
            result = subprocess.run(
                ["python3", str(tq_cli_path), "quote", symbol],
                capture_output=True,
                text=True,
                timeout=10,
                env=os.environ.copy()
            )

            if result.returncode != 0:
                return None

            # Parse JSON response
            data = json.loads(result.stdout)

            # Extract open interest (try multiple field names)
            open_interest = data.get("open_interest") or data.get("持仓量") or data.get("open_interest_lot")

            if open_interest:
                return int(open_interest)

            return None

        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
            print(f"Warning: Failed to get open interest for {symbol}: {e}", file=sys.stderr)
            return None

    def update_variety(self, variety: str, exchange: str) -> bool:
        """
        Update dominant contract for a single variety
        Returns: True if successful, False otherwise
        """
        import sys
        contracts = self.generate_contract_codes(variety, exchange)

        max_oi = 0
        dominant_contract = None

        print(f"  Checking {len(contracts)} contracts for {variety}...", file=sys.stderr)

        for contract in contracts:
            oi = self.get_contract_open_interest(exchange, contract)
            if oi and oi > max_oi:
                max_oi = oi
                dominant_contract = contract

        if dominant_contract:
            self.config[variety.lower()] = {
                "dominant": dominant_contract,
                "exchange": exchange,
                "updated_at": datetime.now().isoformat()
            }
            print(f"  ✓ {variety}: {dominant_contract} (OI: {max_oi})", file=sys.stderr)
            return True
        else:
            print(f"  ✗ {variety}: No data found", file=sys.stderr)
            return False

    def update_dominant(self, varieties: Optional[List[str]] = None) -> Dict:
        """
        Update dominant contracts for specified varieties or all
        Returns: {"updated": int, "failed": int, "timestamp": str}
        """
        import sys
        # Default varieties to update (common contracts)
        default_varieties = [
            ("rb", "SHFE"), ("cu", "SHFE"), ("al", "SHFE"), ("au", "SHFE"),
            ("ag", "SHFE"), ("ru", "SHFE"), ("bu", "SHFE"), ("hc", "SHFE"),
            ("a", "DCE"), ("m", "DCE"), ("y", "DCE"), ("p", "DCE"),
            ("i", "DCE"), ("j", "DCE"), ("jm", "DCE"), ("l", "DCE"),
            ("v", "DCE"), ("pp", "DCE"), ("eg", "DCE"),
            ("CF", "CZCE"), ("SR", "CZCE"), ("TA", "CZCE"), ("MA", "CZCE"),
            ("RM", "CZCE"), ("OI", "CZCE"), ("FG", "CZCE"), ("ZC", "CZCE"),
            ("IF", "CFFEX"), ("IC", "CFFEX"), ("IH", "CFFEX"),
            ("sc", "INE"), ("lu", "INE"), ("nr", "INE")
        ]

        if varieties:
            # Filter to specified varieties
            varieties_set = set(v.lower() for v in varieties)
            update_list = [(v, e) for v, e in default_varieties if v.lower() in varieties_set]
        else:
            update_list = default_varieties

        print(f"Updating {len(update_list)} varieties...", file=sys.stderr)

        updated = 0
        failed = 0

        for variety, exchange in update_list:
            print(f"\n[{updated + failed + 1}/{len(update_list)}] {variety} ({exchange})", file=sys.stderr)
            if self.update_variety(variety, exchange):
                updated += 1
            else:
                failed += 1

        # Save updated config
        self.save_config()

        print(f"\n✅ Update complete: {updated} succeeded, {failed} failed", file=sys.stderr)

        return {
            "updated": updated,
            "failed": failed,
            "timestamp": datetime.now().isoformat()
        }


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
            varieties = args.varieties.split(',') if args.varieties else None
            manager = DominantContractManager(DOMINANT_CONTRACTS_FILE)
            result = manager.update_dominant(varieties)
            print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
