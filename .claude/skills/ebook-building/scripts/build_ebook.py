#!/usr/bin/env python3
"""Assemble chapter markdown files into a single self-contained HTML e-book.

Usage:
    python3 build_ebook.py --outline <outline.md> --chapters <dir> --out <file.html>

Uses the `markdown` package when available; otherwise falls back to a built-in
mini converter (headings, paragraphs, fenced code, tables, lists, blockquote
callouts, <details>). No external CSS/JS/font URLs — the output is one file.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

try:
    import markdown as _md  # type: ignore

    def md_to_html(text: str) -> str:
        return _md.markdown(text, extensions=["tables", "fenced_code"])
except ImportError:
    def md_to_html(text: str) -> str:
        return _mini_convert(text)


def _inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def _mini_convert(text: str) -> str:
    out: list[str] = []
    lines = text.splitlines()
    i = 0
    para: list[str] = []

    def flush_para() -> None:
        if para:
            out.append(f"<p>{_inline(' '.join(para))}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        fence = re.match(r"^```(\w+)?(.*)$", stripped)
        if fence and stripped.startswith("```"):
            flush_para()
            lang = fence.group(1) or ""
            body: list[str] = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                body.append(lines[i])
                i += 1
            code = html.escape("\n".join(body))
            out.append(f'<pre class="lang-{lang}"><code>{code}</code></pre>')
        elif stripped.startswith("#"):
            flush_para()
            level = len(stripped) - len(stripped.lstrip("#"))
            out.append(f"<h{level}>{_inline(stripped[level:].strip())}</h{level}>")
        elif stripped.startswith("|") and i + 1 < len(lines) and set(lines[i + 1].strip()) <= set("|-: "):
            flush_para()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            i -= 1
            thead = "".join(f"<th>{_inline(c)}</th>" for c in rows[0])
            body_rows = "".join(
                "<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>"
                for r in rows[2:])
            out.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{body_rows}</tbody></table>")
        elif stripped.startswith(">"):
            flush_para()
            quote: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            i -= 1
            cls = "callout-warn" if "⚠️" in quote[0] else "callout-aice" if "🎯" in quote[0] else "callout"
            inner = "<br>".join(_inline(q) for q in quote if q)
            out.append(f'<blockquote class="{cls}">{inner}</blockquote>')
        elif re.match(r"^[-*]\s+", stripped):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(f"<li>{_inline(lines[i].strip()[2:])}</li>")
                i += 1
            i -= 1
            out.append("<ul>" + "".join(items) + "</ul>")
        elif stripped.startswith("<details") or stripped.startswith("</details") or stripped.startswith("<summary"):
            flush_para()
            out.append(stripped)
        elif not stripped:
            flush_para()
        else:
            para.append(stripped)
        i += 1
    flush_para()
    return "\n".join(out)


CSS = """
:root{--bg:#fdfcf9;--fg:#1e2430;--muted:#5b6472;--surface:#f3f1ea;--border:#e2ded2;
--py:#3776ab;--js:#c9a227;--accent:#3776ab;--warn-bg:#fdf3e7;--aice-bg:#e9f2fb;
--sidebar-w:280px}
@media(prefers-color-scheme:dark){:root{--bg:#14181f;--fg:#e6e4dd;--muted:#9aa3b2;
--surface:#1c222c;--border:#2b3340;--py:#6aa9d8;--js:#e0be4f;--accent:#6aa9d8;
--warn-bg:#2a2118;--aice-bg:#17232f}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font-family:Pretendard,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;
line-height:1.72;font-size:1.02rem}
nav{position:fixed;inset:0 auto 0 0;width:var(--sidebar-w);overflow-y:auto;
background:var(--surface);border-right:1px solid var(--border);padding:1.5rem 1rem}
nav h1{font-size:1rem;letter-spacing:.02em}
nav .part{margin:1.2rem 0 .3rem;font-size:.72rem;text-transform:uppercase;
letter-spacing:.12em;color:var(--muted)}
nav a{display:block;padding:.28rem .5rem;border-radius:6px;color:var(--fg);
text-decoration:none;font-size:.88rem}
nav a:hover,nav a:focus-visible{background:var(--border);outline:none}
main{margin-left:var(--sidebar-w);padding:3rem clamp(1.5rem,6vw,5rem);max-width:56rem}
article{margin-bottom:5rem;padding-bottom:3rem;border-bottom:1px solid var(--border)}
h1{font-size:clamp(1.6rem,3vw,2.2rem);line-height:1.25}
h2{margin-top:2.6rem;padding-top:.4rem;font-size:1.35rem}
h2::before{content:"";display:block;width:2.2rem;height:3px;background:var(--accent);
margin-bottom:.6rem;border-radius:2px}
pre{background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--muted);
border-radius:8px;padding:1rem 1.1rem;overflow-x:auto;font-size:.9rem;line-height:1.55}
pre.lang-python{border-left-color:var(--py)}
pre.lang-javascript,pre.lang-js{border-left-color:var(--js)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
p code,li code,td code{background:var(--surface);padding:.1em .35em;border-radius:4px;font-size:.9em}
table{border-collapse:collapse;width:100%;margin:1.2rem 0;font-size:.92rem}
th,td{border:1px solid var(--border);padding:.5rem .7rem;text-align:left;vertical-align:top}
th{background:var(--surface)}
td>code,td pre{white-space:pre-wrap}
blockquote{margin:1.4rem 0;padding:.9rem 1.1rem;border-radius:8px;
border-left:4px solid var(--muted);background:var(--surface)}
blockquote.callout-warn{border-left-color:var(--js);background:var(--warn-bg)}
blockquote.callout-aice{border-left-color:var(--py);background:var(--aice-bg)}
details{margin:1rem 0;padding:.6rem 1rem;background:var(--surface);
border:1px solid var(--border);border-radius:8px}
summary{cursor:pointer;font-weight:600}
@media(max-width:900px){nav{position:static;width:auto;border-right:none;
border-bottom:1px solid var(--border)}main{margin-left:0}}
"""

SHELL = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<nav aria-label="목차"><h1>{title}</h1>{toc}</nav>
<main>{body}</main>
</body>
</html>
"""


def chapter_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outline", help="outline md; its first '# ' heading becomes the book title")
    ap.add_argument("--chapters", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    title = args.title
    if not title and args.outline and Path(args.outline).is_file():
        title = chapter_title(Path(args.outline).read_text(encoding="utf-8"), "")
    title = title or "Python for JavaScript Developers — AICE 대비"

    chapter_dir = Path(args.chapters)
    files = sorted(chapter_dir.glob("ch*.md")) + sorted(chapter_dir.glob("appendix*.md"))
    if not files:
        print(f"error: no ch*.md files in {chapter_dir}", file=sys.stderr)
        return 1

    toc_items: list[str] = []
    articles: list[str] = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        anchor = f.stem
        ch_title = chapter_title(text, f.stem)
        toc_items.append(f'<a href="#{anchor}">{html.escape(ch_title)}</a>')
        articles.append(f'<article id="{anchor}">{md_to_html(text)}</article>')

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = SHELL.format(title=html.escape(title), css=CSS,
                       toc="\n".join(toc_items), body="\n".join(articles))
    out.write_text(doc, encoding="utf-8")

    missing = [a for a in (f.stem for f in files) if f'id="{a}"' not in doc]
    print(f"built {out} — {len(files)} chapters, {out.stat().st_size // 1024} KB")
    if missing:
        print(f"warning: missing anchors: {missing}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
