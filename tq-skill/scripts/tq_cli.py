#!/usr/bin/env python3
"""
TQ Skill CLI - China Futures Data Retrieval Tool
Fetch real-time quotes, K-line data, and tick sequences from EasyFut API.
"""

import argparse
import json
import sys
from typing import Optional
import requests


class TQClient:
    """TQ API Client for China Futures Data"""

    BASE_URL = "http://47.115.228.20:8888"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize TQ client with optional API key"""
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def get_quote(self, symbol: str) -> dict:
        """Get real-time quote for a futures contract

        Args:
            symbol: Futures symbol with exchange prefix (e.g., SHFE.rb2601, CFFEX.IF2601)
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/quote/{symbol}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch quote: {str(e)}"}

    def get_klines(
        self,
        symbol: str,
        duration_seconds: int,
        data_length: int = 100
    ) -> dict:
        """Get K-line data for a futures contract

        Args:
            symbol: Futures symbol with exchange prefix (e.g., SHFE.rb2601)
            duration_seconds: K-line period in seconds (60=1min, 300=5min, 3600=1hour, 86400=1day)
            data_length: Number of K-line bars to retrieve (max 8000)
        """
        try:
            # Format: {symbol}_{duration_seconds}_{data_length}
            klines_symbol = f"{symbol}_{duration_seconds}_{data_length}"

            response = requests.get(
                f"{self.BASE_URL}/klines/{klines_symbol}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch klines: {str(e)}"}

    def get_ticks(
        self,
        symbol: str,
        data_length: int = 100
    ) -> dict:
        """Get tick sequence data for a futures contract

        Args:
            symbol: Futures symbol with exchange prefix (e.g., SHFE.rb2601)
            data_length: Number of ticks to retrieve (max 8000)
        """
        try:
            # Format: {symbol}_{data_length}
            ticks_symbol = f"{symbol}_{data_length}"

            response = requests.get(
                f"{self.BASE_URL}/ticks/{ticks_symbol}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch ticks: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(
        description="TQ Skill - Fetch China futures data from EasyFut API"
    )
    parser.add_argument("--api-key", help="EasyFut API key (or set TQ_API_KEY env var)")

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Quote command
    quote_parser = subparsers.add_parser("quote", help="Get real-time quote")
    quote_parser.add_argument(
        "symbol",
        help="Futures symbol with exchange (e.g., SHFE.rb2601, CFFEX.IF2601)"
    )

    # Klines command
    klines_parser = subparsers.add_parser("klines", help="Get K-line data")
    klines_parser.add_argument(
        "symbol",
        help="Futures symbol with exchange (e.g., SHFE.rb2601)"
    )
    klines_parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="K-line duration in seconds (60=1min, 300=5min, 3600=1hour, 86400=1day)"
    )
    klines_parser.add_argument(
        "--length",
        type=int,
        default=100,
        help="Number of K-line bars to retrieve (max 8000)"
    )

    # Ticks command
    ticks_parser = subparsers.add_parser("ticks", help="Get tick sequence")
    ticks_parser.add_argument(
        "symbol",
        help="Futures symbol with exchange (e.g., SHFE.rb2601)"
    )
    ticks_parser.add_argument(
        "--length",
        type=int,
        default=100,
        help="Number of ticks to retrieve (max 8000)"
    )

    args = parser.parse_args()

    # Get API key from args or environment
    import os
    api_key = args.api_key or os.getenv("TQ_API_KEY")

    # Initialize client
    client = TQClient(api_key=api_key)

    # Execute commands
    if args.command == "quote":
        result = client.get_quote(args.symbol)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "klines":
        result = client.get_klines(
            args.symbol,
            duration_seconds=args.duration,
            data_length=args.length
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "ticks":
        result = client.get_ticks(
            args.symbol,
            data_length=args.length
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
