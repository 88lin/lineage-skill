# 师承.skill / Lineage Skill

把一整门课，炼成可对话、可溯源、可复用的专家 Skill。

`师承.skill` 是一个课程蒸馏与 Skill 生成项目。它把视频课程转录、画面分析、关键截图、逐课摘要、课程级蒸馏笔记和证据索引，进一步包装成 AI Agent 可以调用的课程专家 Skill。

```text
Course video in, grounded expert skill out.
```

## 为什么有价值

高价值课程的问题通常不是“没有内容”，而是内容太长、线索太散、复习太慢、引用不清、学完后难以调用。

`师承.skill` 解决的是课程资产化问题：

- 把视频转成可检索文字
- 把 PPT、板书、图表、软件界面等关键画面抽出来
- 把逐课内容压缩成结构化摘要
- 把整门课重建成体系图、主题图谱、概念表、金句表和行动清单
- 把蒸馏结果封装成带来源意识的 Skill

它不是“生成一篇总结”，而是把课程变成一个可以追问、复习、回查证据、专题整理的知识系统。

理论上，它结合了教学设计、认知学徒制、知识管理、多媒体学习和 RAG。详细说明见 [THEORETICAL_FOUNDATION.md](./THEORETICAL_FOUNDATION.md)。

## 当前真实能力

这个仓库现在已经内置完整的视频课程主链路：

| 阶段 | 脚本 | 状态 |
| --- | --- | --- |
| 视频语音转录 | `scripts/transcribe_video.py` | 已有 |
| 视频画面分析 + 干货截图 | `scripts/analyze_videos.py` | 已有 |
| 转录 + 画面分析课程蒸馏 | `scripts/distill_course.py` | 已有 |
| 标准 CoursePackage 构建 | `scripts/build_course_package.py` | 已有 |
| 多模式 Skill 生成 | `scripts/build_course_skill.py` | 已有 |
| 一键流水线 | `scripts/run_course_pipeline.py` | 已有 |
| 本地关键词检索 | 生成到 Skill 的 `scripts/search_course_notes.py` | 已有 |

这些能力沉淀自真实课程蒸馏实践，但仓库本身只保留通用方法和通用流水线，不绑定任何既有课程、老师、领域或本地目录：大视频分片、720p/480p 压缩、音频转录、OpenAI-compatible 视觉分析、截图去重、LLM 课程蒸馏和本地抽取式 fallback。

文字资料、扫描 PDF、MinerU OCR 二次蒸馏已有参考实现来源，但还没有完全通用化进本仓库主命令；当前主线先聚焦视频课程到 Skill。

## C5 课程炼化框架

```text
Capture   采集：视频、音频、讲义、PDF、字幕、附件
Cite      溯源：课时、转录、截图、分析文件、时间点
Compress  压缩：逐课摘要、概念、案例、原则、边界
Connect   关联：课程模块、主题图谱、学习路径、证据地图
Codify    技能化：封装为 Agent 可调用 Skill
Evaluate  评估：完整性、证据强度、可用性和缺口
```

核心原则：先保留证据，再压缩；先逐课整理，再全局重建；最后把静态资料变成可调用能力，并用质量评估暴露缺口。

## 一键处理课程

准备一个包含 `.mp4` 的课程目录：

```bash
python scripts/run_course_pipeline.py \
  --input-dir /path/to/course-videos \
  --course-name "example-course" \
  --skill-name example-course \
  --mode course-expert \
  --output-dir ./dist \
  --chunk-minutes 8
```

流水线会依次执行：

```text
videos/*.mp4
  ↓
transcripts/*.json
  ↓
analysis/*_analysis.md + analysis/screenshots/
  ↓
lesson_summaries.json + course_distillation_<date>.md/json + full_transcript.md
  ↓
course_package.json
  ↓
dist/<skill-name>/SKILL.md + references/*
```

如果你已经有部分产物，可以跳过阶段：

```bash
python scripts/run_course_pipeline.py \
  --input-dir /path/to/course-videos \
  --course-name "example-course" \
  --skill-name example-course \
  --mode course-expert,study-coach \
  --skip-transcribe \
  --skip-analyze
```

## 分阶段运行

### 1. 转录

```bash
python scripts/transcribe_video.py \
  --input-dir /path/to/course-videos \
  --course-name "example-course"
```

输出：

```text
example-course/transcripts/*_transcript.json
```

长音频会自动分段转写。

### 2. 视频画面分析与截图

```bash
python scripts/analyze_videos.py \
  --input-dir /path/to/course-videos \
  --course-name "example-course" \
  --chunk-minutes 8
```

能力：

- 大视频自动压缩
- 长视频自动分片
- 识别 PPT、板书、图表、公式、软件界面等干货画面
- 从原视频抽帧
- 感知哈希去重

输出：

```text
example-course/analysis/*_analysis.md
example-course/analysis/screenshots/<video>/*.jpg
```

### 3. 课程蒸馏

```bash
python scripts/distill_course.py \
  --course-name "example-course"
```

输出：

```text
example-course/lesson_summaries.json
example-course/full_transcript.md
example-course/course_distillation_<date>.md
example-course/course_distillation_<date>.json
```

如果 `DISTILL_USE_LLM=0`，脚本会使用本地抽取式摘要 fallback，适合先跑通流程。

### 4. 生成 Skill

先生成标准中间层：

