# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains three complementary financial data skills for accessing Chinese financial market data:

1. **akshare-data** - Comprehensive market data (stocks, bonds, funds, indices, macroeconomic indicators)
2. **tianqin-data** - Real-time futures market data (quotes, K-lines, ticks) via EasyFut API
3. **trade-skills** - Router skill that directs user requests to the appropriate data skill
4. **github-repo-init** - Skill for initializing GitHub repositories

## Architecture

### Three-Tier Structure

```
skills/
├── akshare-data/          # Data skill for spot markets, stocks, bonds, funds
│   ├── scripts/           # CLI wrapper (akshare_cli.py)
│   ├── tests/             # pytest tests for CLI functionality
│   └── references/        # API documentation organized by asset class
│
├── tianqin-data/          # Data skill for China futures
│   ├── scripts/           # CLI wrapper (tq_cli.py)
│   ├── references/        # API reference documentation
│   └── TEST_REPORT.md     # Test results and validation
│
├── trade-skills/          # Router skill
│   ├── SKILL.md           # Routing rules and data mapping table
│   └── TEST.md            # Routing test cases
│
└── github-repo-init/      # GitHub initialization skill
    ├── SKILL.md           # Skill documentation
    └── README.md          # Usage guide
```

### Data Flow

```
User Request
    ↓
[trade-skills] Routes request to correct skill
    ↓
[akshare-data] OR [tianqin-data]
    ↓
CLI wrapper (akshare_cli.py or tq_cli.py)
    ↓
Returns JSON data
```

### Skill Responsibilities

- **trade-skills**: Maps user requests to data types; routes to akshare-data or tianqin-data based on data category
- **akshare-data**: Provides historical and spot market data (stocks, bonds, funds, macroeconomic, commodities)
- **tianqin-data**: Provides real-time and historical futures market data (quotes, K-lines, ticks)

## Development Commands

### Testing

```bash
# Run all tests for akshare-data
cd akshare-data && python3 -m pytest tests/

# Run specific test file
python3 -m pytest tests/test_cli.py -v

# Run tests for a specific function
python3 -m pytest tests/test_stock_cli.py::test_function_name -v
```

### CLI Commands

#### AKShare Data Skill

```bash
# Stock historical data
python3 akshare-data/scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131

# Macroeconomic data
python3 akshare-data/scripts/akshare_cli.py macro_china_gdp --format json

# Export to CSV
python3 akshare-data/scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131 --format csv > output.csv

# Help
python3 akshare-data/scripts/akshare_cli.py --help
```

#### TianQin Futures Data Skill

```bash
# Real-time quote (requires TQ_API_KEY environment variable)
export TQ_API_KEY="your_key"
python3 tianqin-data/scripts/tq_cli.py quote SHFE.rb2601

# K-line data (1-minute candles, 100 bars)
python3 tianqin-data/scripts/tq_cli.py klines CFFEX.IF2601 --duration 60 --length 100

# Tick data (100 ticks)
python3 tianqin-data/scripts/tq_cli.py ticks DCE.a2601 --length 100
```

### Common Duration Values for K-Lines

- 60 seconds = 1-minute candle
- 300 seconds = 5-minute candle
- 900 seconds = 15-minute candle
- 3600 seconds = 1-hour candle
- 86400 seconds = 1-day candle
- 604800 seconds = 1-week candle

## Testing

### Skill Installation & Testing

Before testing skills, install them:

```bash
# Clean old skills
rm -rf ~/.agents/skills/{akshare-data,tianqin-data,trade-skills}

# Install from this repository
npx skills add https://github.com/PPsteven/skills
```

### Trade-Skills Routing Tests

See `trade-skills/TEST.md` for complete routing test cases. Key test scenarios:

1. **Spot price request** → Routes to akshare-data
2. **Futures real-time quote** → Routes to tianqin-data (quote command)
3. **Futures K-line analysis** → Routes to tianqin-data (klines command with --duration)
4. **Stock/bond/fund request** → Routes to akshare-data
5. **Macroeconomic data** → Routes to akshare-data

### AKShare CLI Tests

```bash
cd akshare-data
python3 -m pytest tests/test_cli.py -v
python3 -m pytest tests/test_stock_cli.py -v
python3 -m pytest tests/test_bank_cli.py -v
```

## Key Files & Patterns

### API Documentation Structure

Each skill's API reference follows this pattern:

- **API name** - Function identifier (e.g., `stock_zh_a_hist`)
- **Description** - What data it provides
- **Input parameters** - With types and usage
- **Output parameters** - DataFrame columns
- **Code example** - Working code sample
- **Data sample** - Sample output

### CLI Wrapper Pattern

Both akshare_cli.py and tq_cli.py follow similar patterns:

1. Accept command and parameters from CLI
2. Call the underlying Python library
3. Format output as JSON (default), pretty-printed tables, or CSV
4. Handle errors gracefully

### Exchange Prefix Format (TianQin)

All futures symbols require exchange prefix:
- `SHFE.rb2601` - Shanghai Futures Exchange, Rebar, Jan 2026
- `CFFEX.IF2601` - China Financial Futures Exchange, CSI 300, Jan 2026
- `DCE.a2601` - Dalian Commodity Exchange, Soybeans, Jan 2026

## Important Notes

### Dependencies

- **akshare-data** requires `akshare` Python package
- **tianqin-data** requires TQ_API_KEY environment variable for authentication
- All skills return JSON by default for API integration

### Output Formats

- `--format json` - JSON (default, best for programmatic use)
- `--format pretty` - Human-readable tables
- `--format csv` - CSV (for export/complex analysis)

### Data Categories Mapping (trade-skills routing)

**Route to akshare-data for:**
- Stocks, indices, bonds, interest rates
- Mutual funds, private funds
- Commodities spot prices
- Options, forex, Hong Kong stocks
- Macroeconomic data (GDP, CPI, industrial production, energy)
- Technical indicators, bank data

**Route to tianqin-data for:**
- Futures real-time quotes
- Futures K-line data (all intervals)
- Futures tick data
- Only for Chinese futures contracts on SHFE, DCE, CFFEX, CZCE, INE exchanges

## References

- **akshare-data**: See `akshare-data/SKILL.md` for complete API reference
- **tianqin-data**: See `tianqin-data/SKILL.md` for EasyFut API documentation
- **trade-skills**: See `trade-skills/SKILL.md` for routing rules and `trade-skills/TEST.md` for test cases
- **Main README**: `README.md` for project overview
