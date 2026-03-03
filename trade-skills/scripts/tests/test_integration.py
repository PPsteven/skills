#!/usr/bin/env python3
"""Integration tests for trade_utils CLI"""

import subprocess
import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).parent.parent / "trade_utils.py"


def run_command(args):
    """Run trade_utils.py command and return parsed JSON output"""
    result = subprocess.run(
        ["python3", str(SCRIPT_PATH)] + args,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Command failed: {' '.join(args)}")
        print(f"STDERR: {result.stderr}")
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Invalid JSON output: {result.stdout}")
        return None


def test_is_trading_command():
    """Test is-trading command"""
    print("Testing is-trading command...")

    result = run_command(["is-trading", "SHFE.rb2601"])

    assert result is not None, "Command failed"
    assert "trading" in result, "Missing 'trading' field"
    assert "session" in result, "Missing 'session' field"
    assert "symbol" in result, "Missing 'symbol' field"
    assert result["symbol"] == "SHFE.rb2601", "Wrong symbol in output"
    assert isinstance(result["trading"], bool), "'trading' should be bool"

    print("✅ is-trading command works")


def test_dominant_contract_command_not_found():
    """Test dominant-contract command with missing data"""
    print("Testing dominant-contract command (expect null)...")

    result = subprocess.run(
        ["python3", str(SCRIPT_PATH), "dominant-contract", "nonexistent"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, "Should succeed with exit code 0"
    assert result.stdout.strip() == "null", "Should return null for nonexistent variety"

    print("✅ dominant-contract error handling works")


def test_cli_help():
    """Test --help output"""
    print("Testing --help...")

    result = subprocess.run(
        ["python3", str(SCRIPT_PATH), "--help"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, "Help should succeed"
    assert "is-trading" in result.stdout, "Help should mention is-trading"
    assert "dominant-contract" in result.stdout, "Help should mention dominant-contract"
    assert "update-dominant" in result.stdout, "Help should mention update-dominant"

    print("✅ CLI help works")


def test_invalid_symbol_format():
    """Test error handling for invalid symbol format"""
    print("Testing invalid symbol format...")

    result = subprocess.run(
        ["python3", str(SCRIPT_PATH), "is-trading", "rb2601"],
        capture_output=True,
        text=True
    )

    assert result.returncode != 0, "Should fail for invalid format"
    assert "Invalid symbol format" in result.stderr, "Should have format error"

    print("✅ Invalid symbol error handling works")


if __name__ == "__main__":
    print("Running integration tests...\n")

    test_cli_help()
    test_is_trading_command()
    test_invalid_symbol_format()
    test_dominant_contract_command_not_found()

    print("\n✅ All integration tests passed!")
