---
name: lineage-skill
description: Distills course materials into source-grounded AI agent skills. Use when the user wants to convert videos, audio, PDFs, slides, transcripts, OCR output, notes, or existing course distillation files into a CoursePackage and generated course-expert, study-coach, practitioner, citation-archive, knowledge-base, or domain-expert Skill.
---

# Lineage Skill

Turn course materials into reusable, source-grounded AI Skills.

Core method: **Capture -> Cite -> Compress -> Connect -> Codify -> Evaluate**.
Use this as an evidence-first workflow: preserve source material before summarizing, cite sources before synthesizing, and mark unsupported gaps.

## Read When Needed

- Method and evidence rules: [references/methodology.md](references/methodology.md)
- CoursePackage schema: [references/course-package.md](references/course-package.md)
- Mode selection: [references/skill-modes.md](references/skill-modes.md)
- Environment variables: [references/configuration.md](references/configuration.md)
- PDF/OCR workflow: [references/mineru-ocr.md](references/mineru-ocr.md)

## Trigger Conditions

Use this skill when the user asks to:

- Distill a course, lecture series, workshop, training program, curriculum, or long-form class.
- Convert videos, audio, PDFs, slides, screenshots, notes, transcripts, OCR output, or course summaries into structured course knowledge.
- Generate or update a course-backed Skill.
- Build a course expert, study coach, practitioner playbook, citation archive, knowledge base, or domain expert Skill.
- Package existing `transcripts/`, `analysis/`, `documents/`, `lesson_summaries.json`, `course_distillation_*.md/json`, or `course_package.json`.

## Decision Flow

1. Identify source state:
   - **Videos/audio only**: run the full pipeline.
   - **Videos plus PDFs**: run the full pipeline with document OCR if configured.
   - **Existing transcripts/OCR/notes**: skip capture; build package and Skill.
   - **Existing CoursePackage**: skip distillation; build or update Skill.
2. Choose mode:
   - Default: `course-expert`.
   - Add `practitioner` when the user wants checklists, playbooks, templates, or application workflows.
   - Add `study-coach` when the user wants review plans or learning paths.
   - Add `citation-archive` when strict quote/source lookup matters.
   - Read [references/skill-modes.md](references/skill-modes.md) for multi-course or domain modes.
3. Preserve evidence before summarizing.
4. Generate outputs.
5. Verify expected files exist and report paths.

## Workflows

### Full Course Pipeline

Use when raw course videos need transcription, visual analysis, distillation, packaging, and Skill generation.

```bash
python scripts/run_course_pipeline.py \
  --input-dir <course-video-dir> \
  --course-name <course-name> \
  --skill-name <skill-name> \
  --mode course-expert \
  --output-dir ./dist
```

With PDFs/OCR:

```bash
python scripts/run_course_pipeline.py \
  --input-dir <course-video-dir> \
  --documents-input <pdf-or-pdf-dir> \
  --course-name <course-name> \
  --skill-name <skill-name> \
  --mode course-expert,practitioner \
  --output-dir ./dist
```

Before using PDFs, check `MINERU_API_TOKEN`. If it is missing, read [references/mineru-ocr.md](references/mineru-ocr.md) and explain the fallback.

### Existing Materials

Use when the user already has transcripts, OCR, notes, summaries, or distillation outputs.

```bash
python scripts/build_course_package.py \
  --course-name <course-name> \
  --source-dir <course-dir>

python scripts/build_course_skill.py \
  --course-name <course-name> \
  --skill-name <skill-name> \
  --mode <mode> \
  --source-dir <course-dir> \
  --output-dir ./dist
```

### Existing CoursePackage

If `<course-dir>/course_package.json` already exists, run only `build_course_skill.py` unless the user asks to rebuild the package.

## Validation Loop

After generation, verify:

```text
<generated-skill>/
├── SKILL.md
├── agents/
├── references/
├── scripts/search_course_notes.py
└── lineage_manifest.json
```

Check:

- `references/course_package.json` exists.
- `references/evidence_map.json` exists.
- `references/lesson_index.json` exists.
- Mode-specific reference files exist for requested modes.
- `scripts/search_course_notes.py` is executable.

If validation fails, fix the missing artifact and rerun the smallest necessary command.

## Response Rules

- State which source state was detected and which workflow you used.
- Prefer the smallest pipeline that fits the user's materials.
- Name the generated Skill path and important reference files.
- Distinguish direct course content, course-grounded synthesis, and your own inference.
- If support is missing, say what evidence is missing.
- Never write real API keys into repository files or commit `.env`.
- Do not commit private transcripts, screenshots, OCR output, or course distillation artifacts unless the user explicitly wants to publish them.
- For medical, legal, financial, investment, or other high-stakes courses, keep answers educational and source-bounded.
