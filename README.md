# Agent Guidelines

Behavioral guidelines that reduce the most common LLM coding mistakes, packaged for **every AI coding agent** and **VS Code**.

| Principle | Addresses |
|---|---|
| **Think Before Coding** | Wrong assumptions, hidden confusion, missing tradeoffs |
| **Simplicity First** | Overcomplication, bloated abstractions |
| **Surgical Changes** | Orthogonal edits, touching code you shouldn't |
| **Goal-Driven Execution** | Unverified "done", vague success criteria |

The full text lives in one place: [`core/guidelines.md`](core/guidelines.md). Every other file is generated from it.

## Install

**Option A: Claude Code Plugin (recommended for Claude Code)**

From within Claude Code, first add the marketplace:

```
/plugin marketplace add vicik25/agent-guidelines
```

Then install the plugin:

```
/plugin install agent-guidelines@vicik25-skills
```

This installs the guidelines as a Claude Code plugin, making the skill available across all your projects.

**Option B: One-line installer (any agent, per project)**

Run inside your project folder (needs Python 3.8+, no packages):

```bash
# macOS / Linux / Windows (Git Bash)
curl -fsSL https://raw.githubusercontent.com/vicik25/agent-guidelines/main/install.py | python3 - install
```

```powershell
# Windows PowerShell
irm https://raw.githubusercontent.com/vicik25/agent-guidelines/main/install.py | python - install
```

By default this writes `AGENTS.md`, `CLAUDE.md` and `GEMINI.md`. Pick other tools with `--tools`:

```bash
curl -fsSL https://raw.githubusercontent.com/vicik25/agent-guidelines/main/install.py | python3 - install --tools agents,claude,copilot,cursor
```

Your existing instructions are never overwritten: the guidelines are added between `<!-- agent-guidelines:start/end -->` markers, and re-running the installer updates that block instead of duplicating it. Add `--dry-run` to preview.

**Option C: Manual (no Python)**

New project, pick the file for your tool:

```bash
curl -O https://raw.githubusercontent.com/vicik25/agent-guidelines/main/dist/AGENTS.md
curl -O https://raw.githubusercontent.com/vicik25/agent-guidelines/main/dist/CLAUDE.md
```

Existing project (append to what you already have):

```bash
echo "" >> AGENTS.md
curl -fsSL https://raw.githubusercontent.com/vicik25/agent-guidelines/main/dist/AGENTS.md >> AGENTS.md
```

Everything else is in [`dist/`](dist/), laid out exactly as it should appear in your project.

## Supported tools

| Tool | File | Default |
|---|---|---|
| Codex, Cursor, Windsurf, Zed, Amp, Jules, Copilot (VS Code), and others | `AGENTS.md` | ✅ |
| Claude Code | `CLAUDE.md` | ✅ |
| Gemini CLI | `GEMINI.md` | ✅ |
| GitHub Copilot | `.github/copilot-instructions.md` | |
| Cursor | `.cursor/rules/agent-guidelines.mdc` | |
| Windsurf | `.windsurf/rules/agent-guidelines.md` | |
| Cline | `.clinerules/agent-guidelines.md` (or `.clinerules` if it is a file) | |
| Roo Code | `.roo/rules/agent-guidelines.md` | |
| Continue | `.continue/rules/agent-guidelines.md` | |
| Kiro | `.kiro/steering/agent-guidelines.md` | |
| Amazon Q | `.amazonq/rules/agent-guidelines.md` | |
| JetBrains Junie | `.junie/guidelines.md` | |
| Aider | `CONVENTIONS.md` (then `read: CONVENTIONS.md` in `.aider.conf.yml`) | |
| Agent Skills (Claude Code, VS Code) | `.claude/skills/agent-guidelines/SKILL.md` | |

`python install.py list` prints the same table. Use `--tools all` to install everything.

The default set is deliberately small: tools that read `AGENTS.md` don't need a second file, and installing duplicate files makes the same text load twice.

## Using with VS Code

- **GitHub Copilot** reads `AGENTS.md` from the workspace root automatically (setting: `chat.useAgentsMdFile`). Prefer the classic file? Use `--tools copilot` for `.github/copilot-instructions.md`. Use one or the other, not both.
- **Claude Code / Claude extension** reads `CLAUDE.md`. Copilot can also read it via `chat.useClaudeMdFile`.
- **Cline, Roo Code, Continue** extensions: `--tools cline`, `roo`, `continue`.
- **All projects at once:** run *Chat: New Instructions File* in the Command Palette, choose **User**, and paste the contents of `core/guidelines.md`. It syncs with Settings Sync.
- **As an Agent Skill** (loaded only when relevant, not always on): `--tools skills`. VS Code looks in `.github/skills/`, `.claude/skills/` and `.agents/skills/`. Skill and always-on instructions carry the same text, so use one or the other.

## Customization

These guidelines are meant to be merged with project-specific rules. Add your own sections outside the marker block:

```markdown
## Project-Specific Guidelines

- Use TypeScript strict mode
- All API endpoints must have tests
```

## How to know it's working

- Fewer unnecessary changes in diffs
- Fewer rewrites caused by overcomplication
- Clarifying questions come before implementation, not after mistakes

## Maintaining

Edit only `core/guidelines.md`, then run `python install.py build` to regenerate `dist/` and `skills/`. If you fork this under a different owner or name, change `REPO` at the top of `install.py` and the names in `.claude-plugin/`.

## Credits & license

MIT. Derived from [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (MIT), which in turn builds on [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) about LLM coding pitfalls.
