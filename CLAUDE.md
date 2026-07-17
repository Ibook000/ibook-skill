# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

A **skill registry** — a collection of independent, self-contained AI agent skills for Claude Code, OpenClaw, and Codex. Each skill is a markdown-based persona/workflow definition that causes an AI agent to adopt specific behavioral patterns. This is not a traditional software project; the primary artifacts are `.md` files, not code.

## Skills

| Skill | Location | Domain |
|-------|----------|--------|
| `ibook-builder` | `SKILL.md` (root) | Engineering builder persona — system-building, closed-loop delivery |
| `jiaoyiyuan-tony` | `skills/jiaoyiyuan-tony/SKILL.md` | Trading discipline, risk control, position sizing |
| `tweet-card-generator` | `skills/tweet-card-generator/SKILL.md` | Twitter data card generation with 12 chart types |
| `ssh-skill` | `skills/ssh-skill/SKILL.md` | High-performance SSH operations with persistent connections and batch concurrency |
| `ioc-edit` | `skills/ioc-edit/SKILL.md` | STM32CubeMX .ioc file editing (pins, peripherals, clocks, interrupts) |
| `image-well` | `skills/image-well/SKILL.md` | Parallel image search across 12 APIs (4 no-key sources) |
| `chart-visualization` | `skills/chart-visualization/SKILL.md` | Data visualization with 26 chart types |
| `notion-skill` | `skills/notion-skill/SKILL.md` | Notion workspace operations |
| `xiaohongshu-finance` | `skills/xiaohongshu-finance/SKILL.md` | Xiaohongshu financial content generation with banned-word avoidance |

## Skill Anatomy (Convention for Adding/Editing Skills)

Every skill follows this structure:

1. **`SKILL.md`** — Core definition. YAML frontmatter (`name`, `description`), activation rules, behavioral protocols, output contracts, anti-patterns. This is what gets loaded into an AI agent's context.
2. **`README.md`** — Human-readable docs: what it does, installation, usage examples.
3. **`references/`** (optional) — Domain knowledge loaded at generation time (e.g., banned-word lists, reference guides).
4. **`templates/`** (optional) — Reusable assets (HTML templates, shell scripts).
5. **`examples/`** (optional) — Example configurations demonstrating usage.

When adding a new skill, place it under `skills/<skill-name>/` with at minimum a `SKILL.md` and `README.md`. Update the root `README.md` skill directory listing.

## Executable Code

Several skills contain Python scripts with runtime dependencies:

### xiaohongshu-finance

`skills/xiaohongshu-finance/driver.py` renders HTML/SVG templates into PNG images via Playwright.

```bash
# Setup
pip install playwright && playwright install chromium

# Generate a cover image
python driver.py --title "标题" --points "要点1" "要点2" --template card --output output.png

# Generate a complete post (image + text)
python driver.py generate examples/post_chart.json --output-dir output/

# Templates: card, minimal, data, table, comparison, kpi, ranking, chart
# Chart types: line, bar, pie, donut, area, mixed
```

The sub-skill has its own CLAUDE.md at `skills/xiaohongshu-finance/CLAUDE.md` with detailed architecture docs. HTML templates use `{{VARIABLE}}` placeholders. The unified theme is blue-gray (`#111844` / `#4B5694` / `#7288AE` / `#EAE0CF`).

### ssh-skill

`skills/ssh-skill/scripts/` contains 16+ Python scripts for SSH operations:

- `ssh_daemon.py` — Persistent SSH connection daemon
- `ssh_execute.py` — Remote command execution
- `ssh_upload.py` / `ssh_download.py` — File transfer
- `ssh_tunnel.py` — Port forwarding and tunnels
- `ssh_cluster.py` — Batch server operations
- `ssh_config_manager_v3.py` — SSH config management
- `ssh_key_manager.py` — SSH key operations

### image-well

`skills/image-well/scripts/well.py` searches 12 image APIs in parallel:

```bash
# Search across all no-key sources
uv run ~/.claude/skills/image-well/scripts/well.py search "ancient Minoan fresco"

# Search with preset
uv run well.py search "military vehicle" --preset military

# Download with metadata
uv run well.py download "NASA mars" --limit 10 --save-metadata
```

### ioc-edit

`skills/ioc-edit/scripts/ioc_editor.py` edits STM32CubeMX .ioc configuration files programmatically.

## Critical Constraints (xiaohongshu-finance)

These are hard rules from the skill's safety principles, enforced on every output:

- **Banned words are zero-tolerance** — every output must pass `references/banned-words.md`. Hit = replace.
- **Never promise returns** — no "保证赚钱", "稳赚不赔", "年化XX%".
- **Never recommend specific trades** — analyze methods/logic, never say "买入/卖出".
- **Risk disclaimer required** — every piece of financial content must end with a risk warning.
- **No引流/导流** — no WeChat IDs, private messages, or external links.

## Repository Conventions

- Primary language is **Chinese** (README.md, SKILL.md files, references are all in Chinese).
- No build system, no tests, no CI/CD, no linting config at the repo level.
- No `package.json`, `Makefile`, `pyproject.toml`, or `Dockerfile`.
- `.serena/` is in `.gitignore` — local LSP tooling config, not tracked.
- `output/` contains generated sample images from driver.py — not source material.