```bash
python scripts/build_course_package.py \
  --course-name "example-course" \
  --source-dir ./example-course
```

输出：

```text
example-course/course_package.json
```

再生成 Skill：

```bash
python scripts/build_course_skill.py \
  --course-name "example-course" \
  --skill-name example-course \
  --mode course-expert \
  --source-dir ./example-course \
  --output-dir ./dist
```

输出：

```text
dist/example-course/
├── SKILL.md
├── lineage_manifest.json
├── references/
│   ├── course_digest.md
│   ├── course_package.json
│   ├── full_transcript.md
│   ├── lesson_index.json
│   ├── concept_glossary.md
│   ├── evidence_map.json
│   ├── quote_index.md
│   └── study_paths.md
└── scripts/
    └── search_course_notes.py
```

构建器会优先复用已有 reference 文件；如果没有，会从最新 `course_distillation_*.md/json` 派生概念、金句、行动清单等内容；仍缺失的部分会生成占位文件，不伪造证据。

## CoursePackage

`course_package.json` 是通用课程蒸馏的中间层。它不绑定课程领域，统一表达：

```text
manifest, lessons, concepts, topics, cases, methods, learning_checks,
quotes, evidence, study_paths, boundaries, quality
```

多模式 Skill 生成器应该优先把 `course_package.json` 当作结构化入口，再回到 Markdown references 查细节和原文。

## Skill 生成模式

同一份课程蒸馏结果可以生成不同用途的 Skill：

| 模式 | 用途 |
| --- | --- |
| `course-expert` | 默认模式，回答课程问题、解释概念、回查课时和来源 |
| `study-coach` | 生成学习计划、复习路径、回忆/反思提示和薄弱点复盘 |
| `practitioner` | 把课程方法转为 playbook、checklist、template 和实操流程 |
| `citation-archive` | 强引用、强证据、原话检索和可审计笔记 |
| `knowledge-base` | 多课程知识库、概念别名、跨课程主题图谱 |
| `domain-expert` | 多课程沉淀后的领域专家、方法库、案例库和边界规则 |

模式可以组合：

```bash
python scripts/build_course_skill.py \
  --course-name "example-course" \
  --skill-name example-course-coach \
  --mode course-expert,study-coach \
  --source-dir ./example-course \
  --output-dir ./dist
```

详细设计见 [SKILL_MODES.md](./SKILL_MODES.md)。

## 环境变量

创建 `.env`：

```bash
# 语音转录：OpenAI-compatible /audio/transcriptions
AUDIO_TRANSCRIBE_API_KEY=xxx
AUDIO_TRANSCRIBE_BASE_URL=https://your-audio-endpoint/v1
AUDIO_TRANSCRIBE_MODEL=whisper-1

# 视频/图片分析：OpenAI-compatible chat completions with vision support
LINEAGE_VISION_API_KEY=xxx
LINEAGE_VISION_BASE_URL=https://your-vision-endpoint/v1
LINEAGE_VISION_MODEL=gpt-4o
LINEAGE_VISION_TIMEOUT=600

# 文本蒸馏：OpenAI-compatible chat completions
LINEAGE_TEXT_API_KEY=xxx
LINEAGE_TEXT_BASE_URL=https://your-text-endpoint/v1
LINEAGE_TEXT_MODEL=gpt-4o
LINEAGE_TEXT_MAX_TOKENS=4096
LINEAGE_TEXT_TIMEOUT=300

# 可选：不用 LLM，使用本地抽取式 fallback
DISTILL_USE_LLM=0
```

系统依赖：

- Python 3.11+
- `ffmpeg`
- `ffprobe`

Python 依赖：

```bash
pip install -r requirements.txt
```

如需处理 PDF/扫描件参考实现，还会用到 `PyMuPDF`、MinerU API 或视觉 OCR。

## 生成后的 Skill 怎么用

典型问题：

```text
这门课的核心框架是什么？
第 3 课主要讲了什么？
老师怎么解释某个概念？
把所有关于定价的内容整理成专题笔记。
这个结论来自哪一课、哪个截图或哪个转录文件？
我只有 2 小时，应该怎么复习这门课？
```

生成的 Skill 会要求 Agent 优先读取：

1. `course_digest.md`
2. `lesson_index.json`
3. `concept_glossary.md`
4. `evidence_map.json`
5. `quote_index.md`
6. `study_paths.md`
7. `full_transcript.md`

这让回答既能组织成专家视角，也能回到课程证据。

## 项目结构

```text
.
├── README.md
├── SKILL_MODES.md
├── THEORETICAL_FOUNDATION.md
├── METHODOLOGY.md
├── ROADMAP.md
├── examples/
│   ├── command-line-flow.txt
│   └── generated-skill-structure.txt
└── scripts/
    ├── analyze_videos.py
    ├── build_course_package.py
    ├── build_course_skill.py
    ├── distill_course.py
    ├── llm_client.py
    ├── run_course_pipeline.py
    └── transcribe_video.py
```

## 边界

当前项目已经具备视频课程主链路，但仍有几个明确边界：

- 依赖外部模型 API 和 `ffmpeg`
- 扫描 PDF / MinerU / 大规模文字资料蒸馏尚未完全通用化到主命令
- `evidence_map.json` 当前以文件级证据为主，后续要升级到片段级、时间点级和主题级
- 语义检索、向量索引、多课程知识库仍在路线图中
