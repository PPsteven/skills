│ 2. 优化生成流程（采用 AskUserQuestion 实现交互选择）                                                                                                  │
│                                                                                                                                                       │
│ 目标： 让用户能够轻松选择"全部 categories"或"自定义选择"                                                                                              │
│                                                                                                                                                       │
│ 流程改进：                                                                                                                                            │
│                                                                                                                                                       │
│ 步骤 1: 输入 URL                                                                                                                                      │
│   └─ 用户提供 OpenAPI 规范 URL                                                                                                                        │
│                                                                                                                                                       │
│ 步骤 2: 解析并提取 categories                                                                                                                         │
│   └─ openapi_parser.py 获取所有 category 列表                                                                                                         │
│                                                                                                                                                       │
│ 步骤 3: 使用 AskUserQuestion 询问选择方式                                                                                                             │
│   └─ 选项 A: 全部 categories (不提)                                                                                                                   │
│   └─ 选项 B: 自定义选择 N 个                                                                                                                          │
│                                                                                                                                                       │
│ 步骤 4: 获取用户选择                                                                                                                                  │
│   └─ 若选"全部" → 使用所有 categories                                                                                                                 │
│   └─ 若选"自定义" → 列出每个 category 让用户多选                                                                                                      │
│                                                                                                                                                       │
│ 步骤 5: 循环生成 CLI 命令                                                                                                                             │
│   └─ 对每个 category                                                                                                                                  │
│     ├─ 获取所有 endpoints                                                                                                                             │
│     ├─ 对每个 endpoint                                                                                                                                │
│     │ ├─ 解析参数信息                                                                                                                                 │
│     │ ├─ 生成 Click 命令定义                                                                                                                          │
│     │ └─ 生成对应的 API 调用代码                                                                                                                      │
│     └─ 生成该 category 的完整命令组                                                                                                                   │
│                                                                                                                                                       │
│ 步骤 6: 验证和生成最终 skill                                                                                                                          │
│   └─ 使用 skill-creator 技能验证符合规范                                                                                                              │
│                                                                                                                                                       │
│ 关键改动：                                                                                                                                            │
│ - 替换当前的 prompt_category_selection() 为 AskUserQuestion 调用                                                                                      │
│ - 支持批量选择（multiSelect: true）                                                                                                                   │
│ - 显示每个 category 的端点数量作为参考 