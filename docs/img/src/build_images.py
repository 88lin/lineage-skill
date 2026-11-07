#!/usr/bin/env python3
"""Build the README illustrations (Chinese and English SVGs).

Run:  python3 docs/img/src/build_images.py
Edit the text in COPY below, then re-run. Pillow is used only to measure
text so labels fit inside their boxes.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

from PIL import ImageFont

OUT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- design tokens
INK = "#17232E"
MUTED = "#5B6B78"
FAINT = "#8A97A3"
LINE = "#E3E7EA"
CARD = "#FFFFFF"
BG_A = "#F8FAF8"
BG_B = "#F4F2FA"

TEAL = ("#2F8F83", "#E8F4F1", "#BFE0D9")     # evidence
BLUE = ("#4C6FB8", "#ECF1FA", "#C9D6EE")     # teacher
VIOLET = ("#7B5BB5", "#F2EDF9", "#D9CCEE")   # practice
GREEN = ("#5E8C4A", "#EEF5EA", "#CFE2C5")    # personal
WARM = ("#C8732A", "#FCF1E6", "#F1D2B0")     # distill accent

FONT = ("'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC',"
        "'Noto Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif")
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'PingFang SC','Microsoft YaHei',monospace"

_FONT_FILES = [
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]
_cache: dict = {}


def _font(size: int, bold: bool):
    key = (size, bold)
    if key not in _cache:
        for path in _FONT_FILES:
            if Path(path).exists():
                # index 0 is regular; bold is approximated with a 6% widening
                _cache[key] = ImageFont.truetype(path, size, index=0)
                break
        else:
            _cache[key] = None
    return _cache[key]


def measure(text: str, size: int, bold: bool = False) -> float:
    f = _font(size, bold)
    if f is None:  # rough fallback: CJK ≈ 1em, Latin ≈ 0.56em
        w = sum(size if ord(c) > 0x2E80 else size * 0.56 for c in text)
    else:
        w = f.getlength(text)
    return w * (1.07 if bold else 1.0)


def wrap(text: str, size: int, width: float, bold: bool = False) -> list[str]:
    if "\n" in text:  # explicit line breaks
        return [ln for part in text.split("\n") for ln in wrap(part, size, width, bold)]
    cjk = any(ord(c) > 0x2E80 for c in text)
    tokens = list(text) if cjk else text.split(" ")
    sep = "" if cjk else " "
    lines, cur = [], ""
    for tok in tokens:
        trial = (cur + sep + tok) if cur else tok
        if measure(trial, size, bold) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = tok
    if cur:
        lines.append(cur)
    # keep CJK punctuation off the start of a line
    for i in range(1, len(lines)):
        while lines[i] and lines[i][0] in "，。、；：！？）》」":
            lines[i - 1] += lines[i][0]
            lines[i] = lines[i][1:]
    return lines


# ---------------------------------------------------------------- svg helpers
def t(x, y, s, size=16, weight=400, fill=INK, anchor="start", ls=0, family=None, extra=""):
    fam = f' font-family="{family}"' if family else ""
    lsp = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}"'
            f' text-anchor="{anchor}"{lsp}{fam}{extra}>{escape(s)}</text>')


def lines_at(x, y, lines, size, lh, **kw):
    return "".join(t(x, y + i * lh, s, size, **kw) for i, s in enumerate(lines))


def rect(x, y, w, h, r=16, fill=CARD, stroke=LINE, sw=1, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}"{st}{extra}/>'


def pill(x, y, s, color, size=13, h=30, padx=14, ls=1.2, weight=700, solid=False):
    w = measure(s, size, True) + ls * len(s) + padx * 2
    fg, tint, border = color
    out = rect(x, y, w, h, h / 2, fg if solid else tint, None if solid else border)
    out += t(x + w / 2, y + h / 2 + size * 0.36, s, size, weight, "#FFFFFF" if solid else fg, "middle", ls)
    return out, w


def chip(x, y, s, color, size=15, h=38, padx=14):
    w = measure(s, size, True) + padx * 2
    fg, tint, border = color
    out = rect(x, y, w, h, 10, tint, border)
    out += t(x + w / 2, y + h / 2 + size * 0.36, s, size, 600, INK, "middle")
    return out, w


def arrow(x1, y1, x2, y2, color=FAINT, sw=2):
    return (f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{color}" stroke-width="{sw}"'
            f' stroke-linecap="round" marker-end="url(#arrow)"/>')


def frame(w, h, title, desc, body, lang):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc" lang="{lang}">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(desc)}</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG_A}"/><stop offset="1" stop-color="{BG_B}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.85" cy="0.1" r="0.6">
      <stop offset="0" stop-color="#DDEFEA" stop-opacity="0.9"/><stop offset="1" stop-color="#DDEFEA" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-40%" width="140%" height="200%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#1B2B3A" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M1 1L9 5 1 9" fill="none" stroke="{FAINT}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <rect width="{w}" height="{h}" rx="28" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" rx="28" fill="url(#glow)"/>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="27.5" fill="none" stroke="#E6E3DC"/>
  <g font-family="{FONT}">
{body}
  </g>
</svg>
'''


def heading(title, sub, y=92):
    return t(72, y, title, 40, 750, INK, ls=-0.5) + t(72, y + 42, sub, 18, 400, MUTED)


# ---------------------------------------------------------------- copy
COPY = {
    "zh": {
        "hero": {
            "badge": "TEACHER-TO-SKILLS",
            "h1": ["把老师，", "蒸馏成 Skill。"], "h1_size": 78, "accent": "Skill",
            "sub": ["提炼老师怎么看、怎么判断、怎么纠错，", "变成一位会示范、会纠错、最终放手的 AI 老师。"],
            "chips": ["有出处", "先练后评", "逐步放手"],
            "materials": ["课程视频", "书与讲义", "录音访谈", "笔记批注"],
            "distill": "蒸馏",
            "card": "产品分析课 · 老师 Skill",
            "teacher": "AI 老师", "you": "你",
            "q": "这个需求，你会先看什么？",
            "a": "先看用户量和增长。",
            "fb": "先别急着看数据。老师的第一步是：谁、在什么场景下被卡住了？",
            "src": "出处 · 第 2 讲 08:15",
            "input": "写下你的判断……",
            "title": "Teacher-to-Skills：把老师蒸馏成 Skill",
        },
        "distill": {
            "title": "不是总结课程，而是蒸馏老师",
            "sub": "把老师没写下来的判断方式，提炼成能回查、能练习的 Skill",
            "left": "老师的材料",
            "materials": ["课程视频", "书与讲义", "录音访谈", "文章笔记", "批注反馈"],
            "mid": "蒸馏", "steps": ["转录识别", "标注出处", "提炼方法"],
            "right": "蒸馏出的东西",
            "cards": [
                ("出处", "每条结论对应的原文、原话、讲义页或画面"),
                ("观察点", "面对一个问题，老师先看什么、盯住什么"),
                ("判断规则", "凭哪些条件下结论，遇到例外怎么处理"),
                ("示范", "老师完整做一遍的过程和其中的关键步骤"),
                ("常见错误与纠偏", "学生通常错在哪里，老师会怎样指出"),
                ("适用边界", "什么情况下这套方法不能用"),
            ],
            "from": "摘要只留下：老师讲了什么", "to": "蒸馏留下：老师会怎么做",
        },
        "layers": {
            "title": "从老师的材料，到你自己的能力",
            "sub": "老师那一侧可回查、生成后不改动；你这一侧私有，持续积累",
            "layers": [
                ("证据层", "原文、原话和画面，每条结论都能回查",
                 ["转录文字", "讲义页码", "关键画面", "原话出处"]),
                ("老师层", "老师怎么看、怎么判断、怎么纠错",
                 ["观察点", "判断规则", "示范", "纠错方式", "适用边界"]),
                ("练习层", "按顺序练，先做后评，逐步放手",
                 ["摸底", "先做后评", "最小提示", "间隔复习", "换场景检验"]),
                ("个人层", "你的尝试和结果，经你同意沉淀成自己的方法",
                 ["尝试记录", "错误与修订", "复习计划", "真实结果", "个人方法"]),
            ],
            "b1": ["老师 Skill", "生成后不改动", "随时回查出处"],
            "b2": ["你的学习记录", "私有", "存在 Skill 之外"],
        },
        "journey": {
            "title": "老师先扶着你，再慢慢放手",
            "sub": "提示一点点减少，你的独立能力一点点显现",
            "steps": [
                ("定目标", "目标、基础、\n真实场景"),
                ("看示范", "老师怎么看、\n怎么判断"),
                ("跟着做", "有模板，\n也有提示"),
                ("被纠偏", "每次只抓\n最关键的问题"),
                ("独立做", "自己定方案，\n自己完成"),
                ("换场景", "没见过的问题\n也会做"),
                ("出师检验", "不给提示，\n隔段时间再测"),
                ("持续精进", "形成你\n自己的方法"),
            ],
            "up": "你的独立程度",
            "bar": "老师的支持", "bar_l": "完整示范 + 提示", "bar_r": "只给最终反馈",
        },
        "lesson": {
            "title": "一节课怎么上",
            "sub": "讲清一个知识点，一起出两道题，分别点评，记下你的进度",
            "cards": [
                ("选一个知识点", "只讲你现在最需要的"),
                ("讲清楚", "先讲直觉，再讲准确"),
                ("画出来", "终端 ASCII 或 SVG 图示"),
                ("出两道题", "一起给出，等你作答"),
            ],
            "map": [("✓", "观察点", "已掌握"), ("●", "判断规则", "今天"), ("○", "示范", "之后")],
            "explain": ["直觉", "准确定义", "例子", "反例", "三点小结"],
            "ascii": ["观察 ──▶ 判断 ──▶ 验证", "  │", "  └─ 复杂关系 → SVG"],
            "ascii_note": "任何终端里都能看清",
            "qs": [("① 检查理解", "这条规则在什么条件下成立？"), ("② 检查应用", "换到这个案例，你会怎么判断？")],
            "q_note": "不提前给答案",
            "flow": ["点评第 1 题", "点评第 2 题", "记录错误与修订", "进入下一个知识点"],
        },
    },
    "en": {
        "hero": {
            "badge": "TEACHER-TO-SKILLS",
            "h1": ["Distill your teacher", "into a Skill."], "h1_size": 66, "accent": "Skill",
            "sub": ["Capture how your teacher sees, judges, and corrects,", "then learn it until you can work on your own."],
            "chips": ["Source-backed", "Try first", "Hints fade"],
            "materials": ["Course videos", "Books & handouts", "Recordings", "Notes & feedback"],
            "distill": "Distill",
            "card": "Product Analysis · Teacher Skill",
            "teacher": "AI teacher", "you": "You",
            "q": "What would you look at first here?",
            "a": "User numbers and growth.",
            "fb": "Hold the data for now. The teacher's first step: who is blocked, and in what situation?",
            "src": "Source · Lesson 2, 08:15",
            "input": "Write down your judgment…",
            "title": "Teacher-to-Skills: distill your teacher into a Skill",
        },
        "distill": {
            "title": "Not a course summary. A distilled teacher.",
            "sub": "The judgment your teacher never wrote down, turned into a Skill you can check and practice",
            "left": "Teacher's material",
            "materials": ["Course videos", "Books & handouts", "Recordings", "Articles & notes", "Written feedback"],
            "mid": "Distill", "steps": ["Transcribe", "Cite sources", "Extract method"],
            "right": "What gets distilled",
            "cards": [
                ("Sources", "The passage, quote, page, or frame behind each claim"),
                ("Focus points", "What the teacher looks at first and watches closely"),
                ("Judgment rules", "What a conclusion rests on, and how exceptions work"),
                ("Demonstrations", "The teacher's full worked approach and its key steps"),
                ("Mistakes & corrections", "Where students slip, and how the teacher points it out"),
                ("Boundaries", "When the method does not apply"),
            ],
            "from": "A summary keeps what the teacher said", "to": "Distilling keeps what the teacher would do",
        },
        "layers": {
            "title": "From your teacher's material to your own ability",
            "sub": "The teacher's side stays traceable and fixed. Your side stays private and keeps growing.",
            "layers": [
                ("Evidence", "Every claim traces back to its source",
                 ["Transcripts", "Handout pages", "Key frames", "Quoted sources"]),
                ("Teacher", "How the teacher sees, judges, and corrects",
                 ["Focus points", "Judgment rules", "Demos", "Corrections", "Boundaries"]),
                ("Practice", "Ordered practice: try first, then feedback",
                 ["Baseline", "Try first", "Minimal hints", "Spaced review", "Transfer checks"]),
                ("Personal", "Your attempts and results, kept private",
                 ["Attempts", "Mistakes & fixes", "Review plan", "Real results", "Your method"]),
            ],
            "b1": ["Teacher Skill", "Fixed once built", "Always traceable"],
            "b2": ["Your records", "Private", "Outside the Skill"],
        },
        "journey": {
            "title": "Your teacher holds on, then lets go",
            "sub": "Hints fade step by step as your own ability shows",
            "steps": [
                ("Set goals", "Goal, level, and a real use"),
                ("Watch", "How the teacher sees and judges"),
                ("Follow along", "With a template and hints"),
                ("Get corrected", "One key issue at a time"),
                ("Work alone", "Your own plan, your own work"),
                ("New context", "Problems you have not seen"),
                ("Graduate", "No hints, tested after a delay"),
                ("Keep growing", "Form your own method"),
            ],
            "up": "Your independence",
            "bar": "Teacher support", "bar_l": "Full demo + hints", "bar_r": "Final feedback only",
        },
        "lesson": {
            "title": "How one lesson works",
            "sub": "Explain one concept, ask two questions together, give feedback on each, record progress",
            "cards": [
                ("Pick one concept", "Only what you need now"),
                ("Explain it well", "Plain first, then precise"),
                ("Show it", "Terminal ASCII or SVG"),
                ("Ask two questions", "Shown together, then you answer"),
            ],
            "map": [("✓", "Focus points", "done"), ("●", "Judgment rules", "today"), ("○", "Demonstrations", "later")],
            "explain": ["Intuition", "Precise definition", "Example", "Counterexample", "Three-point recap"],
            "ascii": ["observe ──▶ judge ──▶ check", "   │", "   └─ complex → SVG"],
            "ascii_note": "Readable in any terminal",
            "qs": [("① Understanding", "When does this rule hold?"), ("② Application", "How would you judge this case?")],
            "q_note": "No answers before you try",
            "flow": ["Feedback on Q1", "Feedback on Q2", "Log mistakes & fixes", "Next concept"],
        },
    },
}


# ---------------------------------------------------------------- images
def hero(c, lang):
    W, H = 1440, 640
    b = []
    p, _ = pill(72, 72, c["badge"], TEAL, size=13, h=32, ls=2)
    b.append(p)
    size = c["h1_size"]
    y = 196
    for line in c["h1"]:
        if c["accent"] in line:
            pre, post = line.split(c["accent"], 1)
            b.append(f'<text x="72" y="{y}" font-size="{size}" font-weight="800" fill="{INK}" letter-spacing="-1.5">'
                     f'{escape(pre)}<tspan fill="{TEAL[0]}">{escape(c["accent"])}</tspan>{escape(post)}</text>')
        else:
            b.append(t(72, y, line, size, 800, INK, ls=-1.5))
        y += size * 1.18
    y += 18 - size * 0.18
    b.append(lines_at(72, y, c["sub"], 23, 36, weight=400, fill=MUTED))
    x, cy = 72, y + 84
    for s, col in zip(c["chips"], (TEAL, BLUE, VIOLET)):
        w = measure(s, 16, True) + 54
        b.append(rect(x, cy, w, 42, 21, CARD, col[2]))
        b.append(f'<circle cx="{x + 22}" cy="{cy + 21}" r="9" fill="{col[1]}" stroke="{col[0]}" stroke-width="1.5"/>')
        b.append(f'<path d="M{x + 17.5} {cy + 21}l3 3 5.5-6" fill="none" stroke="{col[0]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append(t(x + 38, cy + 27, s, 16, 600, INK))
        x += w + 12

    card_x, card_w = 992, 376
    chat, card_h = _chat(c, card_x, 0, card_w)
    card_y = (H - card_h) / 2
    chat, card_h = _chat(c, card_x, card_y, card_w)

    # material chips flowing into the Skill card
    mw = max(measure(m, 15, True) for m in c["materials"]) + 40
    mx = card_x - 88 - mw
    node_x, node_y = card_x - 44, card_y + card_h / 2
    n = len(c["materials"])
    for i, m in enumerate(c["materials"]):
        my = node_y - (n * 66 - 22) / 2 + i * 66
        col = (TEAL, BLUE, VIOLET, GREEN)[i]
        b.append(rect(mx, my, mw, 44, 12, CARD, LINE, extra=' filter="url(#shadow)"'))
        b.append(f'<rect x="{mx + 14}" y="{my + 15}" width="14" height="14" rx="4" fill="{col[1]}" stroke="{col[0]}"/>')
        b.append(t(mx + 38, my + 27, m, 15, 600, INK))
        sx, sy = mx + mw, my + 22
        b.append(f'<path d="M{sx} {sy}C{sx + 30} {sy} {node_x - 30} {node_y} {node_x - 20} {node_y}" fill="none" stroke="{WARM[2]}" stroke-width="2"/>')
    b.append(f'<circle cx="{node_x}" cy="{node_y}" r="20" fill="{WARM[1]}" stroke="{WARM[0]}" stroke-width="2"/>')
    b.append(f'<path d="M{node_x - 7} {node_y - 7}h14l-5 7v6h-4v-6z" fill="{WARM[0]}"/>')
    b.append(t(node_x, node_y - 32, c["distill"], 14, 700, WARM[0], "middle"))
    b.append(arrow(node_x + 20, node_y, card_x - 6, node_y, WARM[0]))
    b.extend(chat)
    return frame(W, H, c["title"], " ".join(c["h1"] + c["sub"]), "\n".join(b), lang)


def _chat(c, card_x, card_y, card_w):
    """Chat window for the hero. Returns (svg parts, card height)."""
    parts = []
    bx, inner = card_x + 22, card_w - 44
    yy = card_y + 90

    def bubble(text, who, right=False, tint=BLUE[1], border=BLUE[2], extra_h=0):
        nonlocal yy
        maxw = inner - 40
        ls = wrap(text, 15, maxw - 28)
        w = min(maxw, max(measure(s, 15) for s in ls) + 28)
        h = 18 + len(ls) * 22 + extra_h
        x = bx + inner - w if right else bx
        out = t(x + (w if right else 0), yy - 8, who, 12, 600, FAINT, "end" if right else "start")
        out += rect(x, yy, w, h, 14, tint, border)
        out += lines_at(x + 14, yy + 27, ls, 15, 22, fill=INK)
        top = yy
        yy += h + 34
        return out, x, top, len(ls)

    body = []
    o, *_ = bubble(c["q"], c["teacher"]); body.append(o)
    o, *_ = bubble(c["a"], c["you"], True, "#F3F5F6", LINE); body.append(o)
    o, x, top, n = bubble(c["fb"], c["teacher"], extra_h=40); body.append(o)
    sp, _ = pill(x + 14, top + 18 + n * 22 + 6, c["src"], TEAL, size=12, h=26, padx=10, ls=0, weight=600)
    body.append(sp)
    iy = yy - 10
    card_h = iy + 44 + 22 - card_y

    parts.append(rect(card_x, card_y, card_w, card_h, 22, CARD, LINE, extra=' filter="url(#shadow)"'))
    parts.append(f'<path d="M{card_x} {card_y + 22}a22 22 0 0 1 22-22h{card_w - 44}a22 22 0 0 1 22 22v32h-{card_w}z" fill="#F6F8F9"/>')
    parts.append(f'<path d="M{card_x} {card_y + 54}h{card_w}" stroke="{LINE}"/>')
    for i, col in enumerate(("#E8796B", "#E9B949", "#6CC07A")):
        parts.append(f'<circle cx="{card_x + 24 + i * 16}" cy="{card_y + 27}" r="5" fill="{col}"/>')
    parts.append(t(card_x + 82, card_y + 32, c["card"], 14, 600, MUTED))
    parts.extend(body)
    parts.append(rect(bx, iy, inner, 44, 12, "#F8FAFA", LINE))
    parts.append(t(bx + 16, iy + 28, c["input"], 14, 400, FAINT))
    parts.append(f'<circle cx="{bx + inner - 24}" cy="{iy + 22}" r="13" fill="{TEAL[0]}"/>')
    parts.append(f'<path d="M{bx + inner - 29} {iy + 22}h10m-4-4 4 4-4 4" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    return parts, card_h


def distill(c, lang):
    W, H = 1440, 760
    b = [heading(c["title"], c["sub"])]
    top = 188
    # left: materials
    b.append(t(72, top + 14, c["left"], 14, 700, FAINT, ls=1))
    for i, m in enumerate(c["materials"]):
        y = top + 34 + i * 70
        col = (TEAL, BLUE, VIOLET, GREEN, WARM)[i]
        b.append(rect(72, y, 300, 56, 14, CARD, LINE, extra=' filter="url(#shadow)"'))
        b.append(f'<rect x="90" y="{y + 16}" width="24" height="24" rx="7" fill="{col[1]}" stroke="{col[0]}"/>')
        b.append(t(128, y + 34, m, 17, 600, INK))
        b.append(f'<path d="M372 {y + 28}C410 {y + 28} 420 {top + 205} 459 {top + 205}" fill="none" stroke="{WARM[2]}" stroke-width="2"/>')
    # middle: funnel
    fx, fy = 436, top + 40
    b.append(f'<path d="M{fx} {fy}H{fx + 196}L{fx + 150} {fy + 330}H{fx + 46}Z" fill="{WARM[1]}" stroke="{WARM[2]}" stroke-width="1.5" stroke-linejoin="round"/>')
    b.append(t(fx + 98, fy + 52, c["mid"], 24, 800, WARM[0], "middle"))
    for i, s in enumerate(c["steps"]):
        yy = fy + 110 + i * 70
        b.append(f'<path d="M{fx + 34 + i * 12} {yy - 26}H{fx + 162 - i * 12}" stroke="{WARM[2]}" stroke-dasharray="4 5"/>')
        b.append(t(fx + 98, yy + 6, s, 15, 600, INK, "middle"))
    b.append(arrow(fx + 175, top + 205, 662, top + 205, WARM[0]))
    # right: six cards
    rx = 676
    b.append(t(rx, top + 14, c["right"], 14, 700, FAINT, ls=1))
    cw, ch, gap = 336, 116, 20
    cols = (TEAL, BLUE, BLUE, BLUE, VIOLET, WARM)
    for i, (name, desc) in enumerate(c["cards"]):
        x = rx + (i % 2) * (cw + gap)
        y = top + 34 + (i // 2) * (ch + 18)
        col = cols[i]
        b.append(rect(x, y, cw, ch, 16, CARD, LINE, extra=' filter="url(#shadow)"'))
        b.append(f'<rect x="{x}" y="{y + 20}" width="5" height="{ch - 40}" rx="2.5" fill="{col[0]}"/>')
        b.append(t(x + 26, y + 40, name, 19, 700, INK))
        b.append(lines_at(x + 26, y + 68, wrap(desc, 15, cw - 50), 15, 23, fill=MUTED))
    # bottom contrast strip
    sy = 648
    b.append(rect(72, sy, 1296, 64, 18, CARD, LINE))
    b.append(t(104, sy + 39, c["from"], 18, 500, FAINT))
    fw = measure(c["from"], 18)
    b.append(arrow(104 + fw + 24, sy + 33, 104 + fw + 84, sy + 33, WARM[0]))
    b.append(t(104 + fw + 104, sy + 39, c["to"], 18, 750, TEAL[0]))
    return frame(W, H, c["title"], c["sub"], "\n".join(b), lang)


def layers(c, lang):
    W, H = 1440, 790
    b = [heading(c["title"], c["sub"])]
    x0, w, lh, gap, top = 72, 1100, 120, 22, 184
    cols = (TEAL, BLUE, VIOLET, GREEN)
    for i, (name, desc, chips) in enumerate(c["layers"]):
        y = top + i * (lh + gap)
        col = cols[i]
        personal = i == 3
        extra = ' stroke-dasharray="6 6"' if personal else ' filter="url(#shadow)"'
        b.append(rect(x0, y, w, lh, 18, col[1] if personal else CARD, col[2] if personal else LINE, 1.5 if personal else 1, extra))
        b.append(f'<rect x="{x0}" y="{y + 18}" width="6" height="{lh - 36}" rx="3" fill="{col[0]}"/>')
        b.append(f'<circle cx="{x0 + 46}" cy="{y + 44}" r="17" fill="{col[1]}" stroke="{col[0]}" stroke-width="1.5"/>')
        b.append(t(x0 + 46, y + 50, f"0{i + 1}", 14, 700, col[0], "middle"))
        b.append(t(x0 + 76, y + 51, name, 23, 750, INK))
        b.append(lines_at(x0 + 30, y + 92, wrap(desc, 15, 330), 15, 22, fill=MUTED))
        # chips, flowing into up to two rows
        cx, cy, right = x0 + 400, y + 22, x0 + w - 24
        widths = [measure(s, 15, True) + 28 for s in chips]
        rows, row, used = [], [], 0
        for s, cw in zip(chips, widths):
            if row and used + cw > right - cx:
                rows.append(row); row, used = [], 0
            row.append((s, cw)); used += cw + 12
        rows.append(row)
        cy = y + (lh - (len(rows) * 38 + (len(rows) - 1) * 10)) / 2
        for r in rows:
            xx = cx
            for s, cw in r:
                o, _ = chip(xx, cy, s, col)
                b.append(o)
                xx += cw + 12
            cy += 48
        if i < 3:
            ay = y + lh + 2
            b.append(f'<path d="M{x0 + 46} {ay}v{gap - 4}" stroke="{FAINT}" stroke-width="2" marker-end="url(#arrow)"/>')
    # brackets
    bx = x0 + w + 26
    for (y1, y2, labels, col) in ((top, top + 3 * lh + 2 * gap, c["b1"], BLUE), (top + 3 * (lh + gap), top + 4 * lh + 3 * gap, c["b2"], GREEN)):
        b.append(f'<path d="M{bx} {y1 + 6}h8v{y2 - y1 - 12}h-8" fill="none" stroke="{col[0]}" stroke-width="2" stroke-linejoin="round"/>')
        mid = (y1 + y2) / 2
        b.append(t(bx + 24, mid - 16, labels[0], 18, 750, col[0]))
        b.append(t(bx + 24, mid + 10, labels[1], 14, 500, MUTED))
        b.append(t(bx + 24, mid + 32, labels[2], 14, 500, MUTED))
    return frame(W, H, c["title"], c["sub"], "\n".join(b), lang)


def journey(c, lang):
    W, H = 1440, 610
    b = [heading(c["title"], c["sub"])]
    n, gap, x0 = 8, 14, 72
    cw = (1296 - gap * (n - 1)) / n
    base = 470
    cols = (TEAL, TEAL, BLUE, BLUE, VIOLET, VIOLET, GREEN, GREEN)
    for i, (name, desc) in enumerate(c["steps"]):
        h = 150 + i * 20
        x, y = x0 + i * (cw + gap), base - h
        col = cols[i]
        b.append(rect(x, y, cw, h, 16, CARD, LINE, extra=' filter="url(#shadow)"'))
        b.append(f'<rect x="{x}" y="{y + 18}" width="5" height="{h - 36}" rx="2.5" fill="{col[0]}"/>')
        b.append(f'<circle cx="{x + 30}" cy="{y + 40}" r="15" fill="{col[1]}" stroke="{col[0]}" stroke-width="1.5"/>')
        b.append(t(x + 30, y + 45, str(i + 1), 14, 700, col[0], "middle"))
        size = 18
        while measure(name, size, True) > cw - 32 and size > 14:
            size -= 1
        b.append(t(x + 16, y + 86, name, size, 750, INK))
        b.append(lines_at(x + 16, y + 112, wrap(desc, 14, cw - 30), 14, 21, fill=MUTED))
    # independence arrow
    b.append(f'<path d="M{x0 + cw / 2} {base - 150 - 26}L{x0 + 7 * (cw + gap) + cw / 2 - 20} {base - 290 - 26}" stroke="{TEAL[2]}" stroke-width="2" stroke-dasharray="5 6" marker-end="url(#arrow)"/>')
    b.append(t(x0 + 6.6 * (cw + gap), base - 290 - 40, c["up"], 14, 700, TEAL[0], "end"))
    # support bar
    by = 508
    b.append('<defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#2F8F83" stop-opacity="0.85"/>'
             '<stop offset="1" stop-color="#2F8F83" stop-opacity="0.08"/></linearGradient></defs>')
    b.append(t(x0, by - 10, c["bar"], 13, 700, FAINT, ls=1))
    b.append(rect(x0, by, 1296, 12, 6, "url(#fade)", None))
    b.append(t(x0, by + 38, c["bar_l"], 14, 500, MUTED))
    b.append(t(x0 + 1296, by + 38, c["bar_r"], 14, 500, MUTED, "end"))
    return frame(W, H, c["title"], c["sub"], "\n".join(b), lang)


def lesson(c, lang):
    W, H = 1440, 740
    b = [heading(c["title"], c["sub"])]
    cw, gap, top, ch = 300, 32, 184, 300
    cols = (TEAL, BLUE, VIOLET, WARM)
    xs = [72 + i * (cw + gap) for i in range(4)]
    for i, (name, sub) in enumerate(c["cards"]):
        x, col = xs[i], cols[i]
        b.append(rect(x, top, cw, ch, 20, CARD, LINE, extra=' filter="url(#shadow)"'))
        p, _ = pill(x + 22, top + 22, f"0{i + 1}", col, size=12, h=26, padx=10, ls=1)
        b.append(p)
        b.append(t(x + 22, top + 82, name, 23, 750, INK))
        b.append(t(x + 22, top + 108, sub, 14, 500, MUTED))
        if i < 3:
            b.append(arrow(x + cw + 6, top + ch / 2, x + cw + gap - 8, top + ch / 2))
    # card 1: concept map
    x, y = xs[0] + 22, top + 140
    for k, (mark, name, state) in enumerate(c["map"]):
        yy = y + k * 46
        on = k == 1
        b.append(rect(x, yy, cw - 44, 38, 10, TEAL[1] if on else "#F7F9F9", TEAL[2] if on else LINE))
        b.append(t(x + 14, yy + 25, mark, 15, 700, TEAL[0] if k < 2 else FAINT))
        b.append(t(x + 38, yy + 25, name, 15, 650 if on else 500, INK if k < 2 else MUTED))
        b.append(t(x + cw - 58, yy + 25, state, 13, 600, TEAL[0] if on else FAINT, "end"))
    # card 2: explanation ladder
    x, y = xs[1] + 34, top + 146
    b.append(f'<path d="M{x} {y}v{4 * 30}" stroke="{BLUE[2]}" stroke-width="2"/>')
    for k, s in enumerate(c["explain"]):
        yy = y + k * 30
        b.append(f'<circle cx="{x}" cy="{yy}" r="7" fill="{CARD}" stroke="{BLUE[0]}" stroke-width="2"/>')
        b.append(t(x + 20, yy + 5, s, 15, 500, INK))
    # card 3: terminal
    x, y = xs[2] + 22, top + 138
    b.append(rect(x, y, cw - 44, 112, 12, "#1E2830", None))
    for k, s in enumerate(c["ascii"]):
        b.append(t(x + 16, y + 34 + k * 24, s, 14, 500, "#CFE7E1" if k == 0 else "#9FB3C2", family=MONO, extra=' xml:space="preserve"'))
    b.append(t(x, y + 140, c["ascii_note"], 13, 500, FAINT))
    # card 4: two questions
    x, y = xs[3] + 22, top + 132
    for k, (q, s) in enumerate(c["qs"]):
        yy = y + k * 66
        col = (VIOLET, BLUE)[k]
        b.append(rect(x, yy, cw - 44, 58, 12, col[1], col[2]))
        b.append(t(x + 14, yy + 24, q, 14, 700, col[0]))
        b.append(t(x + 14, yy + 45, wrap(s, 14, cw - 72)[0], 14, 500, INK))
    b.append(t(x, y + 150, c["q_note"], 13, 500, FAINT))
    # feedback flow
    fy, fh = 560, 110
    sw = (1296 - 48 - 3 * 56) / 4
    first_cx = 96 + sw / 2
    mid_y = (top + ch + fy) / 2
    b.append(f'<path d="M{xs[3] + cw / 2} {top + ch + 6}V{mid_y}H{first_cx}V{fy - 8}" fill="none" stroke="{FAINT}"'
             f' stroke-width="2" stroke-linejoin="round" marker-end="url(#arrow)"/>')
    b.append(rect(72, fy, 1296, fh, 22, CARD, LINE, extra=' filter="url(#shadow)"'))
    fcol = (VIOLET, BLUE, TEAL, GREEN)
    for k, s in enumerate(c["flow"]):
        sx = 96 + k * (sw + 56)
        col = fcol[k]
        b.append(rect(sx, fy + 24, sw, fh - 48, 14, col[1], col[2]))
        b.append(t(sx + sw / 2, fy + fh / 2 + 6, s, 16, 650, INK, "middle"))
        if k < 3:
            b.append(arrow(sx + sw + 12, fy + fh / 2, sx + sw + 44, fy + fh / 2))
    return frame(W, H, c["title"], c["sub"], "\n".join(b), lang)


def main() -> None:
    builders = {"hero": hero, "distill": distill, "layers": layers, "journey": journey, "lesson": lesson}
    for lang, copy in COPY.items():
        for name, fn in builders.items():
            path = OUT / f"{name}-{lang}.svg"
            path.write_text(fn(copy[name], lang), encoding="utf-8")
            print("wrote", path.relative_to(OUT.parent.parent))


if __name__ == "__main__":
    main()
