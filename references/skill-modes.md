# Skill Modes

Default to `course-expert`. Combine modes only when the user asks for multiple behaviors.

## Modes

| Mode | Use When | Adds |
| --- | --- | --- |
| `course-expert` | Course Q&A, concept explanation, lesson lookup, source-backed notes | Base references only |
| `study-coach` | Study plans, review paths, recall prompts, weak-point review | `review_prompts.md`, `learning_plans.md`, `difficulty_map.json`, `learning_checks.json` |
| `practitioner` | Checklists, playbooks, templates, practical workflows | `playbooks.md`, `checklists.md`, `templates.md`, `case_index.json` |
| `citation-archive` | Strict source lookup, quotes, auditable notes | `source_manifest.json`, `confidence_rules.md` |
| `knowledge-base` | Multi-course catalog, concept aliases, cross-course topic maps | `course_catalog.json`, `cross_course_topics.json`, `concept_aliases.json`, `teacher_views.md` |
| `domain-expert` | Domain synthesis from one or more courses | `domain_map.md`, `method_library.md`, `case_library.json`, `source_courses.json`, `boundary_rules.md` |

## Selection Rules

- Use one focused mode when possible.
- Use `course-expert,practitioner` for "can answer questions and produce action checklists."
- Use `course-expert,study-coach` for "can answer questions and help me review."
- Use `citation-archive` when the user emphasizes exact wording, auditability, or source verification.
- Use `knowledge-base` or `domain-expert` only when the user has multiple courses or wants a broader domain Skill.

## Command Pattern

```bash
python scripts/build_course_skill.py \
  --course-name <course-name> \
  --skill-name <skill-name> \
  --mode course-expert,practitioner \
  --source-dir <course-dir> \
  --output-dir ./dist
```
