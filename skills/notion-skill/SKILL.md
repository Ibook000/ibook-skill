---
name: notion
description: "Notion API via curl: pages, databases, blocks, search."
version: 1.0.0
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Notion, Productivity, Notes, Database, API]
    homepage: https://developers.notion.com
prerequisites:
  env_vars: [NOTION_API_KEY]
---

# Notion API

Use the Notion API via curl to create, read, update pages, databases (data sources), and blocks. No extra tools needed — just curl and a Notion API key.

## Prerequisites

1. Create an integration at https://notion.so/my-integrations
2. Copy the API key (starts with `ntn_` or `secret_`)
3. Store it in `~/.hermes/.env`:
   ```
   NOTION_API_KEY=ntn_your_key_here
   ```
4. **Important:** Share target pages/databases with your integration in Notion (click "..." → "Connect to" → your integration name)

## API Basics

All requests use this pattern:

```bash
curl -s -X GET "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

The `Notion-Version` header is required. This skill uses `2025-09-03` (latest). In this version, databases are called "data sources" in the API.

## Common Operations

### Search

```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

### Get Page

```bash
curl -s "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### Get Page Content (blocks)

```bash
curl -s "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### Create Page in a Database

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "xxx"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Item"}}]},
      "Status": {"select": {"name": "Todo"}}
    }
  }'
```

### Query a Database

```bash
curl -s -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "Active"}},
    "sorts": [{"property": "Date", "direction": "descending"}]
  }'
```

### Create a Database

```bash
curl -s -X POST "https://api.notion.com/v1/data_sources" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "xxx"},
    "title": [{"text": {"content": "My Database"}}],
    "properties": {
      "Name": {"title": {}},
      "Status": {"select": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
      "Date": {"date": {}}
    }
  }'
```

### Update Page Properties

```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

### Add Content to a Page

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello from Hermes!"}}]}}
    ]
  }'
```

## Property Types

Common property formats for database items:

- **Title:** `{"title": [{"text": {"content": "..."}}]}`
- **Rich text:** `{"rich_text": [{"text": {"content": "..."}}]}`
- **Select:** `{"select": {"name": "Option"}}`
- **Multi-select:** `{"multi_select": [{"name": "A"}, {"name": "B"}]}`
- **Date:** `{"date": {"start": "2026-01-15", "end": "2026-01-16"}}`
- **Checkbox:** `{"checkbox": true}`
- **Number:** `{"number": 42}`
- **URL:** `{"url": "https://..."}`
- **Email:** `{"email": "user@example.com"}`
- **Relation:** `{"relation": [{"id": "page_id"}]}`

## Key Differences in API Version 2025-09-03

- **Databases → Data Sources:** Use `/data_sources/` endpoints for queries and retrieval
- **Two IDs:** Each database has both a `database_id` and a `data_source_id`
  - Use `database_id` when creating pages (`parent: {"database_id": "..."}`)
  - Use `data_source_id` when querying (`POST /v1/data_sources/{id}/query`)
- **Search results:** Databases return as `"object": "data_source"` with their `data_source_id`

## Pitfalls

### API calls timeout from certain regions
From servers in China (or other regions with poor connectivity to Notion), API calls frequently timeout with default settings. Use `--max-time 30` for curl and `timeout: 60` for terminal calls. Initial connection test (`/v1/users/me`) is the most likely to timeout — always use extended timeout there.

### Always confirm target when user says "write to X"
Users may have multiple similar pages/databases (e.g. "交易笔记" page vs "每日交易复盘" database). Before writing, confirm which one they mean. When in doubt, default to the database (structured data) over the page (freeform notes).

### Get full page ID after creating database entries
The page ID returned from `POST /v1/pages` may be truncated or in a different format than what `PATCH /v1/blocks/{id}/children` expects. **Always query the database after creating an entry** to get the full UUID before adding content blocks:

```bash
# After POST /v1/pages, query to get full ID:
curl -s -X POST "https://api.notion.com/v1/databases/{db_id}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -d '{"sorts": [{"property": "Date", "direction": "descending"}], "page_size": 1}'
```

### Shell escaping kills complex JSON payloads
When `curl -d '...'` contains variable interpolation (`$VAR`, backticks, nested quotes), shell escaping silently corrupts the JSON. **Always write the payload to a temp file and use `-d @file`:**

```python
# In execute_code, build payload as a Python dict, dump to file:
import json
with open('/tmp/notion_payload.json', 'w') as f:
    json.dump(payload, f, ensure_ascii=False)

# Then curl with -d @file:
terminal('curl -s -X POST ... -d @/tmp/notion_payload.json')
```

This avoids all shell escaping issues with `{"rich_text": [{"text": {"content": "..."}}]}` nesting.

### API version compatibility
The `2022-06-28` API version is the most stable and widely compatible. The newer `2025-09-03` renames databases to "data sources" and changes endpoint paths (`/databases/` → `/data_sources/`). Use `2022-06-28` unless you specifically need the newer features.

### Select fields accept new values dynamically
Notion API creates new select/multi_select options on the fly — you don't need to pre-define them in the database. Use any string value and it becomes a new option.

## Notes

- Page/database IDs are UUIDs (with or without dashes)
- Rate limit: ~3 requests/second average
- The API cannot set database view filters — that's UI-only
- Use `is_inline: true` when creating data sources to embed them in pages
- Add `-s` flag to curl to suppress progress bars (cleaner output for Hermes)
- Pipe output through `jq` for readable JSON: `... | jq '.results[0].properties'`
- See `references/notion-memory-db.md` for the user's 记忆库 database schema and write pattern
- See `references/trading-journal-workflow.md` for writing daily trading notes (交易笔记)
