---
name: trade-skills
description: Comprehensive guide for accessing financial market data and trading tools. Provides navigation across multiple financial data sources (akshare-skill, TuShare, Yahoo Finance, etc.) to help users select the right data provider for their needs. Use when Claude needs to guide users on acquiring trading data, understanding data source capabilities, or routing requests to specialized financial skills.
---

# Trade Skills

## Overview

Trade Skills is a comprehensive guide for accessing financial market data and trading tools. It helps users navigate the landscape of available financial data sources, understand their capabilities, and route their specific data requests to the appropriate specialized skill or tool.

## Data Source Navigation

### Chinese Market Data

**Primary Source: AKShare**
- **Coverage:** A/H shares, indices, futures, options, funds, bonds, forex, macroeconomic indicators
- **When to use:** Need comprehensive Chinese market data with historical and real-time coverage
- **Specialty:** Futures, commodities, bonds, macroeconomic data
- **Usage:** See [akshare-skill](akshare-skill/SKILL.md)

**Alternative: TuShare** (supplementary source)
- **Coverage:** Stock quotes, fundamentals, indices, fund data
- **When to use:** Need alternative data verification or specific fundamentals not in AKShare
- **Specialty:** Financial statements, company fundamentals

### International Market Data

**Yahoo Finance** (supplementary source)
- **Coverage:** Global stocks, ETFs, indices, options, forex
- **When to use:** Need US/international market data or cross-market analysis
- **Specialty:** Real-time quotes, technical analysis

**Alternative Crypto Data** (supplementary source)
- **Coverage:** Bitcoin, Ethereum, and other cryptocurrencies
- **When to use:** Need crypto trading data or blockchain metrics

## Quick Reference

| **Data Type** | **Primary Source** | **Use Case** |
|---|---|---|
| Chinese A-shares | akshare-skill | Historical data, technical analysis |
| Chinese futures | akshare-skill | Commodities, financial futures |
| Chinese funds | akshare-skill | Mutual funds, ETFs |
| Chinese bonds | akshare-skill | Government, corporate bonds |
| Chinese macro | akshare-skill | GDP, inflation, economic indicators |
| US stocks | Yahoo Finance | International comparison, cross-market analysis |
| Crypto | Crypto APIs | Digital asset trading |
| Company fundamentals | TuShare | Financial statements, ratios |

## How to Choose a Data Source

1. **Identify your market:** Chinese domestic? International? Crypto?
2. **Identify your asset class:** Stocks? Futures? Bonds? Funds? Macroeconomic data?
3. **Check the Quick Reference table above** for the best match
4. **Use the appropriate specialized skill** for detailed API documentation and usage examples

## Using AKShare

AKShare provides the most comprehensive coverage of Chinese financial market data. For detailed documentation on all available APIs, parameters, and examples:

```
→ Use the akshare-skill to access:
  - Historical stock data (stock_zh_a_hist)
  - Index data and components
  - Futures contracts and open interest
  - Fund information and performance
  - Bond data (government, corporate, municipal)
  - Macroeconomic indicators (GDP, CPI, production)
  - Foreign exchange and currency data
```

Common usage pattern:
```bash
python3 scripts/akshare_cli.py <function_name> <parameters>
```

Example:
```bash
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131
```

## Data Integration Workflow

When working with multiple data sources:

1. **Fetch data** from appropriate sources using specialized skills
2. **Normalize** timestamps and symbols across sources (Chinese vs. international naming)
3. **Align** time zones if mixing Chinese and international data
4. **Combine** data for cross-market analysis

Example: Comparing Chinese A-shares with US ADRs requires:
- AKShare for Chinese market data
- Yahoo Finance for US market data
- Symbol mapping between markets
- Time zone alignment (Shanghai vs. New York)

## Getting Started

**For Chinese market data:**
→ Read the [akshare-skill documentation](akshare-skill/SKILL.md)

**For international market data:**
→ Use Yahoo Finance API documentation

**For trading analysis:**
→ Combine data from multiple sources following the Data Integration Workflow above

---

**Note:** This is a navigation skill. For detailed API documentation, parameter tables, and code examples, refer to the specialized skills for each data source.
