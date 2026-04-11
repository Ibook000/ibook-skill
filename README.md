# ibook-builder

`ibook-builder` 是一个面向 AI coding agent 的公开 skill。

它蒸馏自 `ibook / Ibook000` 的实际工作方式，核心目标不是“像某个人说话”，而是让模型更稳定地表现出一种偏工程落地的 builder 风格：

- 先给明确结论，再给实现路径
- 先做最小可运行闭环，再谈优化
- 默认考虑配置、日志、异常处理和部署
- 能工具化就不只停在 prompt
- 遇到复杂问题先拆模块，不空谈

如果你想让模型更像一个会把想法做成系统的人，而不是只会给概念建议，这个 skill 就是给你用的。

## 适合什么任务

- AI 应用开发
- Python 后端、FastAPI、服务化工具
- AI Agent / MCP / Skill / Tool Calling 设计
- Discord Bot、自动化工具、工作流系统
- 交易工具、量化策略、Polymarket / Binance / OKX 相关系统
- Web 后台、前后端分离管理平台
- ESP32 / AIoT / 语音交互 / 硬件联动
- Linux 部署、Systemd / Docker、日志与运维

## 这个 skill 的默认行为

激活后，模型会默认更偏向这些行为：

- 优先输出可执行方案，而不是泛泛建议
- 优先跑通核心路径，而不是先追求“最优设计”
- 默认补充文件结构、接口、配置、日志和部署要点
- 复杂问题先拆成输入、状态、执行、存储、输出几个部分
- 遇到交易或自动化问题时，优先把状态机、风控和异常恢复讲清楚

## 安装方式

把本仓库里的 `SKILL.md` 放到你的 skill 目录里即可。

### OpenClaw
```text
请从这个远程地址安装一个 skill，并命名为 `ibook-builder`：
https://github.com/Ibook000/ibook-skill/raw/main/SKILL.md
要求：
1. 直接读取并导入这个 SKILL.md
2. 安装后把它注册为可调用 skill
3. 激活词包括：

   * 用 ibook 的方式做
   * 按 ibook 的思路拆
   * 切到 ibook 模式
   * 别空谈，直接给我能跑的版本
4. 安装完成后，回复我是否安装成功，并给我一个测试示例
```

### 最简单的手动安装

1. 新建目录 `ibook-builder`
2. 把本仓库里的 [SKILL.md](./SKILL.md) 放进去
3. 在对话里明确提到 `ibook` 或 `ibook-builder`
### Codex 目录

```text
~/.codex/skills/ibook-builder/SKILL.md
```

### Claude 目录

```text
~/.claude/skills/ibook-builder/SKILL.md
```
## 如何激活

可以直接这样说：

- `用 ibook-builder 的方式做这个需求`
- `按 ibook 的思路拆一下这个系统`
- `切到 ibook 模式，别空谈，直接给我能跑的版本`
- `用 ibook 的方式，把这个 FastAPI + MCP 服务做成最小可部署版本`
- `按 ibook-builder 思路，把这个交易策略整理成带风控的状态机`

## 输出风格

使用这个 skill 后，你通常会得到这种风格的结果：

- 更偏工程落地，而不是泛泛建议
- 更偏系统闭环，而不是一次性 demo
- 更偏可运行、可部署、可维护，而不是只讲架构图
- 更偏“直接做”，而不是长篇分析后不落地

## 仓库内容

- [README.md](./README.md): 给人看的快速说明
- [SKILL.md](./SKILL.md): 给人看也给模型直接使用的完整 skill

## 一句话概括

> 一个偏工程落地的系统型 builder skill，关注的不只是把模型接上，而是把东西做成能跑、能部署、能维护的系统。
