---
name: trade-skills
description: Router for accessing financial market data and trading tools. Routes users to appropriate specialized skill based on their data needs - akshare-skill for Chinese stocks/indices/bonds/funds/forex/macro, tq-skill for China futures real-time data/K-lines/ticks. Use when users request any financial market data or trading information.
---

# Trade Skills

Umbrella skill for accessing financial market data from multiple sources. Route to the appropriate sub-skill based on data type and source needed.

## Available Skills

### 1. akshare-skill
Comprehensive Chinese financial market data via AKShare API.

**Equities & Indices:**
- A/B shares (stocks), daily snapshots, sector data, board listings
- Stock indices, index components, performance data

**Fixed Income:**
- Government bonds, corporate bonds, municipal bonds
- Interest rates (LPR, deposit/loan rates, yield curves)

**Derivatives:**
- Futures contracts, open interest, delivery data
- Options contracts, Greeks, implied volatility

**Funds & Alternative Assets:**
- Mutual funds (public funds), hedge funds (private funds), fund ratings, fund fundamentals
- Commodities, spot trading data
- QDII (Qualified Domestic Institutional Investor) products

**Forex & International:**
- Foreign exchange (FX), currency pairs, exchange rates
- Hong Kong stocks, Singapore data (QHKC)

**Macroeconomic Data:**
- GDP, CPI, inflation, industrial production, consumer spending
- Currency data, forex indicators
- Oil, coal, natural gas prices
- Central bank rates, yield curves

**Specialized Data:**
- Bank data, regulatory data, administrative penalties
- Events & corporate actions, news
- Technical indicators, analysis tools
- Financial research articles

**Usage:** See [akshare-skill](akshare-skill/SKILL.md)

### 2. tq-skill
China futures real-time data and historical data via EasyFut API.

**Real-Time Data:**
- Five-level order book (bid/ask prices and volumes)
- Latest price, daily high/low, open interest, price limits

**K-Line Data (Historical):**
- Multiple timeframes: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w
- Open, high, low, close, volume, open interest

**Tick Data (Granular):**
- Individual transaction records with timestamps
- Price, volume, bid/ask levels

**Exchanges & Contracts:**
- SHFE (Shanghai): Rebar, copper, aluminum, rubber, etc.
- CFFEX (China Financial Futures): CSI 300, CSI 500, Shanghai 50 indices
- DCE (Dalian): Soybeans, soybean meal, soybean oil, plastics, coals, etc.

**Usage:** See [tq-skill](tq-skill/SKILL.md)

## Quick Decision Tree

**Need Chinese stocks or indices data?** → `akshare-skill`
- Historical daily prices, technical analysis, fundamentals, components

**Need Chinese bonds data?** → `akshare-skill`
- Government/corporate/municipal bond yields and data

**Need Chinese funds data?** → `akshare-skill`
- Mutual funds, hedge funds, ETFs, QDII products

**Need macroeconomic indicators?** → `akshare-skill`
- GDP, CPI, inflation, industrial production, economic data

**Need China futures real-time quotes?** → `tq-skill`
- Current prices with five-level order book, daily limits

**Need China futures historical K-line data?** → `tq-skill`
- 1m to weekly candles for technical analysis

**Need China futures tick-level data?** → `tq-skill`
- Individual transaction records for detailed market analysis

See the respective skill documentation for API usage, parameters, and examples.
