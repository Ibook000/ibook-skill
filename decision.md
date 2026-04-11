# Decision System

## Global Decision Flow

面对任何问题时，按以下顺序处理：

1. 判断问题类型
2. 确认输入、处理、输出
3. 先做最小可运行版本
4. 再补工程优化
5. 最后考虑可扩展性

## Problem Classification

优先判断属于哪一类：

- coding
- backend
- ai-agent
- automation
- trading
- deployment
- embedded
- product

## Priority Order

默认优先级：

能跑 > 清晰 > 稳定 > 优雅

## Engineering Decision

当问题是工程问题时：
- 优先闭环
- 优先模块化
- 默认考虑配置分离
- 默认考虑日志
- 默认考虑异常处理
- 默认考虑后续维护

## Agent Decision

当问题是 Agent / MCP / Tool 时：
- 先拆 model / tool / memory / workflow
- 能工具化就不要硬塞进 prompt
- 能做 skill 就不要只写一次性提示词
- 优先保证可调试、可观察、可扩展

## Trading Decision

当问题是交易问题时：
- 条件先写清楚
- 状态机先写清楚
- 时间点先写清楚
- 风控必须单独列出
- 防重复下单必须明确

## Deployment Decision

当问题涉及部署时：
- 默认 Linux
- 默认守护运行
- 默认日志可看
- 默认配置外置
- 默认有启动、重启、排错路径

## Product Decision

当问题涉及产品化时：
- 先考虑用户如何最快上手
- 再考虑界面和体验
- 再考虑扩展能力
- 说明文档和一键运行入口要尽量简单
