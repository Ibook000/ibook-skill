# Trading Journal Workflow (交易笔记)

## Primary Target: 每日交易复盘 Database

User's main trading journal is the **"每日交易复盘" database** (ID: `656aa858-6967-4b0b-a38b-94ac21ac548d`), NOT the "交易笔记" page.

**Always write daily trading notes as new entries in this database.**

## Database Schema

| Property | Type | Notes |
|----------|------|-------|
| Name | title | Entry title, e.g. "6月7日 反弹行情逆势开空，亏麻了" |
| 日期 | date | Format: YYYY-MM-DD |
| 盈亏_u | number | Profit/loss in USDT (negative for losses) |
| 类型 | select | 做多 / 做空 / Other |
| 问题 | multi_select | Tags like: 多单没拿住, 空单乱开, 频繁反手, 逆势交易 |
| 资产 | multi_select | Asset traded (e.g. BTC) |

## Workflow: Creating a Daily Entry

### Step 1: Create database entry with properties

```bash
curl -s --max-time 30 -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d @/tmp/notion_entry.json
```

### Step 2: Query database to get full page ID

**Critical**: The returned page ID from Step 1 may be truncated. Always query the database to get the full UUID:

```bash
curl -s --max-time 30 -X POST "https://api.notion.com/v1/databases/656aa858-6967-4b0b-a38b-94ac21ac548d/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"sorts": [{"property": "日期", "direction": "descending"}], "page_size": 1}'
```

### Step 3: Add content blocks to the page

```bash
curl -s --max-time 30 -X PATCH "https://api.notion.com/v1/blocks/{full_page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d @/tmp/notion_detail.json
```

## Content Structure for Detail Blocks

```
### 行情                   (heading_3)
- 行情描述                 (paragraph)

### 操作问题               (heading_3)
- 具体问题                 (paragraph)

### 教训                   (heading_3)
- lesson 1                 (bulleted_list_item)
- lesson 2                 (bulleted_list_item)
...

### 计划                   (heading_3)
- 接下来打算               (paragraph)
```

## Behavior Notes

- **Incremental updates**: User reflects in multiple messages. Add new blocks after each message rather than waiting for full summary.
- **Lessons as bullet points**: User dictates rules like "不要多空双吃" — turn them into bulleted list items.
- **Don't editorialize**: User calls themselves "纯傻子" — don't argue or soften, just record. They're using self-critique as motivation.
- **No rigid templates**: User explicitly said templates are too rigid. They want their own casual, self-deprecating style preserved.
- **Chinese throughout**: User trades in Chinese context, all notes in Chinese.
- **Confirm target**: If user says "交易笔记", clarify whether they mean the database (每日交易复盘) or the page (交易笔记). Default to database.

## Other Notion Pages (for reference)

- 交易笔记 page: `2f8743c5-2624-803d-b9bd-dd91f2607d5d` (general notes, not daily entries)
- 任务清单: `31a743c5-...`
- 任务跟踪器 database: `5a3aa4a3-...`
