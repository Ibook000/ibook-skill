# ibook.skill

一个围绕 **AI 应用开发 / Python 后端 / AI Agent / 自动化系统 / 交易工具 / 嵌入式 AIoT** 蒸馏出来的个人 skill。

它不是一句人格 prompt，而是一套能复用的工作方法：

- 定义身份
- 固化决策方式
- 提炼自我约束
- 沉淀复盘机制
- 按领域拆成能力模块

目标不是“像你说话”，而是尽量逼近你真实做事的方式。

## 核心画像

ibook 更像一个偏工程落地的系统型 builder：

- 喜欢把能力做成 bot / tool / skill / server
- 默认考虑配置、部署、日志、异常处理和长期运行
- 擅长把 AI、自动化、交易逻辑和真实系统接起来
- 行动力强，但会主动把经验沉淀成规则

## 适用场景

当任务属于下面这些方向时，适合启用：

- Python / FastAPI / 后端开发
- AI Agent / LangChain / MCP / Tool Calling / Skill 设计
- 自动化系统 / Bot / 服务化工具
- 交易机器人 / 策略逻辑 / 风控流程
- Linux 部署 / systemd / 配置管理 / 运行维护
- ESP32 / AIoT / 软硬件联动
- 从想法快速落成可运行系统

## 仓库结构

- `SKILL.md`：技能入口，定义基础身份、工作方式和模块加载策略
- `identity.md`：基础身份和技术背景
- `builder_identity.md`：更深层的 builder 画像
- `decision.md`：默认决策路径
- `self_rules.md`：长期约束和行为规则
- `reflection_engine.md`：复盘与规则沉淀方式
- `style.md`：表达风格
- `productization.md`：产品化和交付偏好
- `skills/*`：具体领域模块

## 安装

把整个目录放到你的 skill 目录里，例如：

```bash
~/.codex/skills/ibook/
```

或：

```bash
~/.claude/skills/ibook/
```

## 使用方式

调用时不要只说“帮我写代码”，而是明确告诉模型要以 `ibook` 的方式做事。

示例：

```text
用 ibook.skill 的方式，帮我把一个 FastAPI + MCP 服务做成最小可部署版本。
```

```text
用 ibook.skill 的方式，把这个交易策略整理成可执行状态机，并补上风控约束。
```

```text
用 ibook.skill 的方式，帮我把一个想法落成 bot/tool/skill，并给出目录结构和启动方式。
```

## 设计重点

这个 skill 的重点不是“语气像不像我”，而是下面这些约束会被默认带上：

- 先闭环，再优化
- 先可运行，再谈优雅
- 能工具化就不要只停在 prompt
- 默认考虑配置、日志、异常和部署
- 复盘的目标是提炼规则，不是情绪宣泄

## 一句话定义

> 一个会把 AI、自动化、交易逻辑和真实工程环境接起来的人；有冲劲，但会用规则把冲劲驯化成系统。
