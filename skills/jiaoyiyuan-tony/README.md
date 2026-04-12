# jiaoyiyuan-tony

`jiaoyiyuan-tony` 是一个偏交易认知、趋势交易、资金管理和风控纪律的公开 skill。

它蒸馏自公开表达中的交易风格，目标不是“代替你做单”，而是让模型在讨论交易问题时更稳定地体现出一种直接、重纪律、重系统、重风险控制的交易员视角。

## 适合什么任务

- 交易认知梳理
- 仓位、止损、盈亏比、资金管理
- 趋势交易与执行纪律
- 交易心态、反人性行为校正
- 交易系统复盘与框架搭建

## 这个 skill 的默认行为

激活后，模型会默认偏向这些行为：

- 不哄人，直接指出认知偏差
- 不鼓励频繁短线和情绪化交易
- 优先强调趋势、盈亏比、止损和仓位
- 不把讨论停在技术指标层面，而是追到系统和纪律
- 更像一个强调生存与复利的交易员，而不是喊单博主

## 安装方式

把这个目录里的 `SKILL.md` 放到你的 skill 目录里即可。

### OpenClaw

```text
请从这个远程地址安装一个 skill，并命名为 `jiaoyiyuan-tony`：
https://github.com/Ibook000/ibook-skill/raw/main/skills/jiaoyiyuan-tony/SKILL.md
要求：
1. 直接读取并导入这个 SKILL.md
2. 安装后把它注册为可调用 skill
3. 激活词包括：

   * 用 Tony 的方式看这笔交易
   * 切到 jiaoyiyuan-tony 模式
   * 按 Tony 的思路拆我的交易系统
   * 用交易员 Tony 的风格回答
4. 安装完成后，回复我是否安装成功，并给我一个测试示例
```

### 最简单的手动安装

1. 新建目录 `jiaoyiyuan-tony`
2. 把本目录里的 [SKILL.md](./SKILL.md) 放进去
3. 在对话里明确提到 `jiaoyiyuan-tony`、`Tony` 或相关激活句

### Codex 目录

```text
~/.codex/skills/jiaoyiyuan-tony/SKILL.md
```

### Claude 目录

```text
~/.claude/skills/jiaoyiyuan-tony/SKILL.md
```

## 如何激活

可以直接这样说：

- `用 jiaoyiyuan-tony 的方式看一下我的交易系统`
- `切到 Tony 交易员模式`
- `按 Tony 的思路拆一下我的仓位管理`
- `用交易员 Tony 的风格回答，别空谈`

## 边界说明

- 这是基于公开表达做的风格化蒸馏，不代表原作者官方授权或本人背书。
- 这个 skill 偏认知、纪律和方法论，不等于投资建议。
- 涉及最新市场事实、价格、政策或规则变化时，模型仍应先查证再回答。

## 仓库内容

- [README.md](./README.md): 给人看的快速说明
- [SKILL.md](./SKILL.md): 给模型直接使用的完整 skill

## 一句话概括

> 一个强调趋势、风控、盈亏比和交易纪律的公开 skill，适合把“怎么看行情”升级成“怎么活下来并长期做对”。
