#!/usr/bin/env python3
"""Install agent-guidelines for any AI coding agent / editor.

  python install.py install [PROJECT_DIR] [--tools agents,claude,...|all] [--dry-run]
  python install.py build            # regenerate ./dist and ./skills (maintainers)
  python install.py list

Works from a clone, or piped straight from GitHub (then it downloads core/guidelines.md).
Stdlib only, Python 3.8+.
"""
import argparse
import sys
import urllib.request
from pathlib import Path

REPO = "vicik25/agent-guidelines"   # <- change if you use another owner/name
NAME = "agent-guidelines"
ROOT = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
START = f"<!-- {NAME}:start -->"
END = f"<!-- {NAME}:end -->"
DESC = ("Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, "
        "reviewing, or refactoring code to surface assumptions, keep it simple, "
        "make surgical changes, and define verifiable success criteria.")


def load_body():
    local = ROOT / "core" / "guidelines.md"
    if local.is_file():
        return local.read_text(encoding="utf-8").strip()
    url = f"https://raw.githubusercontent.com/{REPO}/main/core/guidelines.md"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return r.read().decode("utf-8").strip()
    except Exception as e:  # noqa: BLE001
        sys.exit(f"Could not read core/guidelines.md locally or from {url}\n  {e}")


def front(*lines):
    return "---\n" + "\n".join(lines) + "\n---\n\n"


SKILL_HEAD = front(f"name: {NAME}", f'description: "{DESC}"', "license: MIT")

# name -> [(relative path, mode, header)]
#   merge: shared file, we only own the block between the markers
#   own:   file dedicated to us, overwritten
TARGETS = {
    "agents":   [("AGENTS.md", "merge", "")],
    "claude":   [("CLAUDE.md", "merge", "")],
    "gemini":   [("GEMINI.md", "merge", "")],
    "copilot":  [(".github/copilot-instructions.md", "merge", "")],
    "aider":    [("CONVENTIONS.md", "merge", "")],
    "junie":    [(".junie/guidelines.md", "merge", "")],
    "cursor":   [(f".cursor/rules/{NAME}.mdc", "own",
                  front(f'description: "{DESC}"', "alwaysApply: true"))],
    "windsurf": [(f".windsurf/rules/{NAME}.md", "own",
                  front("trigger: always_on", f'description: "{DESC}"'))],
    "continue": [(f".continue/rules/{NAME}.md", "own",
                  front("name: Agent Guidelines", "alwaysApply: true"))],
    "kiro":     [(f".kiro/steering/{NAME}.md", "own", front("inclusion: always"))],
    "cline":    [(f".clinerules/{NAME}.md", "own", "")],
    "roo":      [(f".roo/rules/{NAME}.md", "own", "")],
    "amazonq":  [(f".amazonq/rules/{NAME}.md", "own", "")],
    "skills":   [(f".claude/skills/{NAME}/SKILL.md", "own", SKILL_HEAD)],
}
# AGENTS.md is read by Codex, Copilot (VS Code), Cursor, Windsurf, Zed, Amp, Jules, ...
# Claude Code and Gemini CLI need their own file. Everything else is opt-in.
DEFAULT = ["agents", "claude", "gemini"]


def merged(old, block):
    block = block.rstrip("\n")
    if old is None:
        return block + "\n"
    if START in old and END in old:
        a, b = old.index(START), old.index(END) + len(END)
        return (old[:a] + block + old[b:]).rstrip("\n") + "\n"
    return old.rstrip("\n") + "\n\n" + block + "\n"


def write_targets(dest, targets, body, dry=False):
    block = f"{START}\n{body}\n{END}"
    for rel, mode, header in targets:
        path = dest / rel
        if rel == f".clinerules/{NAME}.md" and (dest / ".clinerules").is_file():
            path, mode, header = dest / ".clinerules", "merge", ""  # legacy single file
        old = path.read_text(encoding="utf-8") if path.is_file() else None
        new = merged(old, block) if mode == "merge" else header + body + "\n"
        status = ("created" if old is None else
                  "unchanged" if old == new else
                  "updated" if mode == "own" or START in old else "appended")
        print(f"  {status:<9} {path.relative_to(dest)}")
        if not dry and status != "unchanged":
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(new, encoding="utf-8")


def install(dest, names, dry=False):
    body = load_body()
    for n in names:
        write_targets(dest, TARGETS[n], body, dry)


def pick(arg):
    if arg == "all":
        return list(TARGETS)
    names = [n.strip() for n in arg.split(",") if n.strip()]
    bad = [n for n in names if n not in TARGETS]
    if bad:
        sys.exit(f"Unknown tool(s): {', '.join(bad)}. Run: python install.py list")
    return names


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("install", help="write guidelines into a project")
    p.add_argument("project", nargs="?", default=".")
    p.add_argument("--tools", default=",".join(DEFAULT))
    p.add_argument("--dry-run", action="store_true")
    sub.add_parser("build", help="regenerate ./dist and the Claude Code plugin skill")
    sub.add_parser("list", help="show available tools")
    a = ap.parse_args()

    if a.cmd == "list":
        for n, items in TARGETS.items():
            tag = "(default)" if n in DEFAULT else ""
            print(f"{n:<9} {tag:<10} {', '.join(r for r, _, _ in items)}")
    elif a.cmd == "build":
        install(ROOT / "dist", list(TARGETS))
        # skill used by the Claude Code plugin (see .claude-plugin/plugin.json)
        write_targets(ROOT, [(f"skills/{NAME}/SKILL.md", "own", SKILL_HEAD)], load_body())
    else:
        dest = Path(a.project).resolve()
        if not dest.is_dir():
            sys.exit(f"Not a directory: {dest}")
        print(f"{'[dry-run] ' if a.dry_run else ''}Installing into {dest}")
        install(dest, pick(a.tools), a.dry_run)


if __name__ == "__main__":
    main()
