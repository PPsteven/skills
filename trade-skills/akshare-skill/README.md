# Trade Skills

本项目包含金融数据获取和处理的相关工具，主要围绕 [AKShare](https://github.com/akfamily/akshare) 库进行扩展，提供 CLI 工具和 API 参考文档。

## 项目结构

```
trade-skills/
├── akshare/              # AKShare 官方 Python 库源码
│   ├── akshare/          # 核心库代码
│   ├── docs/             # 官方文档
│   ├── tests/            # 测试用例
│   └── README.md         # AKShare 官方说明
├── akshare-skill/        # 本项目扩展
│   ├── CLI_DESIGN.md     # CLI 工具设计文档
│   ├── SKILL.md          # Skill 使用说明
│   ├── QUICK_START.md    # 快速开始指南
│   ├── scripts/          # CLI 脚本
│   │   └── akshare_cli.py
│   ├── references/       # API 参考文档
│   │   ├── stock.md
│   │   ├── fund/
│   │   ├── futures.md
│   │   ├── macro.md
│   │   └── ...
│   └── tests/            # 测试用例
└── docs/                 # 项目计划文档
    └── plans/
```

## 主要功能

### AKShare CLI 工具

通过命令行直接获取中国金融市场数据，支持多种输出格式：

```bash
# 获取股票历史数据 (JSON 格式，默认)
python3 akshare-skill/scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131

# 获取 CSV 格式（适合复杂分析）
python3 akshare-skill/scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131 --format csv > stock_data.csv

# 获取人类可读的表格格式
python3 akshare-skill/scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131 --format pretty
```

### 支持的数据类别

- **股票数据**: A/B 股历史行情、日常快照、行业数据
- **指数数据**: 股票指数、指数成分、性能数据
- **基金数据**: 公募基金、私募基金、基金评级
- **期货数据**: 期货合约、持仓数据、交割数据
- **债券数据**: 国债、企业债、可转债
- **外汇数据**: 汇率、货币对
- **宏观经济数据**: GDP、CPI、工业生产、消费数据
- **港股/新加坡数据**: 港股、新加坡市场数据
- 以及更多...

详细 API 文档请参考 [akshare-skill/references/](akshare-skill/references/) 目录。

## 快速开始

### 环境要求

- Python 3.8+
- akshare 库

### 安装依赖

```bash
pip install akshare
```

### 使用 CLI 工具

```bash
# 方式一：直接运行 Python 脚本
python3 akshare-skill/scripts/akshare_cli.py <function_name> [options]

# 方式二：使用可执行脚本（需添加执行权限）
chmod +x akshare-skill/scripts/akshare-cli
./akshare-skill/scripts/akshare-cli <function_name> [options]
```

### 输出格式

| 格式 | 说明 | 使用场景 |
|------|------|----------|
| `json` | JSON 格式（默认） | API 集成、程序处理 |
| `pretty` | 人类可读表格 | 快速查看数据 |
| `csv` | CSV 格式 | 复杂分析、导入 Excel |

## API 参考

详细 API 文档位于 [akshare-skill/references/](akshare-skill/references/) 目录：

- [股票数据](akshare-skill/references/stock.md)
- [基金数据](akshare-skill/references/fund/)
- [期货数据](akshare-skill/references/futures.md)
- [宏观经济](akshare-skill/references/macro.md)
- [外汇数据](akshare-skill/references/fx.md)
- [港股数据](akshare-skill/references/qhkc/)

## 相关文档

- [CLI 设计文档](akshare-skill/CLI_DESIGN.md)
- [Skill 使用说明](akshare-skill/SKILL.md)
- [快速开始指南](akshare-skill/QUICK_START.md)
- [AKShare 官方文档](https://akshare.akfamily.xyz/)

## 许可证

本项目基于 MIT 许可证。AKShare 数据仅供学术研究参考，不构成投资建议。

## 致谢

- [AKShare](https://github.com/akfamily/akshare) - 优雅简洁的 Python 金融数据接口库
- 东方财富网、新浪财经、金十数据等数据源
