#!/usr/bin/env python3
"""
Generate trading_hours.json from akshare-data/references/futures.md
Run this once to initialize the trading hours configuration.
"""

import json
import re
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
FUTURES_MD = SCRIPT_DIR.parent.parent / "akshare-data" / "references" / "futures.md"
OUTPUT_FILE = SCRIPT_DIR / "data" / "trading_hours.json"


def parse_trading_hours_table(md_file: Path) -> dict:
    """
    Parse the trading hours table from futures.md
    Returns: nested dict structure for trading_hours.json
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the trading hours table section
    # Table starts with: | 交易所 | 交易所代码 | 品种名称 | 品种代码 | 集合竞价 | 日盘时间 | 夜盘时间 |
    pattern = r'\| 交易所\s+\| 交易所代码\s+\| 品种名称\s+\| 品种代码\s+\| 集合竞价.*?\n\|[-\s|]+\n((?:\|.*?\n)+?)(?:\n\n|\n#)'

    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

    if not match:
        raise ValueError("Could not find trading hours table in futures.md")

    table_content = match.group(1).strip()
    table_rows = table_content.split('\n')

    config = {}

    for row in table_rows:
        # Parse table row: | 交易所名 | 代码 | 品种名 | 品种代码 | 集合竞价 | 日盘 | 夜盘 |
        cols = [col.strip() for col in row.split('|')[1:-1]]

        if len(cols) < 7:
            continue

        exchange_name, exchange_code, variety_name, variety_code, call_auction, day_hours, night_hours = cols[:7]

        # Skip empty rows
        if not variety_code or not exchange_code:
            continue

        # Initialize exchange if not exists
        if exchange_code not in config:
            config[exchange_code] = {}

        # Parse day sessions (comma-separated time ranges)
        day_sessions = []
        if day_hours and day_hours != '-':
            day_sessions = [s.strip() for s in day_hours.split(',') if s.strip()]

        # Parse call auction sessions
        call_auction_sessions = None
        if call_auction and call_auction != '-':
            call_auction_sessions = [s.strip() for s in call_auction.split(',') if s.strip()]

        # Parse night sessions
        night_sessions = None
        if night_hours and night_hours != '-':
            night_sessions = [s.strip() for s in night_hours.split(',') if s.strip()]

        # Add to config
        config[exchange_code][variety_code] = {
            "name": variety_name,
            "call_auction": call_auction_sessions,
            "day": day_sessions,
            "night": night_sessions
        }

    return config


def main():
    """Generate trading_hours.json from futures.md"""
    print("Parsing futures.md...")

    if not FUTURES_MD.exists():
        print(f"Error: {FUTURES_MD} not found")
        print("Make sure akshare-data skill is installed")
        return 1

    try:
        config = parse_trading_hours_table(FUTURES_MD)

        variety_count = sum(len(varieties) for varieties in config.values())
        exchange_count = len(config)

        print(f"Found {variety_count} varieties across {exchange_count} exchanges")

        # Create output directory
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Write to JSON
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"✅ Generated: {OUTPUT_FILE}")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
