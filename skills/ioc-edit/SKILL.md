---
name: ioc-edit
description: "STM32CubeMX .ioc 文件编辑技能。当用户需要修改 .ioc 配置文件时使用，包括：添加/删除引脚、配置外设（I2C/USART/TIM/ADC/GPIO等）、修改时钟树、使能/禁用中断（NVIC）、修改工程设置。触发词：ioc、cubeMX、引脚配置、外设配置、时钟、中断、NVIC、GPIO、I2C、USART、SPI、TIM、ADC、DMA、引脚、pin、添加引脚、删除引脚、配置外设。"
allowed-tools: Bash, Read, Write, Glob
keywords: ioc,cubeMX,STM32,引脚,外设,时钟,中断,NVIC,GPIO,I2C,USART,SPI,TIM,ADC,DMA,pin,配置
---

# STM32CubeMX .ioc Editor Skill

编辑 STM32CubeMX `.ioc` 配置文件的专用技能。

## 调用方式

当用户通过 `/ioc-edit <需求>` 调用时，按以下流程执行。

## 工作流程

### 1. 理解需求

分析用户意图，确定操作类型：
- **引脚操作**：添加/删除/修改引脚及其信号分配
- **外设配置**：修改 I2C、USART、TIM、ADC 等外设参数
- **时钟配置**：修改 RCC 时钟树参数
- **中断配置**：使能/禁用 NVIC 中断，设置优先级
- **工程配置**：修改堆栈大小、工具链等
- **查看/验证**：查看当前配置或验证一致性

### 2. 定位 .ioc 文件

在当前项目目录中查找 `.ioc` 文件：
- 使用 Glob 工具查找 `**/*.ioc`
- 如果有多个，询问用户选择哪个
- 如果只有一个，直接使用

### 3. 查看当前状态

在修改前，先查看相关当前配置：
```bash
# 查看所有配置
python ~/.claude/skills/ioc-edit/scripts/ioc_editor.py <file.ioc> show

# 查看特定部分
python ~/.claude/skills/ioc-edit/scripts/ioc_editor.py <file.ioc> show --section "TIM2."
python ~/.claude/skills/ioc-edit/scripts/ioc_editor.py <file.ioc> show --section "RCC."

# 查看引脚列表
python ~/.claude/skills/ioc-edit/scripts/ioc_editor.py <file.ioc> list-pins

# 查看外设列表
python ~/.claude/skills/ioc-edit/scripts/ioc_editor.py <file.ioc> list-ips
```

### 4. 创建备份

修改前自动备份：
```bash
python ~/.claude/skills/ioc-edit/scripts/ioc_editor.py <file.ioc> backup
```

### 5. 执行修改

根据需求执行对应命令（见下方命令参考）。多项修改按顺序执行。

### 6. 验证结果

修改后验证一致性：
```bash
python ~/.claude/skills/ioc-edit/scripts/ioc_editor.py <file.ioc> validate
```

### 7. 展示变更摘要

向用户展示：
- 执行了哪些修改
- 验证结果
- 提醒用户在 CubeMX 中重新打开确认

## 命令参考

脚本路径：`~/.claude/skills/ioc-edit/scripts/ioc_editor.py`

**路径说明**：`~` 会自动展开为用户家目录。Windows: `C:\Users\用户名\.claude\skills\ioc-edit\scripts\ioc_editor.py`

### 引脚操作

```bash
# 添加引脚（自动更新 Mcu.Pin 列表）
python ioc_editor.py <file.ioc> add-pin PA9 --signal USART1_TX --mode Asynchronous
python ioc_editor.py <file.ioc> add-pin PB6 --signal I2C1_SCL --mode I2C
python ioc_editor.py <file.ioc> add-pin PA1 --signal GPIO_Output --locked

# 删除引脚（自动清理所有相关键）
python ioc_editor.py <file.ioc> remove-pin PA1

# 查看所有引脚
python ioc_editor.py <file.ioc> list-pins
```

