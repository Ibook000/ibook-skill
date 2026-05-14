# ibook-skill

<p align="center">
  <strong>Ibook000 的个人 AI Agent Skill 仓库</strong><br>
  直接、工程、实战——让 AI 按我的方式工作
</p>

---

## 这是什么

这里存放我自己日常使用的 AI Agent **Skills**。每个 Skill 都是一个可加载的协作协议，让模型获得特定领域的知识、工作流和人格风格。

不是教程，不是文档站——是**拿来就用的工具包**。

---

## 技能列表

### 🏗️ ibook-builder

> 工程 Builder 操作系统 · 把想法做成能跑的系统

**解决什么问题：** 不想让 AI 只给概念建议？想要一个默认就考虑配置、日志、异常、部署的协作模式？

**核心风格：**
- 先给明确结论，再给实现路径
- 先做最小可运行闭环，再谈优化
- 能工具化就不停在 prompt
- 默认补充文件结构、接口、日志、部署要点

**激活方式：**
```
用 ibook 的方式做这个
按 ibook 的思路拆
切到 ibook 模式
别空谈，直接给我能跑的版本
```

**适用场景：** AI 应用开发、Python 后端、Agent/MCP/Skill 设计、自动化工具、交易系统、Web 后台、Linux 部署

[→ 查看 SKILL.md](./SKILL.md)

---

### 📈 jiaoyiyuan-tony

> 李法师Tony · 交易思维操作系统

**解决什么问题：** 交易中迷茫、频繁止损、守不住利润、被市场情绪左右？

**核心理念：**
- 技术只占 30%，资金管理和心态占 60%
- 交易就是越符合人性的越赚不到钱
- 趋势为王，小赔大赚，做大盈亏比
- 独立思考，远离噪音，不猜顶底

**激活方式：**
```
用 Tony 的交易思维分析一下
按李法师的思路看这个行情
Tony，我该不该止损
```

**适用场景：** 交易心态纠正、资金管理设计、趋势判断、风控体系搭建、财富认知升级

[→ 查看 SKILL.md](./skills/jiaoyiyuan-tony/SKILL.md)

---

### 🐦 tweet-card-generator

> 推特卡片生成器 · 一句话生成高密度数据卡片

**解决什么问题：** 想发数据驱动的推文但没有设计能力？需要快速把数据变成好看的信息图？

**能力：**
- 输入一个话题 → 自动搜索数据 → 生成推文 + PNG 数据卡片
- **12 种 SVG 图表**：柱状图、饼图、流程图、面积图、堆叠柱、环形图……
- **4 种布局**：Split / Stacked / Big Number / Timeline
- 米白底色 + `@IBO0OK` 水印，风格统一

**激活方式：**
```
生成一张关于 BTC ETF 流量的卡片
做个黄金持仓变化的图发推
tweet card for NVIDIA earnings
```

**适用场景：** 推特/社交媒体数据可视化、加密货币数据分析、快速制作信息图、自动推文配图

[→ 查看 SKILL.md](./skills/tweet-card-generator/SKILL.md) | [模板目录](./skills/tweet-card-generator/templates/)

---

## 仓库结构

```
ibook-skill/
├── README.md                          ← 你正在看
├── SKILL.md                           ← ibook-builder 主 Skill
└── skills/
    ├── jiaoyiyuan-tony/
    │   └── SKILL.md                   ← Tony 交易员 Skill
    └── tweet-card-generator/
        ├── SKILL.md                   ← 推特卡片生成器 Skill
        └── templates/
            ├── card-dense.html        ← 高密度多区块模板
            ├── card-template.html     ← 经典 4 布局模板
            └── chart-examples.html    ← 12 种 SVG 图表库
```

---

## 安装方式

### 给 Hermes Agent 用户

在对话中直接说：

> 从 https://github.com/Ibook000/ibook-skill 安装 skill，把我需要的加进去

或者手动复制对应 `SKILL.md` 到 `~/.hermes/skills/` 目录。

### 给其他 AI Agent 用户

把需要的 `SKILL.md` 放到你的 Agent 的 skills 目录即可。每个 Skill 文件都是自包含的，不依赖外部运行时。

---

## 一句话

> 不是让 AI 学我说话，是让 AI 按我的方式做事。

---

<p align="center">
  <sub>Made by <a href="https://github.com/Ibook000">Ibook000</a> · 持续补充中</sub>
</p>
