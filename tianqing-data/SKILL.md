---
name: tianqing-data
description: CLI wrapper and API reference for China futures market data from EasyFut API. Use this skill to access real-time quotes, K-line candlestick data, and tick sequences for China futures contracts across major exchanges (SHFE, DCE, CFFEX, CZCE, INE). All commands require exchange prefix format (e.g., SHFE.rb2601, CFFEX.IF2601).
---

# TianQing Data - China Futures Market API

## Overview

TianQing Data provides command-line access to China futures market data through the EasyFut API. Fetch real-time quotes, historical K-line data, and granular tick sequences for futures contracts traded on Chinese exchanges including SHFE (Shanghai Futures Exchange), DCE (Dalian Commodity Exchange), CFFEX (China Financial Futures Exchange), CZCE (Zhengzhou Commodity Exchange), and INE (Shanghai International Energy Exchange).

## Quick Start

### CLI Usage

All commands require the full exchange prefix format:

```bash
# Get real-time quote
python3 scripts/tq_cli.py quote SHFE.rb2601

# Get K-line data (1-minute candles, 100 bars)
python3 scripts/tq_cli.py klines CFFEX.IF2601 --duration 60 --length 100

# Get tick data (100 ticks)
python3 scripts/tq_cli.py ticks DCE.a2601 --length 100
```

### Installation

```bash
# Make the script executable
chmod +x scripts/tq_cli.py

# Optionally, create an alias for convenience
alias tq='python3 /path/to/tianqing-data/scripts/tq_cli.py'
```

## Core Capabilities

### 1. Real-Time Quotes

Fetch current market data for any futures contract:

```bash
python3 scripts/tq_cli.py quote SHFE.rb2601
python3 scripts/tq_cli.py quote CFFEX.IF2601
python3 scripts/tq_cli.py quote DCE.a2601
```

Returns current price, bid/ask spreads (5 levels), volume, open interest, and daily limits in JSON format.

