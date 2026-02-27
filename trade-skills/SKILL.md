---
name: trade-skills
description: Data source router for accessing Chinese financial market data. Routes users to appropriate data skill (akshare-data for stocks/bonds/funds/macro, tianqing-data for futures). Provides comprehensive data resource table showing what data each skill provides and which APIs to call.
---

# Trade Skills - Data Source Router

Router skill for managing access to multiple financial data sources. Provides a comprehensive mapping of data types to available data skills.

## Function

**Purpose:** Route users to the appropriate data skill based on their data requirements.

**How it works:**
1. User requests specific financial data
2. Identify data type and asset class from request
3. Route to corresponding data skill (see Data Resources Table below)
4. User invokes the routed skill with appropriate parameters

---

## Data Resources Table

Complete mapping of data types to data skills and APIs.

### Data Source 1: akshare-data

AKShare provides comprehensive Chinese financial market data.

| Data Type | Data Category | APIs | Use Case |
|---|---|---|---|
| **Stocks** | Equities | stock_zh_a_hist, stock_zh_a_daily | Historical daily prices, technical analysis |
| **Stock Indices** | Indices | index_zh_a_hist, index_zh_a_daily | Index performance, components |
| **Bonds** | Fixed Income | bond data APIs | Yields, credit spreads, maturity |
| **Interest Rates** | Fixed Income | interest rate APIs | LPR, deposit/loan rates, yield curves |
| **Mutual Funds** | Funds | fund_public APIs | Fund data, ratings, performance |
| **Hedge Funds** | Funds | fund_private APIs | Private fund data |
| **Commodities** | Derivatives | futures APIs, spot APIs | Commodity futures, spot prices |
| **Options** | Derivatives | option APIs | Options contracts, Greeks |
| **Forex** | FX & International | fx_rate APIs | Currency pairs, exchange rates |
| **Hong Kong Stocks** | FX & International | hk_stock APIs | Hong Kong market data |
| **GDP** | Macroeconomic | macro_china_gdp | Economic growth |
| **CPI/PPI** | Macroeconomic | macro_china_cpi | Inflation, price indices |
| **Production** | Macroeconomic | macro_china_industrial | Industrial production |
| **Energy** | Macroeconomic | energy APIs | Oil, coal, natural gas |
| **Technical Indicators** | Tools | tool APIs | Moving averages, RSI, MACD |
| **Bank Data** | Specialized | bank_* APIs | Regulatory data, penalties |

**Skill Reference:** [akshare-data](../akshare-data/SKILL.md)

---

### Data Source 2: tianqing-data

Tianqing (天晴) provides China futures real-time and historical data via EasyFut API.

| Data Type | Data Category | APIs | Use Case |
|---|---|---|---|
| **Real-Time Quotes** | Futures | quote | Current prices, five-level order book |
| **Daily High/Low** | Futures | quote | Daily price limits, day's range |
| **K-Line 1m** | Futures | klines --duration 60 | 1-minute candles for intraday trading |
| **K-Line 5m** | Futures | klines --duration 300 | 5-minute candles for short-term analysis |
| **K-Line 15m** | Futures | klines --duration 900 | 15-minute candles |
| **K-Line 1h** | Futures | klines --duration 3600 | Hourly candles for day trading |
| **K-Line 1d** | Futures | klines --duration 86400 | Daily candles for swing trading |
| **K-Line 1w** | Futures | klines --duration 604800 | Weekly candles for trend analysis |
| **Tick Data** | Futures | ticks | Granular transaction records |
| **Open Interest** | Futures | quote | Current open interest |

**Supported Exchanges & Contracts:**
- **SHFE** (Shanghai): Rebar (rb), Copper (cu), Aluminum (al), Rubber (ru)
- **CFFEX** (China Financial Futures): CSI 300 (IF), CSI 500 (IC), Shanghai 50 (IH)
- **DCE** (Dalian): Soybeans (a), Soybean Meal (m), Soybean Oil (y), Plastics (l)

**Skill Reference:** [tianqing-data](../tianqing-data/SKILL.md)

---

## Quick Decision Tree

**Need Chinese stocks or stock indices?** → Use `akshare-data` - stock_zh_a_hist

**Need Chinese bonds or interest rates?** → Use `akshare-data` - bond APIs, interest rate APIs

**Need Chinese funds?** → Use `akshare-data` - fund_public or fund_private APIs

**Need macroeconomic indicators (GDP, CPI, etc.)?** → Use `akshare-data` - macro_china_* APIs

**Need China futures real-time quotes?** → Use `tianqing-data` - quote command

**Need China futures K-lines for technical analysis?** → Use `tianqing-data` - klines command with --duration parameter

**Need China futures tick-level data?** → Use `tianqing-data` - ticks command

---

## Usage Pattern

1. Identify data requirement from user request
2. Locate data type in Data Resources Table above
3. Note the skill name and API to use
4. Invoke the skill with appropriate parameters
5. Return results to user

Example: User wants "daily prices for stock 000001"
- Step 1: Identified as Chinese stock data
- Step 2: Found in akshare-data table → stock_zh_a_hist API
- Step 3: Invoke akshare-data skill
- Step 4: Command: `python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131`
