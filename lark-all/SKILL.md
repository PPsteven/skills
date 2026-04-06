---
name: lark-all
description: "飞书 All-in-One 入口：当用户提出任何飞书相关需求时使用。自动将请求路由到对应的专项 skill（lark-approval / lark-base / lark-calendar / lark-contact / lark-doc / lark-drive / lark-event / lark-im / lark-mail / lark-minutes / lark-sheets / lark-task / lark-vc / lark-whiteboard / lark-wiki / lark-workflow-* 等）。适用场景：用户说'帮我发条飞书消息'、'在飞书日历加个日程'、'查一下飞书任务'、'读取多维表格数据'等一切飞书操作，无需用户指定具体 skill。"
---

# lark-all — 飞书请求路由器

分析用户意图，用 **Skill 工具**调用对应的专项 skill。每个请求只调用一个（或顺序调用多个）skill，不要自行执行飞书命令。

## 路由表

| 场景关键词 | 路由到 |
|---|---|
| 审批、审批流、审批实例 | `lark-approval` |
| 多维表格、Base、bitable、字段、视图 | `lark-base` |
| 日历、日程、会议预约（**未开始**）、忙闲、邀请参会 | `lark-calendar` |
| 通讯录、员工、部门、open_id、搜索同事 | `lark-contact` |
| 云文档、文档创建/编辑、搜索文档 | `lark-doc` |
| 云空间、文件夹、上传/下载文件、文件权限、评论 | `lark-drive` |
| 事件订阅、实时监听、WebSocket | `lark-event` |
| 消息、群聊、发消息、IM、聊天记录 | `lark-im` |
| 邮件、收件箱、起草邮件、回复邮件 | `lark-mail` |
| 妙记、minutes URL（`/minutes/`） | `lark-minutes` |
| 电子表格、Sheet、表格读写 | `lark-sheets` |
| 任务、待办、清单、todo | `lark-task` |
| 视频会议记录（**已结束**）、会议纪要 | `lark-vc` |
| 画板、白板、流程图、架构图、思维导图 | `lark-whiteboard` |
| 知识库、Wiki、知识空间 | `lark-wiki` |
| 整理会议纪要、会议周报 | `lark-workflow-meeting-summary` |
| 今日安排、站会、日程待办摘要 | `lark-workflow-standup-report` |
| 认证、登录、配置初始化、Permission denied | `lark-shared` |
| 需求无法被上述 skill 满足，需原生 OpenAPI | `lark-openapi-explorer` |

## 歧义消解

- **视频会议**：已结束的会议记录/纪要 → `lark-vc`；尚未开始的日程 → `lark-calendar`
- **搜索文件**：按名称/关键词在云空间找文件 → `lark-doc`（`docs +search`）；已知 URL/token 后操作 → `lark-drive` 或 `lark-sheets`
- **多步骤请求**：按顺序依次调用多个 skill（如"发消息并创建任务" → 先 `lark-im`，再 `lark-task`）
