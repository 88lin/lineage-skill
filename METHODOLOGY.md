# C5 课程炼化框架

`师承.skill` 的基础方法论是 C5。它是一个面向 AI Skill 生成的课程炼化流程，理论上对应教学设计、认知学徒制、知识管理、多媒体学习和 RAG。

详细理论基础见 [THEORETICAL_FOUNDATION.md](./THEORETICAL_FOUNDATION.md)。

```text
Capture → Cite → Compress → Connect → Codify
采集 → 溯源 → 压缩 → 关联 → 技能化
```

实际工程中还有一个质量闭环：

```text
Capture → Cite → Compress → Connect → Codify → Evaluate
采集 → 溯源 → 压缩 → 关联 → 技能化 → 评估
```

## 总览

```text
┌────────────┐
│  Capture   │  采集课程原始材料
└─────┬──────┘
      │
      ▼
┌────────────┐
│    Cite    │  建立可回溯证据链
└─────┬──────┘
      │
      ▼
┌────────────┐
│  Compress  │  分层压缩课程内容
└─────┬──────┘
      │
      ▼
┌────────────┐
│  Connect   │  重建课程知识结构
└─────┬──────┘
      │
      ▼
┌────────────┐
│   Codify   │  封装为可调用 Skill
└─────┬──────┘
      │
      ▼
┌────────────┐
│  Evaluate  │  评估完整性、证据强度和可用性
└────────────┘
```

## Capture：采集

目标：尽量完整地拿到课程材料。

输入可以包括：

- 视频
- 音频
- PDF
- 扫描件
- 讲义
- 字幕
- 课程附件
- 学员问答

关键原则：

- 先保留原始材料，再做压缩
- 尽量保留文件名、课程序号、时间顺序
- 不要只依赖单一文本来源

## Cite：溯源

目标：让每个重要结论都可以回到来源。

证据类型：

- 转录 JSON
- 完整转录 Markdown
- 视觉分析 Markdown
- 板书/PPT/图表截图
- 文件路径
- 视频课程序号
- 时间点

关键原则：

- 没有证据的内容要降低置信度
- 课程观点和模型观点要区分
- 涉及专业建议时必须保留边界

## Compress：压缩

目标：把长课程压缩成可以管理的知识单元。

压缩层级：

```text
原始材料
  ↓
片段摘要
  ↓
逐课摘要
  ↓
模块摘要
  ↓
全课摘要
```

提取对象：

- 核心观点
- 概念定义
- 方法步骤
- 案例
- 公式/模型
- 金句
- 反复强调的原则
- 禁忌和边界

关键原则：

- 先局部，再整体
- 先事实，再解释
- 先保留老师原意，再做结构化重写

## Connect：关联

目标：从课程列表中重建知识地图。

关联类型：

- 概念到课程
- 案例到主题
- 主题到模块
- 模块到学习路径
- 金句到上下文
- 截图到知识点

输出形式：

- 课程体系图
- 概念词典
- 案例索引
- 主题图谱
- 学习路径
- 证据地图

关键原则：

- 课程不是线性的，学习路径可以是网络状
- 反复出现的概念往往是老师的核心方法论
- 板书和 PPT 通常是结构信号，需要优先进入知识地图

## Codify：技能化

目标：把课程知识封装成一个能被 Agent 调用的 Skill。

Skill 应具备：

- 课程问答能力
- 来源定位能力
- 概念检索能力
- 专题整理能力
- 学习路径生成能力
- 边界提醒能力

理想结构：

```text
<generated-skill>/
├── SKILL.md
├── references/
│   ├── course_digest.md
│   ├── lesson_index.json
│   ├── concept_glossary.md
│   ├── evidence_map.json
│   └── study_paths.md
└── scripts/
    └── search_course_notes.py
```

关键原则：

- Skill 不是资料夹，而是一套可调用行为
- Skill 应知道什么时候回答，什么时候引用，什么时候提醒边界
- Skill 应该优先基于课程证据，而不是自由发挥

## Evaluate：评估

目标：判断课程包是否足够可靠，适合生成哪类 Skill。

评估对象：

- 课时数量是否完整
- 是否有转录、视觉分析、截图、课程蒸馏
- 是否提取了概念、主题、方法、金句、学习路径
- 证据是文件级、课时级、时间点级还是原话级
- 高风险或专业边界是否被标注

当前实现：

```text
scripts/build_course_package.py
  ↓
course_package.json
  ↓
quality.counts
quality.missing_recommended_fields
quality.status
```

后续应增强：

- 引用准确率
- 学习检查覆盖率（仅在课程适合时）
- 概念覆盖率
- 片段级 evidence map
- 用户反馈回流

## 理论映射

| 理论 | 在项目中的作用 |
| --- | --- |
| ADDIE | C5 + Evaluate 的流程骨架 |
| Cognitive Apprenticeship | 捕捉老师的隐性思考、方法和边界 |
| SECI | 把课程经验转成显性知识资产 CoursePackage |
| Multimedia Learning | 同时保留转录和关键视觉证据 |
| RAG | Skill 回答时优先检索课程 references |
| Bloom Taxonomy | 不同 Skill mode 对应不同学习深度 |
