---
name: tq-skill
description: CLI wrapper and API reference for China futures data retrieval from EasyFut API. Use when fetching real-time quotes, K-line candlestick data, or tick sequences for China futures contracts (IF, IC, IH, and other CFFEX/DCE/SHFE symbols). Supports advanced filtering by date range and intervals, with authentication via API key.
---

# TQ Skill - China Futures Data

## Overview

TQ Skill provides command-line access to China futures market data through the EasyFut API. Fetch real-time quotes, historical K-line data, and granular tick sequences for major futures contracts traded on Chinese exchanges (CFFEX, DCE, SHFE).

## Quick Start

### Installation

Install the CLI tool:
```bash
# Make the script executable
chmod +x scripts/tq_cli.py

# Optionally, add to PATH or create an alias
alias tq='python3 /path/to/tq_cli.py'
```

### Basic Usage

Get a real-time quote:
```bash
python3 scripts/tq_cli.py quote IF
```

Get daily K-line data:
```bash
python3 scripts/tq_cli.py klines IC --interval 1d
```

Get tick data for a date range:
```bash
python3 scripts/tq_cli.py ticks IH --start-date 2024-01-15 --end-date 2024-01-16
```

## Core Capabilities

### 1. Real-Time Quotes

Fetch current market data for any futures contract:

```bash
tq quote IF
tq quote IC
tq quote IH
```

Returns current price, bid/ask, volume, and open interest in JSON format.

**See:** [API Reference - Real-time Quotes](references/api_reference.md#1-real-time-quotes)

---

### 2. K-Line Historical Data

Retrieve candlestick data at various intervals (1m, 5m, 15m, 1h, 1d, etc.):

```bash
# Daily candles
tq klines IF --interval 1d --start-date 2024-01-01 --end-date 2024-01-31

# Hourly candles
tq klines IC --interval 1h --start-date 2024-01-15 --end-date 2024-01-15

# 5-minute intraday candles
tq klines IH --interval 5m
```

Returns OHLC (open, high, low, close) data with volume and open interest.

**See:** [API Reference - K-Line Data](references/api_reference.md#2-k-line-data)

---

### 3. Tick Sequences

Get granular tick-level transaction data for detailed market analysis:

```bash
# All recent tick data
tq ticks IF

# Tick data for specific date range
tq ticks IC --start-date 2024-01-15 --end-date 2024-01-16
```

Returns individual tick prices, volumes, and transaction types (bid/ask/trade).

**See:** [API Reference - Tick Data](references/api_reference.md#3-tick-sequence-data)

---

## Configuration

### API Authentication

Set your API key as an environment variable:

```bash
export TQ_API_KEY="your_api_key_here"
tq quote IF
```

Or pass it directly to each command:

```bash
tq --api-key "your_api_key_here" quote IF
```

### Supported Symbols

Common China futures symbols:

| Index Futures | Commodity Futures |
|---|---|
| IF (Shanghai 300) | CU (Copper) |
| IC (Mid-Cap 100) | AL (Aluminum) |
| IH (Shanghai 50) | RB (Rebar) |
| T (10Y Bond) | CF (Cotton) |
| TF (5Y Bond) | SR (Sugar) |

See full list in [API Reference - Common Symbols](references/api_reference.md#common-futures-symbols)

---

## Examples

### Analyze Recent Price Trends
```bash
tq klines IF --interval 1d --start-date 2024-01-01 --end-date 2024-01-31
```

### Monitor Intraday Volatility
```bash
tq klines IC --interval 15m --start-date 2024-01-15
```

### Check Current Market Activity
```bash
tq quote IF
tq quote IC
tq quote IH
```

### Study Tick-Level Activity
```bash
tq ticks IF --start-date 2024-01-15 --end-date 2024-01-16
```

---

## Output Format

All commands return JSON output for easy integration with other tools:

```json
{
  "symbol": "IF",
  "price": 4500.50,
  "bid": 4500.00,
  "ask": 4501.00,
  "volume": 1000000,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Scripts

### tq_cli.py

Main CLI tool for accessing EasyFut API. Provides three commands: `quote`, `klines`, and `ticks`.

**Usage:**
```bash
python3 scripts/tq_cli.py <command> [options]
```

**Commands:**
- `quote <symbol>` - Get real-time quote
- `klines <symbol> [--interval] [--start-date] [--end-date]` - Get K-line data
- `ticks <symbol> [--start-date] [--end-date]` - Get tick data

**Global Options:**
- `--api-key` - EasyFut API key (or use TQ_API_KEY env var)

---

## Advanced Reference

For detailed API documentation including:
- All supported parameters and intervals
- Error handling and rate limits
- Data availability and historical limits
- Complete futures symbol reference

See: [API Reference Documentation](references/api_reference.md)