### 外设配置

```bash
# 设置外设参数（自动更新 IPParameters 列表）
python ioc_editor.py <file.ioc> config TIM2 Prescaler 71
python ioc_editor.py <file.ioc> config TIM2 Period 999
python ioc_editor.py <file.ioc> config USART1 BaudRate 115200

# 添加/删除外设 IP
python ioc_editor.py <file.ioc> add-ip ADC1
python ioc_editor.py <file.ioc> remove-ip TIM3
```

### 时钟配置

```bash
# 修改时钟参数（自动更新 RCC.IPParameters）
python ioc_editor.py <file.ioc> clock PLLMUL RCC_PLL_MUL9
python ioc_editor.py <file.ioc> clock SYSCLKSource RCC_SYSCLKSOURCE_PLLCLK
python ioc_editor.py <file.ioc> clock APB1CLKDivider RCC_HCLK_DIV2
```

### 中断配置

```bash
# 使能中断并设置优先级
python ioc_editor.py <file.ioc> nvic USART1_IRQn --enable --priority 1 --subpriority 0
python ioc_editor.py <file.ioc> nvic TIM2_IRQn --enable --priority 2 --subpriority 0

# 禁用中断
python ioc_editor.py <file.ioc> nvic TIM3_IRQn --disable
```

### 通用读写

```bash
# 读取任意键
python ioc_editor.py <file.ioc> get Mcu.CPN

# 设置任意键
python ioc_editor.py <file.ioc> set ProjectManager.HeapSize 0x400

# 查看所有配置
python ioc_editor.py <file.ioc> show

# 按前缀过滤
python ioc_editor.py <file.ioc> show --section "NVIC."

# 验证一致性
python ioc_editor.py <file.ioc> validate

# 创建备份
python ioc_editor.py <file.ioc> backup
```

### 试运行模式

添加 `--dry-run` 参数可预览变更而不保存：
```bash
python ioc_editor.py <file.ioc> --dry-run set TIM2.Prescaler 71
python ioc_editor.py <file.ioc> --dry-run add-pin PA5 --signal SPI1_SCK
```

## .ioc 文件格式说明

STM32CubeMX 的 `.ioc` 文件是纯文本键值对格式：

```
# 注释以 # 开头
Key=Value
```

### 关键区域

| 前缀 | 说明 | 示例 |
|------|------|------|
| `Mcu.` | 芯片元数据、引脚/外设列表 | `Mcu.CPN=STM32F103C8T6` |
| `RCC.` | 时钟树配置 | `RCC.PLLMUL=RCC_PLL_MUL16` |
| `NVIC.` | 中断配置 | `NVIC.USART1_IRQn=true\:1\:0\:...` |
| `<PIN>.` | 引脚信号和模式 | `PA9.Signal=USART1_TX` |
| `<PERIPH>.` | 外设参数 | `TIM2.Prescaler=63` |
| `ProjectManager.` | 工程设置 | `ProjectManager.HeapSize=0x200` |

### 一致性规则

- `Mcu.PinsNb` 必须等于 `Mcu.Pin*` 条目数
- `Mcu.IPNb` 必须等于 `Mcu.IP*` 条目数
- `Mcu.Pin*` 和 `Mcu.IP*` 编号必须连续（0, 1, 2, ...）
- 每个 `Mcu.Pin*` 中的引脚必须有对应的 `<PIN>.Signal` 键
- 外设参数变更时 `IPParameters` 列表需同步更新

本脚本自动维护这些一致性规则。

## 重要提醒

1. **始终先备份**：修改前自动创建 `.bak` 文件
2. **先查看再修改**：了解当前配置后再执行变更
3. **验证一致性**：每次修改后运行 `validate`
4. **CubeMX 验证**：建议用户在 CubeMX 中重新打开 `.ioc` 确认无误
5. **USER CODE 保护**：`.ioc` 修改不会影响代码中的 `USER CODE BEGIN/END` 块
