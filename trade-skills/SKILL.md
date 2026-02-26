---
name: trade-skills
description: Router for accessing financial market data and trading tools. Routes users to the appropriate specialized skill based on their data needs - akshare-skill for Chinese stocks/futures/bonds/macro, tq-skill for China futures real-time/K-line/tick data, or other sources. Use when users request financial market data or trading information.
---

# Trade Skills

Umbrella skill for accessing financial market data. Route to the appropriate sub-skill based on data type and source.

## Available Skills

| **Skill** | **Data Type** | **Coverage** |
|---|---|---|
| [akshare-skill](akshare-skill/SKILL.md) | Chinese stocks, funds, bonds, macro | A/H shares, indices, options, forex, economic indicators |
| [tq-skill](tq-skill/SKILL.md) | China futures data | Real-time quotes, K-line (1m-1w), tick sequences; SHFE/DCE/CFFEX |

## Quick Routing

**Need Chinese stocks, funds, bonds, or macro data?** → Use `akshare-skill`

**Need China futures real-time quotes, K-lines, or tick data?** → Use `tq-skill`

See the respective skill documentation for detailed API usage, parameters, and examples.
