---
name: lark-all
version: 1.0.0
description: "飞书/Lark 统一入口：当用户提出任何与飞书相关的操作需求时使用此 skill。涵盖消息、邮件、日历、会议、云文档、表格、多维表格、知识库、云空间、画板、通讯录、任务、审批、事件订阅等所有飞书场景。即使用户只是说"帮我发个飞书消息"、"查一下日历"、"整理下会议纪要"、"在飞书表格里写数据"也应触发。"
metadata:
  requires:
    bins: ["lark-cli"]
---

# lark-all — 飞书统一路由

你是飞书操作的统一协调者。根据用户意图，将任务路由到对应的专项 skill。

## 路由规则

分析用户需求，调用下方对应的 skill。需求跨多个领域时，可串行调用多个 skill。

### 通讯

| 意图 | Skill |
|------|-------|
| 发消息、回消息、搜聊天记录、管理群聊 | **lark-im** |
| 写邮件、发邮件、回邮件、查邮件、收件箱 | **lark-mail** |

### 日历与会议

| 意图 | Skill |
|------|-------|
| 查日程、创建日程、邀请参会人、查忙闲、推荐时间 | **lark-calendar** |
| 查已结束的视频会议记录、获取会议纪要 | **lark-vc** |
| 获取妙记内容、下载妙记音视频 | **lark-minutes** |
| 整理一段时间的会议纪要报告 | **lark-workflow-meeting-summary** |
| 查今天/本周的日程和待办摘要 | **lark-workflow-standup-report** |

### 文档与文件

| 意图 | Skill |
|------|-------|
| 创建/编辑飞书文档、读取文档内容、搜索云空间文档 | **lark-doc** |
| 上传/下载文件、管理云空间文件夹、文件权限、评论 | **lark-drive** |
| 知识空间、知识库节点管理 | **lark-wiki** |
| 创建/读写电子表格、批量数据操作、导出表格 | **lark-sheets** |
| 多维表格（Base）：建表、字段、记录、视图 | **lark-base** |
| 在云文档中绘制图表、流程图、思维导图、架构图 | **lark-whiteboard** |

### 组织与协作

| 意图 | Skill |
|------|-------|
| 查人员信息、搜同事、查组织架构 | **lark-contact** |
| 创建/管理待办任务、任务清单、分配任务 | **lark-task** |
| 审批实例、审批任务 | **lark-approval** |

### 集成与开发

| 意图 | Skill |
|------|-------|
| 实时监听飞书事件（消息、通讯录变更等） | **lark-event** |
| 需要调用未封装的原生飞书 OpenAPI | **lark-openapi-explorer** |
| 把飞书 API 操作封装成可复用 Skill | **lark-skill-maker** |

### 基础配置

| 意图 | Skill |
|------|-------|
| 初始化配置、登录授权、权限不足、切换 user/bot 身份 | **lark-shared** |

## 执行步骤

1. **理解意图**：从用户消息中提取核心操作目标
2. **选择 skill**：对照路由表确定 1 个或多个目标 skill
3. **调用 skill**：使用 Skill 工具调用，传入用户的原始需求上下文
4. **处理多步骤**：如需跨 skill 操作，先完成前置 skill，再调用后续 skill

## 已知问题与解决方法

### Wiki spaces list 不含"我的文库"

**现象**：执行 `lark-cli wiki spaces list` 只返回团队空间（`space_type: team`），看不到用户个人知识库中的文档。

**原因**：飞书 Wiki 有两种空间类型：
- `team`：团队知识库，`spaces list` 正常返回
- `my_library`：我的文库（个人知识库），`spaces list` **不会返回**

**解决**：列出"我的文库"内容时，需要先通过搜索或已知 node_token 查到 space_id，再用该 space_id 查询节点：

```bash
# 1. 通过搜索找到文档，从 node 信息中获取 space_id
lark-cli wiki spaces get_node --params '{"token":"<node_token>"}'
# 返回中的 space_id 即为 my_library 的 space_id

# 2. 用 space_id 列出该空间下的节点
lark-cli wiki spaces nodes list --params '{"space_id":"<space_id>"}'
```

也可直接用 `docs +search` 搜索，结果会同时包含 team 和 my_library 中的文档。

### SSH 环境下 keychain 无法访问

**现象**：通过 SSH 登录后执行 lark-cli，报错 `keychain access blocked` 或 `keychain Get failed`。

**原因**：SSH 会话默认无法解锁 macOS keychain，lark-cli 读取凭证失败。

**替代方案一（推荐）**：使用设备授权登录，不依赖 keychain：

```bash
lark-cli auth login --no-wait --scope "search:docs:read"
# 执行后会返回授权链接和设备码，在浏览器打开完成授权即可
```

设备授权完成后，后续 lark-cli 命令即可正常工作。如果需要其他 scope，可叠加指定：

```bash
lark-cli auth login --no-wait --scope "search:docs:read,wiki:readonly,docx:readonly"
```

**替代方案二**：在本地终端解锁 keychain 后再通过 SSH 使用（不适用于纯 SSH 环境）：

```bash
security unlock-keychain ~/Library/Keychains/login.keychain-db
# 输入 macOS 登录密码后，再执行 lark-cli 命令
```

## 边界情况

- **需求模糊**：优先匹配最可能的 skill，执行后确认是否符合预期
- **需求跨域**：例如"发消息并附上日程"→ 先 lark-calendar 查询日程，再 lark-im 发送消息
- **权限报错**：遇到 Permission denied 时，路由到 **lark-shared** 处理权限问题
- **无匹配 skill**：使用 **lark-openapi-explorer** 探索原生 API
- **keychain 报错**：SSH 环境下使用 `lark-cli auth login --no-wait --scope <needed_scope>` 设备授权，或切回本地终端解锁 keychain 后重试

## 快速参考：高频场景

```
"发飞书消息给 XX"          → lark-im
"帮我看下今天日程"          → lark-calendar (+agenda)
"在表格里写数据"            → lark-sheets / lark-base (视表格类型)
"整理下上周的会议纪要"      → lark-workflow-meeting-summary
"搜索一下云空间里的文件"    → lark-doc (+search)
"查一下 XX 的联系方式"      → lark-contact
"创建一个待办任务"          → lark-task
"给我看看妙记内容"          → lark-minutes
```
