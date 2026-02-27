---
name: trade-skills
description: Router for accessing financial market data and trading tools. Routes users to appropriate specialized skill based on their data needs. Use when users request any financial market data or trading information.
---

# Trade Skills - Data Source Router

Choose the appropriate skill based on the data type you need.

## Data Source Selection

### Chinese Stocks, Indices, Bonds, Funds, Macro Data → **akshare-skill**

**akshare-skill** provides comprehensive Chinese financial market data via AKShare API.

Available data:
- **Equities & Indices** - A/B shares, daily snapshots, sector data, indices, components
- **Fixed Income** - Bonds (government, corporate, municipal), interest rates, yield curves
- **Derivatives** - Futures contracts, open interest, delivery data, options, Greeks
- **Funds** - Mutual funds, hedge funds, fund ratings, QDII products
- **Forex & International** - FX, currency pairs, Hong Kong stocks, Singapore data
- **Macroeconomic** - GDP, CPI, inflation, industrial production, energy prices
- **Specialized** - Bank data, events, corporate actions, technical indicators, articles

**Usage:** See [akshare-skill](../akshare-skill/SKILL.md)

### China Futures Data (Real-Time, K-Line, Ticks) → **tq-skill**

**tq-skill** provides China futures data via EasyFut API.

Available data:
- **Real-Time Quotes** - Five-level order book, latest price, daily high/low, price limits
- **K-Line Data** - Historical candles: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w
- **Tick Data** - Individual transaction records with timestamps, price, volume

Supported exchanges:
- **SHFE** (Shanghai Futures Exchange) - Rebar, copper, aluminum, rubber, etc.
- **CFFEX** (China Financial Futures Exchange) - CSI 300, CSI 500, Shanghai 50
- **DCE** (Dalian Commodity Exchange) - Soybeans, soybean meal, oil, plastics, coals

**Usage:** See [tq-skill](../tq-skill/SKILL.md)

## Quick Reference

| Data Type | Skill | Use Case |
|---|---|---|
| Chinese stocks, indices | akshare-skill | Historical daily prices, technical analysis, fundamentals |
| Chinese bonds | akshare-skill | Yields, credit spreads, maturity data |
| Chinese funds | akshare-skill | Mutual funds, hedge funds, ETFs, QDII products |
| Macroeconomic data | akshare-skill | GDP, CPI, inflation, industrial production |
| China futures real-time | tq-skill | Current prices, order book, daily limits |
| China futures K-lines | tq-skill | Historical candles for technical analysis |
| China futures ticks | tq-skill | Granular transaction records for detailed analysis |
