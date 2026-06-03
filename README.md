<div align="center">

# 师承.skill / Lineage Skill

**把一整套课，变成一个能被 Agent 调用的课程专家。**

你不用记脚本，也不用理解流水线。把课程材料交给支持 Skill 的 Agent，
然后用自然语言让它整理、追问、复习和调用。

面向 Codex / Claude Code / OpenClaw / Hermes / 自定义 Agent。

[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-orange.svg)](./LICENSE)
[![Skill](https://img.shields.io/badge/AI%20Agent-Skill-orange.svg)](./SKILL.md)

</div>

---

## 这是什么

`lineage-skill` 是一个给 Agent 使用的 Skill。它的目标不是只生成课程摘要，而是帮助你把视频课、训练营、讲座、PDF 讲义、板书、截图、转录和学习笔记沉淀成一套可以反复追问的课程知识系统。

一句话：**把“我学过一套课”变成“我有一个能随时调用的课程专家”。**

## 适合谁

- 你有几十小时甚至上百小时课程材料，想以后能随时问。
- 你不只想要摘要，还想知道“老师在哪一课讲过”“这句话来自哪里”。
- 你想把课程方法变成清单、流程、模板和实操判断规则。
- 你想让 Agent 帮你复习、查漏补缺、整理概念和案例。
- 你已经有转录、OCR、课程笔记或蒸馏结果，想让 Agent 打包成可复用 Skill。

## 怎么使用

### 1. 让 Agent 安装这个 Skill

把这段话发给你的 Agent：

```text
请安装这个 Skill：
https://github.com/JuneYaooo/lineage-skill

安装后请告诉我可以怎样把我的课程材料整理成课程专家。
```

### 2. 告诉 Agent 你的材料在哪里

例如：

```text
我有一个视频课程目录，还有一批 PDF 讲义。
请用 lineage-skill 把它们整理成一个课程专家 Skill。
回答时要尽量保留来源，方便我以后回查。
```

如果你已经有转录或笔记：

```text
我已经有课程转录文本、OCR 文档和课程笔记。
请跳过重新采集，直接整理成可问答、可复习、可检索的课程 Skill。
```

### 3. 用自然语言调用它

生成或整理完成后，你可以这样问：

```text
这套课里，老师是怎么解释“定位”的？
```

```text
帮我按学习顺序整理第 1-5 课的重点，并标出容易混淆的概念。
```

```text
把课程里的实操方法整理成 checklist，我要照着执行。
```

```text
找出老师讲过的三个案例，并说明它们分别对应什么方法。
```

```text
这句话或这个观点出自哪一课？有没有原文依据？
```

## 你可以让它做什么

| 用法 | 你可以这样说 |
| --- | --- |
| 课程问答 | “这套课怎么讲 X？” |
| 课时回查 | “X 是哪一课讲的？” |
| 概念梳理 | “把这些概念的区别讲清楚。” |
| 学习复习 | “给我一条 7 天复习路径。” |
| 案例整理 | “把课程里的案例按主题分类。” |
| 实操清单 | “把老师的方法变成 checklist。” |
| 模板生成 | “按课程方法给我一个可复用模板。” |
| 引用核对 | “这个结论有没有课程原文依据？” |

## 可选模式

你可以直接告诉 Agent 想要哪种用途，也可以让它自己判断。

| 模式 | 适合什么 |
| --- | --- |
| `course-expert` | 课程问答、概念解释、课时回查、来源引用 |
| `study-coach` | 学习计划、复习路径、回忆提示、反思提示 |
| `practitioner` | playbook、checklist、template、实操流程 |
| `citation-archive` | 强引用、原话检索、证据档案、可审计笔记 |
| `knowledge-base` | 多课程目录、概念别名、主题索引 |
| `domain-expert` | 领域方法库、案例库、边界规则 |

也可以组合使用：

```text
请把这套课整理成 course-expert,practitioner 模式。
既能回答课程问题，也能输出实操清单。
```

## 准备材料时怎么说

你不需要提前整理得很完美。告诉 Agent 你有什么即可：

```text
材料包括：
- 视频课目录：里面是 mp4
- PDF 讲义目录
- 我自己的学习笔记

目标：
- 能按课程原意回答问题
- 能引用来源
- 能整理案例和实操步骤
```

如果材料很大，可以补充：

```text
请先检查材料结构，告诉我缺什么、能做什么、建议先处理哪一部分。
```

## 回答边界

这个 Skill 会优先依据你的课程材料回答。课程里没有明确讲过的内容，Agent 应该说明不确定，而不是把模型自己的推断伪装成课程原意。

如果课程属于医疗、法律、金融、投资等高风险领域，它只能做学习整理和材料回查，不应替代专业建议。

## 真实案例

[JuneYaooo/nihaixia](https://github.com/JuneYaooo/nihaixia) 是通过这类课程蒸馏流程沉淀出来的真实 Skill 项目，来源包含 **100GB+ 视频课程材料**，最终整理成可触发、可检索、可溯源的专门领域 Skill。

## 更多文档

- [SKILL.md](./SKILL.md) - Agent 使用入口和执行规则
- [docs/capabilities.md](./docs/capabilities.md) - 能做什么、不能做什么
- [SKILL_MODES.md](./SKILL_MODES.md) - 不同使用模式说明

## License

This project is licensed under the [PolyForm Noncommercial License 1.0.0](./LICENSE).

Noncommercial use is permitted. Commercial use requires separate authorization.
