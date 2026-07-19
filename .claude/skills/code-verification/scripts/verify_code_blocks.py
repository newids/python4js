#!/usr/bin/env python3
"""Extract and execute ```python blocks from e-book chapter markdown files.

Blocks in one file share a namespace and run top-to-bottom (chapters build on
earlier variables). `python no-run` fences are skipped. `# 출력: <expected>`
comments are checked against the block's stdout (prefix match on first line).

Usage:
    python3 verify_code_blocks.py <file.md | directory> [...]
Exit codes: 0 all pass, 1 failures found, 2 usage error.
"""
from __future__ import annotations

import io
import os
import re
import sys
import traceback
from contextlib import redirect_stdout
from dataclasses import dataclass, field
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

FENCE_RE = re.compile(r"^```(\w+)([^\n`]*)$")
EXPECTED_RE = re.compile(r"#\s*출력:\s*(.*)")


@dataclass
class Block:
    index: int          # 1-based order among python blocks in the file
    line: int           # line number of the opening fence
    code: str
    no_run: bool


@dataclass
class Result:
    block: Block
    status: str         # PASS | FAIL | SKIP | DEPENDENCY_MISSING | OUTPUT_MISMATCH
    detail: str = ""


@dataclass
class FileReport:
    path: Path
    results: list[Result] = field(default_factory=list)

    def counts(self) -> dict[str, int]:
        c: dict[str, int] = {}
        for r in self.results:
            c[r.status] = c.get(r.status, 0) + 1
        return c


def extract_blocks(text: str) -> list[Block]:
    blocks: list[Block] = []
    lines = text.splitlines()
    i, idx = 0, 0
    in_table = False
    while i < len(lines):
        line = lines[i]
        # code inside markdown tables (side-by-side snippets) is never executed
        if line.lstrip().startswith("|"):
            i += 1
            continue
        m = FENCE_RE.match(line.strip())
        if m and m.group(1).lower() == "python":
            no_run = "no-run" in m.group(2)
            start = i + 1
            body: list[str] = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                body.append(lines[i])
                i += 1
            idx += 1
            blocks.append(Block(idx, start, "\n".join(body), no_run))
        i += 1
    return blocks


def first_line(s: str) -> str:
    return s.strip().splitlines()[0].strip() if s.strip() else ""


def run_file(path: Path) -> FileReport:
    report = FileReport(path)
    blocks = extract_blocks(path.read_text(encoding="utf-8"))
    ns: dict = {"__name__": "__main__"}
    for blk in blocks:
        if blk.no_run:
            report.results.append(Result(blk, "SKIP", "no-run"))
            continue
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                exec(compile(blk.code, f"{path.name}:block{blk.index}", "exec"), ns)
        except ImportError as e:
            report.results.append(Result(blk, "DEPENDENCY_MISSING", str(e)))
            continue
        except Exception:
            tb = traceback.format_exc().strip().splitlines()[-1]
            report.results.append(Result(blk, "FAIL", tb))
            continue
        expected = EXPECTED_RE.findall(blk.code)
        if expected and expected[0].strip():
            actual = first_line(buf.getvalue())
            want = expected[0].strip()
            if not actual.startswith(want):
                report.results.append(
                    Result(blk, "OUTPUT_MISMATCH",
                           f"expected startswith {want!r}, got {actual!r}"))
                continue
        report.results.append(Result(blk, "PASS"))
    return report


def collect_targets(args: list[str]) -> list[Path]:
    targets: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            targets.extend(sorted(p.glob("*.md")))
        elif p.is_file():
            targets.append(p)
        else:
            print(f"error: not found: {a}", file=sys.stderr)
            sys.exit(2)
    return targets


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    failed = False
    for path in collect_targets(sys.argv[1:]):
        rep = run_file(path)
        c = rep.counts()
        summary = " / ".join(f"{v} {k}" for k, v in sorted(c.items())) or "no python blocks"
        print(f"\n## {path.name} — {summary}")
        for r in rep.results:
            if r.status != "PASS":
                print(f"| {r.block.index} | {r.status} | 블록 {r.block.index} (md {r.block.line}행): {r.detail} |")
            if r.status in ("FAIL", "OUTPUT_MISMATCH"):
                failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
