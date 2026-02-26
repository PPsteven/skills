# EasyFut API Reference

## Overview

TQ Skill provides access to China futures data from EasyFut API with three main endpoints:

1. **Real-time Quotes** - Current market prices and trading data
2. **K-line Data** - Candlestick historical data at various intervals
3. **Tick Sequences** - Granular tick-level transaction data

Base URL: `http://47.115.228.20:8888`

## Authentication

All API calls support optional API key authentication:

- Set the `TQ_API_KEY` environment variable, or
- Pass `--api-key` flag to CLI commands

## Endpoints

### 1. Real-time Quotes

**Endpoint:** `GET /quote/{symbol}`

Get current trading data for a futures contract (implicit subscription).

**CLI Usage:**
```bash
python3 tq_cli.py quote SHFE.rb2601
```

**Parameters:**
- `symbol` (required): Futures contract symbol with exchange prefix
  - Format: `{EXCHANGE}.{SYMBOL}`
  - Example: `SHFE.rb2601`, `CFFEX.IF2601`, `DCE.A2601`

**Examples:**
```bash
python3 tq_cli.py quote SHFE.rb2601
python3 tq_cli.py quote CFFEX.IF2601
python3 tq_cli.py quote DCE.A2601
```

**Response Fields:**
- `datetime`: Quote time (Beijing time)
- `last_price`: Latest price
- `bid_price1` - `bid_price5`: Bid prices (5 levels)
- `bid_volume1` - `bid_volume5`: Bid volumes (5 levels)
- `ask_price1` - `ask_price5`: Ask prices (5 levels)
- `ask_volume1` - `ask_volume5`: Ask volumes (5 levels)
- `open`, `high`, `low`, `close`: OHLC prices
- `volume`: Trading volume
- `open_interest`: Open interest
- `upper_limit`, `lower_limit`: Daily price limits

---

### 2. K-line Data

**Endpoint:** `GET /klines/{klines_symbol}`

Get candlestick data at specified intervals (implicit subscription).

**CLI Usage:**
```bash
python3 tq_cli.py klines SHFE.rb2601 --duration 60 --length 100
```

**Parameters:**
- `symbol` (required): Futures contract symbol with exchange prefix
- `duration` (optional, default: 60): K-line period in seconds
  - Common values: `60` (1min), `300` (5min), `900` (15min), `3600` (1hour), `86400` (1day)
  - Note: For periods >= daily, must be multiples of 86400, max 28 days (86400*28)
- `length` (optional, default: 100): Number of bars to retrieve (max 8000)

**Format in URL:** `{symbol}_{duration_seconds}_{data_length}`

**Examples:**
```bash
# Get 100 one-minute candles
python3 tq_cli.py klines SHFE.rb2601 --duration 60 --length 100

# Get 50 five-minute candles
python3 tq_cli.py klines SHFE.rb2601 --duration 300 --length 50

# Get 10 daily candles
python3 tq_cli.py klines SHFE.rb2601 --duration 86400 --length 10

# Get 5 hourly candles
python3 tq_cli.py klines CFFEX.IF2601 --duration 3600 --length 5
```

**Response Fields (per bar):**
- `datetime`: K-line start time (nanoseconds since epoch)
- `open`: Opening price
- `high`: Highest price in period
- `low`: Lowest price in period
- `close`: Closing price
- `volume`: Trading volume
- `open_oi`: Open interest at start
- `close_oi`: Open interest at end
- `duration`: Period in seconds
- `symbol`: Contract symbol

---

### 3. Tick Sequence Data

**Endpoint:** `GET /ticks/{ticks_symbol}`

Get granular tick-level transaction data (implicit subscription).

**CLI Usage:**
```bash
python3 tq_cli.py ticks SHFE.rb2601 --length 100
```

**Parameters:**
- `symbol` (required): Futures contract symbol with exchange prefix
- `length` (optional, default: 100): Number of ticks to retrieve (max 8000)

**Format in URL:** `{symbol}_{data_length}`

**Examples:**
```bash
# Get 100 latest ticks
python3 tq_cli.py ticks SHFE.rb2601 --length 100

# Get 50 ticks
python3 tq_cli.py ticks CFFEX.IF2601 --length 50

# Get 5000 ticks
python3 tq_cli.py ticks DCE.A2601 --length 5000
```

**Response Fields (per tick):**
- `datetime`: Tick time (nanoseconds since epoch)
- `last_price`: Last traded price
- `bid_price1` - `bid_price5`: Bid prices (5 levels)
- `bid_volume1` - `bid_volume5`: Bid volumes (5 levels)
- `ask_price1` - `ask_price5`: Ask prices (5 levels)
- `ask_volume1` - `ask_volume5`: Ask volumes (5 levels)
- `average`: Daily average price
- `highest`, `lowest`: Daily high/low
- `volume`: Cumulative trading volume
- `amount`: Cumulative trading amount
- `open_interest`: Current open interest

---

## Supported Exchanges

| Exchange | Code | Examples |
|----------|------|----------|
| Shanghai Futures Exchange | SHFE | rb (rebar), cu (copper), al (aluminum) |
| Dalian Commodity Exchange | DCE | a (soybeans), m (soybean meal), l (plastic) |
| China Financial Futures Exchange | CFFEX | IF (CSI 300), IC (CSI 500), IH (SSE 50) |

---

## Common Futures Symbols

```
Index Futures (CFFEX):
- CFFEX.IF2601: CSI 300 Index
- CFFEX.IC2601: CSI 500 Index
- CFFEX.IH2601: SSE 50 Index

Metal Futures (SHFE):
- SHFE.cu2601: Copper
- SHFE.al2601: Aluminum
- SHFE.rb2601: Rebar (Steel)

Agricultural Futures (DCE):
- DCE.a2601: Soybeans
- DCE.m2601: Soybean Meal
- DCE.y2601: Soybean Oil
```

---

## Duration Constants (in seconds)

```
1 minute = 60
5 minutes = 300
15 minutes = 900
30 minutes = 1800
1 hour = 3600
4 hours = 14400
1 day = 86400
1 week = 604800 (7 * 86400)
```

---

## Error Response

When API returns an error:
```json
{
  "code": 10000,
  "data": { ... },
  "msg": "操作成功！"
}
```

- `code`: 10000 indicates success
- `data`: Response data (empty for errors)
- `msg`: Message in Chinese

---

## Usage Examples

### Get Real-time Quote
```bash
python3 tq_cli.py quote SHFE.rb2601
python3 tq_cli.py quote CFFEX.IF2601
```

### Get 1-Minute Candles
```bash
python3 tq_cli.py klines SHFE.rb2601 --duration 60 --length 240
```

### Get Hourly Candles
```bash
python3 tq_cli.py klines CFFEX.IF2601 --duration 3600 --length 24
```

### Get Daily Candles
```bash
python3 tq_cli.py klines SHFE.rb2601 --duration 86400 --length 30
```

### Get Latest Tick Data
```bash
python3 tq_cli.py ticks SHFE.rb2601 --length 500
```

### Retrieve 1000 Ticks
```bash
python3 tq_cli.py ticks DCE.A2601 --length 1000
```
