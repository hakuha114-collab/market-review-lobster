# 🦞 Market Review Lobster

> A股 / 港股 / 美股 / 日韩 全市场覆盖的智能复盘报告生成 Skill

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/hakuha114-collab/market-review-lobster)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🎯 这是什么？

Market Review Lobster 是一个基于 OpenClaw 平台的自动化市场复盘报告生成技能。它能够自动采集全球市场数据（A股、港股、美股、日韩），生成结构化、数据驱动、**龙虾风格**的深度复盘报告。

> 🦞 "龙虾风格" = 热辣、主动、数据驱动、带点叛逆的分析师口吻

---

## ✨ 核心能力

| 功能 | 说明 |
|------|------|
| 📊 **六大市场覆盖** | A股、港股、美股、日股、韩股、亚洲三市对比 |
| 📈 **VIX 恐慌指数** | 五维分析模型（当前值/历史分位/形态/期权信号/口诀） |
| 💰 **板块资金流向** | 精确到小数点后两位，全市场 + 行业板块双维度 |
| 🔥 **热点主题挖掘** | TOP5 热点事件，含催化剂、市场反应、龙虾点评 |
| 🏆 **涨停连板追踪** | 连板梯队、封板率、晋级率 |
| 🌏 **外资资金流向** | 北向资金、南向资金、东财/雪球/淘股吧情绪 |
| 📋 **仓位管理建议** | 综合情绪指标 → 建议仓位（30%-80%） |
| ⏰ **定时自动推送** | Cron 配置，美股 08:00 / A股港股 20:00 自动生成 |

---

## 📐 报告结构（十一大模块）

```
1. 📊 市场整体表现概览        — 六大指数对比表
1.5 📉 VIX 恐慌指数分析       — 五维模型 + 口诀 + 仓位对照表
2. 💰 板块资金流入流出详情     — TOP5 流入/流出 + 龙虾点评
2.5 📈 龙头个股资金净流入     — TOP10 个股表
2.6 🏆 涨停连板梯队          — 连板晋级率 + 热点主题
2.7 🔥 热点主题一览          — 概念涨幅 + 代表个股
2.8 🇭🇰 港股明星个股         — 港股特色数据
3. 🎯 主流资金视角分析       — 五大投资人行为画像
4. 🔥 热点事件深度解析       — TOP5 事件 + 催化剂 + 点评
5. 🌏 亚洲三市资金流向对比   — 资金迁移可视化图
6. 💬 散户情绪与讨论热度     — 多平台情绪数据
6.5 📊 情绪与仓位管理总表    — 综合仓位建议
7. ⚔️ 内外资多空对决        — 多空双方博弈分析
8. 📈 后市推演与策略建议     — 超配/标配/低配板块
9. 🔮 关键监测信号           — 未来一周关键事件
9.5 🌍 地缘与宏观数据        — 美伊谈判/美联储/大宗商品/汇率
10. 🦞 龙虾终极总结          — 五大核心叙事 + 行动清单
```

---

## 🦞 龙虾风格示例

> **热点 1：算力租赁概念全面爆发**
> - **催化剂：** 英伟达量子AI模型发布 + 国内大模型训练需求激增
> - **涨停个股：** 剑桥科技、中科曙光、浪潮信息等多股涨停
> - **🦞 龙虾点评：** "AI算力是贯穿全年的主线，每次回调都是上车机会！"

> **VIX 口诀：**
> - VIX 低位别冲动，崩盘往往在梦中！
> - VIX 高位大胆冲，历史大底在其中！
> - VIX 背离要当心，上涨假象要分清！

---

## 🚀 快速开始

### 前置要求

- [OpenClaw](https://github.com/ClawdHub/OpenClaw) 已安装
- ProSearch 搜索工具可用
- vix-index skill（用于美股报告 VIX 数据）

### 安装

```bash
# 方式一：直接下载 SKILL.md
curl -O https://raw.githubusercontent.com/hakuha114-collab/market-review-lobster/main/SKILL.md

# 方式二：克隆整个仓库
git clone https://github.com/hakuha114-collab/market-review-lobster.git
```

将 `SKILL.md` 放置到 OpenClaw skills 目录：

```
~/.qclaw/skills/white-market-review-lobster/SKILL.md
```

### 使用

在 OpenClaw 中发送以下指令：

```
生成A股港股复盘报告
```

或

```
生成美股复盘报告
```

或

```
查一下当前 VIX 恐慌指数
```

---

## ⏰ 定时任务配置

### 美股报告（每天 08:00 北京时间）

```yaml
name: 每日美股复盘报告
schedule: "0 8 * * *"
timezone: Asia/Shanghai
payload:
  kind: agentTurn
  message: "请生成美股市场的深度复盘报告，包含十大模块，使用龙虾风格"
  model: qclaw/modelroute
  timeoutSeconds: 300
delivery:
  mode: announce
  channel: feishu
```

### A股港股报告（每天 20:00 北京时间）

```yaml
name: 每日A股港股复盘报告
schedule: "0 20 * * *"
timezone: Asia/Shanghai
payload:
  kind: agentTurn
  message: "请生成A股港股市场的深度复盘报告，包含十大模块，使用龙虾风格"
  model: qclaw/modelroute
  timeoutSeconds: 300
delivery:
  mode: announce
  channel: feishu
```

---

## 📋 数据精度规范

| 数据类型 | 格式要求 | 示例 |
|----------|----------|------|
| 资金净流入/流出 | 两位小数 + 单位 | 65.76亿元 |
| 涨跌幅 | 两位小数 + % | +3.17% |
| 指数点位 | 两位小数 + 点 | 4,055.55点 |
| 成交额 | 两位小数 + 单位 | 9,766亿元 |
| 外资数据 | 精确到亿美元 | 186.5亿美元 |

---

## 🔧 依赖的 Skill

| Skill | 用途 |
|-------|------|
| `search-market.js` | 实时市场数据搜索（ProSearch封装） |
| `vix-index` | VIX 恐慌指数实时查询（CNBC直连） |
| `online-search` | 数据补充/交叉验证（备用降级方案） |
| `memory_search` | 检索用户偏好、过往报告模板 |
| `cron` | 定时任务调度 |

---

## 📊 最近的报告数据（2026-04-16）

| 市场 | 指数 | 收盘点位 | 涨跌幅 |
|------|------|----------|--------|
| 🇨🇳 A股 上证 | 4,055.55 | +0.70% |
| 🇨🇳 A股 创业板 | 3,626.27 | **+3.17%** ⭐ 11年新高 |
| 🇭🇰 港股 恒生 | 26,394.26 | +1.72% |
| 🇭🇰 港股 恒科 | 5,092.08 | **+3.67%** ⭐ 重返5000点 |
| 🇯🇵 日股 日经225 | 58,969.97 | +1.44% |
| 🇰🇷 韩股 KOSPI | 6,188.99 | +1.60% |

**全市场：88只涨停 / 9只跌停 | 成交2.34万亿 | VIX=17.9（中性偏乐观）**

---

## 📝 许可证

MIT License - 自由使用、修改和分发

---

## 🦞 Credits

- 灵感来源：[市场分析龙虾](https://github.com/m Lobster) Agent
- 技术栈：OpenClaw + ProSearch + vix-index
- 开发者：hakuha114-collab

---

**🦞 龙虾到！市场复盘，交给龙虾！**
