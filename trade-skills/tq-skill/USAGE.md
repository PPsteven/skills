# TQ-Skill 使用指南

## 快速开始

### 安装

```bash
cd /Users/ppsteven/projects/skills/trade-skills/tq-skill
```

### 获取实时行情

```bash
python3 scripts/tq_cli.py quote SHFE.rb2601
python3 scripts/tq_cli.py quote CFFEX.IF2601
python3 scripts/tq_cli.py quote DCE.A2601
```

### 获取K线数据

```bash
# 获取100条1分钟K线
python3 scripts/tq_cli.py klines SHFE.rb2601 --duration 60 --length 100

# 获取50条5分钟K线
python3 scripts/tq_cli.py klines SHFE.rb2601 --duration 300 --length 50

# 获取10条日K线
python3 scripts/tq_cli.py klines SHFE.rb2601 --duration 86400 --length 10

# 获取24条小时K线
python3 scripts/tq_cli.py klines CFFEX.IF2601 --duration 3600 --length 24
```

### 获取Tick数据

```bash
# 获取最新100条Tick
python3 scripts/tq_cli.py ticks SHFE.rb2601 --length 100

# 获取5000条Tick
python3 scripts/tq_cli.py ticks DCE.A2601 --length 5000
```

## 支持的合约

### 指数期货 (CFFEX)
- `CFFEX.IF2601`: 沪深300指数
- `CFFEX.IC2601`: 中证500指数
- `CFFEX.IH2601`: 上证50指数

### 黑色金属 (SHFE)
- `SHFE.rb2601`: 螺纹钢
- `SHFE.cu2601`: 铜
- `SHFE.al2601`: 铝

### 农产品 (DCE)
- `DCE.a2601`: 大豆
- `DCE.m2601`: 豆粕
- `DCE.y2601`: 豆油

## 命令参数

### quote 命令
```
python3 tq_cli.py quote <symbol>

参数:
  symbol: 合约代码（带交易所前缀）
```

### klines 命令
```
python3 tq_cli.py klines <symbol> [--duration <seconds>] [--length <bars>]

参数:
  symbol: 合约代码（带交易所前缀）
  --duration: K线周期（秒），默认60
  --length: 获取的K线数量，默认100，最大8000
```

### ticks 命令
```
python3 tq_cli.py ticks <symbol> [--length <count>]

参数:
  symbol: 合约代码（带交易所前缀）
  --length: 获取的Tick数量，默认100，最大8000
```

## 常见周期参数

| 周期 | 秒数 |
|------|------|
| 1分钟 | 60 |
| 5分钟 | 300 |
| 15分钟 | 900 |
| 30分钟 | 1800 |
| 1小时 | 3600 |
| 4小时 | 14400 |
| 1天 | 86400 |
| 1周 | 604800 |

## API认证

可选的API密钥认证：

```bash
# 方式1：设置环境变量
export TQ_API_KEY="your_api_key"
python3 scripts/tq_cli.py quote SHFE.rb2601

# 方式2：直接传参
python3 scripts/tq_cli.py --api-key "your_api_key" quote SHFE.rb2601
```

## 响应格式

所有命令都返回JSON格式的响应：

```json
{
  "code": 10000,
  "data": {
    "SHFE.rb2601": {
      "datetime": "2026-01-15 14:59:59.999500",
      "last_price": 3165.0,
      "bid_price1": 3115.0,
      "ask_price1": 3165.0,
      ...
    }
  },
  "msg": "操作成功！"
}
```

## 详细文档

更多详细信息请查看：
- `SKILL.md` - 技能概览
- `references/api_reference.md` - 完整API参考
