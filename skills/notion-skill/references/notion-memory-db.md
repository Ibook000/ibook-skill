# Notion 记忆库 — Database Write Pattern

## Database Info
- **Database ID:** `3b76ebc6-4b8f-4e4b-9854-51ca391938e7`
- **API Version:** `2022-06-28`
- **Env var:** `NOTION_API_KEY` (in `~/.hermes/.env`)

## Schema

| Field | Type | Values / Notes |
|-------|------|----------------|
| Name | title | Short title (≤20 chars) |
| 来源 | select | **HKBOT** (user wants this, not "Hermes"), also: Claude, GPT, Gemini, 其他, 香橙派 |
| 类型 | select | 用户信息 / 环境配置 / 技能知识 / 偏好设置 / 经验教训 |
| 标签 | multi_select | 硬件, AI, 工具, 开发, API, 配置, 密钥, etc. (free-form, new options auto-created) |
| 日期 | date | YYYY-MM-DD |

## Write Template

Use `execute_code` to build the payload as a Python dict (avoids shell escaping):

```python
import json, datetime
from hermes_tools import terminal

today = datetime.date.today().isoformat()

payload = {
    "parent": {"database_id": "3b76ebc6-4b8f-4e4b-9854-51ca391938e7"},
    "properties": {
        "Name": {"title": [{"text": {"content": "简短标题"}}]},
        "类型": {"select": {"name": "环境配置"}},
        "来源": {"select": {"name": "HKBOT"}},
        "标签": {"multi_select": [{"name": "标签1"}]},
        "日期": {"date": {"start": today}}
    },
    "children": [
        {"object": "block", "type": "paragraph", "paragraph": {
            "rich_text": [{"text": {"content": "详细内容"}}]
        }}
    ]
}

json_body = json.dumps(payload, ensure_ascii=False)
with open('/tmp/notion_payload.json', 'w') as f:
    f.write(json_body)

result = terminal(
    'curl -s -X POST "https://api.notion.com/v1/pages" '
    '-H "Authorization: Bearer $NOTION_API_KEY" '
    '-H "Notion-Version: 2022-06-28" '
    '-H "Content-Type: application/json" '
    '-d @/tmp/notion_payload.json'
)
```

## Trigger Rules
Write to this DB when:
1. User says "记住" or "记一下"
2. Discovered environment/config info
3. User shares preferences or habits
4. Solved a non-trivial problem
5. Learned a new tool usage
