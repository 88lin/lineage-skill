# Configuration

Read only the variables needed for the selected workflow.

## Audio Transcription

Used by `scripts/transcribe_video.py`.

```bash
AUDIO_TRANSCRIBE_API_KEY=
AUDIO_TRANSCRIBE_BASE_URL=https://api.openai.com/v1
AUDIO_TRANSCRIBE_MODEL=whisper-1
```

## Vision Analysis

Used by `scripts/analyze_videos.py`.

```bash
LINEAGE_VISION_API_KEY=
LINEAGE_VISION_BASE_URL=https://api.openai.com/v1
LINEAGE_VISION_MODEL=gpt-4o
LINEAGE_VISION_TIMEOUT=600
```

## Text Distillation

Used by `scripts/distill_course.py`.

```bash
LINEAGE_TEXT_API_KEY=
LINEAGE_TEXT_BASE_URL=https://api.openai.com/v1
LINEAGE_TEXT_MODEL=gpt-4o
LINEAGE_TEXT_MAX_TOKENS=4096
LINEAGE_TEXT_TIMEOUT=300
DISTILL_USE_LLM=1
```

Set `DISTILL_USE_LLM=0` for local extractive fallback.

## PDF/OCR

Used by `scripts/parse_mineru_documents.py`.

```bash
MINERU_API_TOKEN=
MINERU_API_BASE=https://mineru.net/api/v4
MINERU_MODEL_VERSION=vlm
MINERU_ENABLE_FORMULA=false
MINERU_ENABLE_TABLE=false
MINERU_LANGUAGE=ch
```

## Local Tool Overrides

Used by media transcription and video analysis stages.

```bash
FFMPEG=
FFPROBE=
```

## Security

- Do not write real keys into repository files.
- Do not commit `.env`.
- Prefer agent config or system environment variables.
- Keep private course materials out of git unless explicitly authorized.