**See:** [API Reference - Real-time Quotes](references/api_reference.md#1-real-time-quotes)

---

### 2. K-Line Historical Data

Retrieve candlestick data at various intervals using duration in seconds:

```bash
# 1-minute candles (60 seconds)
python3 scripts/tq_cli.py klines SHFE.rb2601 --duration 60 --length 100

# 5-minute candles (300 seconds)
python3 scripts/tq_cli.py klines CFFEX.IF2601 --duration 300 --length 50

# Hourly candles (3600 seconds)
python3 scripts/tq_cli.py klines DCE.a2601 --duration 3600 --length 24

# Daily candles (86400 seconds)
python3 scripts/tq_cli.py klines SHFE.rb2601 --duration 86400 --length 30
```

Returns OHLC (open, high, low, close) data with volume and open interest.

**Duration values:**
- 1 minute = 60
- 5 minutes = 300
- 15 minutes = 900
- 1 hour = 3600
- 1 day = 86400

**See:** [API Reference - K-Line Data](references/api_reference.md#2-k-line-data)

---

### 3. Tick Sequences

Get granular tick-level transaction data for detailed market analysis:

```bash
# Get 100 latest ticks
python3 scripts/tq_cli.py ticks SHFE.rb2601 --length 100

# Get 500 ticks
python3 scripts/tq_cli.py ticks CFFEX.IF2601 --length 500

# Get 5000 ticks (max 8000)
python3 scripts/tq_cli.py ticks DCE.a2601 --length 5000
```

Returns individual tick prices, volumes, bid/ask spreads (5 levels), and transaction data.

**See:** [API Reference - Tick Data](references/api_reference.md#3-tick-sequence-data)

---

## Configuration

### API Authentication

Set your API key as an environment variable:

```bash
export TQ_API_KEY="your_api_key_here"
python3 scripts/tq_cli.py quote SHFE.rb2601
```

Or pass it directly to each command:

```bash
python3 scripts/tq_cli.py --api-key "your_api_key_here" quote SHFE.rb2601
```

### Supported Exchanges & Symbols

| Exchange | Code | Common Symbols | Examples |
|----------|------|----------------|----------|
| Shanghai Futures Exchange | SHFE | rb (rebar), cu (copper), al (aluminum), au (gold), ag (silver) | SHFE.rb2601, SHFE.cu2601 |
| Dalian Commodity Exchange | DCE | a (soybeans), m (soybean meal), l (plastic), pp (polypropylene) | DCE.a2601, DCE.m2601 |
| China Financial Futures Exchange | CFFEX | IF (CSI 300), IC (CSI 500), IH (SSE 50), T (10Y bond), TF (5Y bond) | CFFEX.IF2601, CFFEX.IC2601 |
| Zhengzhou Commodity Exchange | CZCE | CF (cotton), SR (sugar), TA (PTA), MA (methanol) | CZCE.CF601, CZCE.SR601 |
| Shanghai International Energy Exchange | INE | sc (crude oil), lu (low sulfur fuel oil) | INE.sc2601, INE.lu2601 |

**Symbol Format:** `{EXCHANGE}.{SYMBOL}{CONTRACT_MONTH}`
- Example: `SHFE.rb2601` = Shanghai Futures Exchange, Rebar, January 2026 contract

See full list in [API Reference - Common Symbols](references/api_reference.md#common-futures-symbols)

---

## Examples

### Analyze Recent Price Trends
```bash
# Get 30 daily candles for rebar
python3 scripts/tq_cli.py klines SHFE.rb2601 --duration 86400 --length 30
```

### Monitor Intraday Volatility
```bash
# Get 100 15-minute candles for CSI 300 index futures
python3 scripts/tq_cli.py klines CFFEX.IF2601 --duration 900 --length 100
```

### Check Current Market Activity
```bash
python3 scripts/tq_cli.py quote SHFE.rb2601
python3 scripts/tq_cli.py quote CFFEX.IF2601
python3 scripts/tq_cli.py quote DCE.a2601
```

### Study Tick-Level Activity
```bash
# Get 1000 ticks for detailed analysis
python3 scripts/tq_cli.py ticks SHFE.rb2601 --length 1000
```

### Compare Multiple Contracts
```bash
# Get quotes for multiple contracts
python3 scripts/tq_cli.py quote CFFEX.IF2601  # CSI 300
python3 scripts/tq_cli.py quote CFFEX.IC2601  # CSI 500
python3 scripts/tq_cli.py quote CFFEX.IH2601  # SSE 50
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
  - Example: `python3 scripts/tq_cli.py quote SHFE.rb2601`
  
- `klines <symbol> [--duration] [--length]` - Get K-line data
  - `--duration`: Period in seconds (default: 60)
  - `--length`: Number of bars (default: 100, max: 8000)
  - Example: `python3 scripts/tq_cli.py klines SHFE.rb2601 --duration 300 --length 50`
  
- `ticks <symbol> [--length]` - Get tick data
  - `--length`: Number of ticks (default: 100, max: 8000)
  - Example: `python3 scripts/tq_cli.py ticks SHFE.rb2601 --length 500`

**Global Options:**
- `--api-key` - EasyFut API key (or use TQ_API_KEY env var)

**Symbol Format:** All symbols must include exchange prefix (e.g., `SHFE.rb2601`, `CFFEX.IF2601`)

---

## Advanced Reference

For detailed API documentation including:
- Complete parameter specifications and response formats
- All supported exchanges and contract symbols
- Duration constants and interval calculations
- Error handling and response codes
- Data limits and constraints

See: [API Reference Documentation](references/api_reference.md)

## Related Documentation

- [API Reference](references/api_reference.md) - Complete API endpoint documentation
- [Usage Guide](USAGE.md) - Detailed usage examples and best practices
- [Test Report](TEST_REPORT.md) - API testing results and validation
