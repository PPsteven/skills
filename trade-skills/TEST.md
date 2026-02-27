# Trade-Skills 技能测试指南

## 技能说明

`trade-skills` 是一个数据源路由技能，用于将用户的金融数据请求路由到正确的数据技能：
- **akshare-data**：提供股票、债券、基金、宏观经济等数据
- **tianqin-data**：提供期货实时行情、K线、Tick数据等

## 测试流程

### 1. 清理旧技能
删除 `~/.agents/skills` 目录下的旧技能：
```bash
cd ~/.agents/skills
rm -rf akshare-data tianqin-data trade-skills
```

### 2. 安装技能
使用 npx 从 GitHub 仓库安装技能：
```bash
npx skills add https://github.com/PPsteven/skills
```

此命令会：
- 安装三个技能：`akshare-data`、`tianqin-data`、`trade-skills`
- Global 级
- Cline, Claude Code, OpenClaw
- 软连接

### 3. 测试用例

以下测试用例专门测试 `trade-skills` 的路由功能：

#### 测试用例 1：获取生猪现货价格
**用户请求：**
```
获取生猪现货价格
```

**预期行为：**
- `trade-skills` 识别为现货价格数据
- 路由到 `akshare-data` 技能
- 使用 spot 相关 API 获取生猪现货价格

**验证点：**
- ✅ 正确识别数据类型（现货价格）
- ✅ 路由到 akshare-data
- ✅ 返回生猪现货价格数据

---

#### 测试用例 2：获取铁矿石期货价格
**用户请求：**
```
获取铁矿石期货价格
```

**预期行为：**
- `trade-skills` 识别为期货价格数据
- 可能路由到 `akshare-data`（历史数据）或 `tianqin-data`（实时行情）
- 根据用户需求选择合适的数据源

**验证点：**
- ✅ 正确识别数据类型（期货价格）
- ✅ 路由到合适的数据技能
- ✅ 返回铁矿石期货价格数据

---

#### 测试用例 3：铁矿石5分钟技术分析
**用户请求：**
```
铁矿石5分钟技术分析
```

**预期行为：**
- `trade-skills` 识别为期货K线数据（5分钟周期）
- 路由到 `tianqin-data` 技能
- 使用 klines 命令，duration=300（5分钟）
- 获取铁矿石期货5分钟K线数据

**验证点：**
- ✅ 正确识别数据类型（期货K线）
- ✅ 正确识别时间周期（5分钟）
- ✅ 路由到 tianqin-data
- ✅ 返回5分钟K线数据用于技术分析

---

## 路由决策验证

测试 `trade-skills` 的核心功能是验证其路由决策是否正确：

| 数据请求 | 应路由到 | 使用的API/命令 |
|---------|---------|--------------|
| 股票价格 | akshare-data | stock_zh_a_hist |
| 债券数据 | akshare-data | bond APIs |
| 基金数据 | akshare-data | fund_public/fund_private |
| 宏观经济 | akshare-data | macro_china_* |
| 现货价格 | akshare-data | spot APIs |
| 期货实时行情 | tianqin-data | quote |
| 期货K线 | tianqin-data | klines --duration |
| 期货Tick数据 | tianqin-data | ticks |

## 预期结果

成功的测试应该显示：

1. **路由准确性**：`trade-skills` 能正确识别数据类型并路由到对应技能
2. **参数传递**：路由时能正确传递必要的参数（如品种代码、时间周期等）
3. **数据返回**：最终能成功获取并返回用户请求的数据

## 故障排查

如果技能无法正常工作：

1. **检查技能安装：**
   ```bash
   ls -la ~/.agents/skills/
   # 应该看到 akshare-data, tianqin-data, trade-skills 三个目录
   ```

2. **验证软连接：**
   ```bash
   ls -la ~/.agents/skills/
   # 检查是否有正确的软连接
   ```

3. **查看技能文档：**
   ```bash
   cat ~/.agents/skills/trade-skills/SKILL.md
   cat ~/.agents/skills/akshare-data/SKILL.md
   cat ~/.agents/skills/tianqin-data/SKILL.md
   ```

4. **测试单个数据技能：**
   - 先单独测试 `akshare-data` 和 `tianqin-data` 是否正常工作
   - 确认底层数据技能可用后，再测试 `trade-skills` 的路由功能

5. **重启 AI 助手：**
   - 重新加载 VSCode 窗口
   - 或重启 Claude Code / Cline

## 调试技巧

如果路由不正确，检查：
- 用户请求的关键词是否清晰（如"期货"、"股票"、"K线"等）
- 是否需要更明确的时间周期描述（如"5分钟"、"日线"等）
- 品种代码是否正确（如铁矿石期货代码）
