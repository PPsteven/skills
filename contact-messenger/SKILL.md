---
name: contact-messenger
description: 联系人管理与统一消息发送。当用户说"给 xxx 发消息"、"添加联系人"、"列出联系人"时使用此 skill。支持飞书(imessage)、imsg、Telegram 等多种渠道的联系人管理和消息发送。
---

# Contact Messenger - 联系人管理与消息发送

此 skill 用于管理联系人和发送消息。当你需要处理以下任务时使用：

- 添加新联系人
- 查看/列出联系人
- 给联系人发送消息
- 查询联系人信息

## 联系人数据结构

联系人存储在 `~/.openclaw/workspace/contacts.json`：

```json
{
  "contacts": [
    {
      "id": "unique-id",
      "name": "显示名称",
      "channels": [
        {"type": "feishu_user", "address": "ou_xxxxx", "priority": 1},
        {"type": "feishu_group", "address": "oc_xxxxx", "priority": 2},
        {"type": "imessage", "address": "手机号或邮箱", "priority": 1},
        {"type": "telegram", "address": "telegram_id或username", "priority": 1}
      ]
    }
  ]
}
```

**渠道类型说明：**
- `feishu_user` - 飞书用户，address 为 ou_xxxxx
- `feishu_group` - 飞书群组，address 为 oc_xxxxx
- `imessage` - iMessage/短信，address 为手机号或 Apple ID 邮箱
- `telegram` - Telegram，address 为 username（不带@）或 user_id

**priority 说明：** 数字越小优先级越高。发送消息时优先使用优先级高的渠道。

## 操作指南

### 1. 列出所有联系人

当用户说"列出联系人"、"查看联系人"、"联系人列表"时：

1. 读取 `~/.openclaw/workspace/contacts.json`
2. 以表格形式展示所有联系人，包含：名称、可用渠道、首选渠道

### 2. 添加联系人

当用户说"添加联系人"、"新建联系人"时：

1. 询问用户联系人名称
2. 询问用户的联系方式（支持多种渠道）
3. 读取现有联系人文件
4. 生成新联系人 ID（使用 uuid 或时间戳）
5. 添加到 contacts 数组并保存

**交互示例：**
```
用户：添加联系人
助手：请提供联系人名称
用户：张三
助手：请提供联系方式，格式如：渠道类型:地址（如 feishu_user:ou_xxxxx）
     支持的类型：feishu_user, feishu_group, imessage, telegram
     如有多个渠道，用逗号分隔
用户：feishu_user:ou_abc123, telegram:zhangsan
```

### 3. 删除联系人

当用户说"删除联系人"、"移除联系人"时：

1. 询问要删除的联系人名称或 ID
2. 确认删除
3. 从文件中移除并保存

### 4. 发送消息（核心功能）

当用户说"给 xxx 发消息"、"发送消息给 xxx"时：

**步骤：**
1. 从 contacts.json 查找联系人
2. 按 priority 排序渠道
3. 根据渠道类型调用对应的发送工具：
   - `feishu_user` → 使用 feishu_doc 或 message 工具（需要确认飞书用户ID格式）
   - `feishu_group` → 使用飞书群组消息发送
   - `imessage` → 使用 imsg 工具
   - `telegram` → 使用 message 工具（channel: telegram）
4. 如果第一个渠道发送失败，尝试下一个渠道

**交互示例：**
```
用户：给张三发消息：晚上一起吃饭
助手：（查找张三的联系方式，优先使用 feishu_user:ou_abc123）
     正在通过飞书给张三发送消息...
     消息已发送成功 ✓
```

### 5. 查询联系人信息

当用户问"xxx 的联系方式是什么"、"查看 xxx 信息"时：

1. 查找联系人
2. 显示所有渠道信息

## 文件路径

- 联系人数据：`~/.openclaw/workspace/contacts.json`
- Skill 源码：`~/.openclaw/workspace/skills/contact-messenger/SKILL.md`

## 注意事项

1. 添加联系人时，地址格式要正确：
   - 飞书用户：以 `ou_` 开头
   - 飞书群组：以 `oc_` 开头
   - iMessage：手机号（如 +86138xxxx）或邮箱
   - Telegram：username（不带@）

2. 发送消息失败时，自动尝试下一个渠道，并告知用户

3. 如果联系人不在列表中，提示用户是否添加