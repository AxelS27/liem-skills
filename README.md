# Liem Skills

[![Suite Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![Brand](https://img.shields.io/badge/Brand-Liem%20Product-blue.svg)]()
[![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-red.svg)](LICENSE)
[![Compatibility](https://img.shields.io/badge/Compatibility-All%20Agentic%20IDEs-orange.svg)]()

**Liem Skills** is an open repository of custom, production-grade AI Agent skills designed to standardize and elevate coding assistant workflows across any AI development environment.

---

## Overview

The Liem Skills ecosystem provides reusable, agentic capabilities and behavioral policies for AI coding assistants. Each skill in this repository focuses on a specific engineering discipline, workflow automation, or quality governance rule.

---

## Catalog of Available Skills

| Skill Name | Version | Category | Overview | Documentation |
| :--- | :---: | :--- | :--- | :---: |
| **maximal-effort** | 1.0.0 | Execution Policy | Universal behavioral execution policy and quality governor enforcing deliverable isolation and zero TODO shortcuts. | [Skill README](skills/maximal-effort/README.md) \| [SKILL.md](skills/maximal-effort/SKILL.md) |

---

## Universal Setup & Installation

Any skill in this repository can be installed or linked into a project workspace using standard discovery methods:

### Method 1: Natural Language Trigger
In your active AI coding session (Antigravity, Claude Code, Cursor, Windsurf, Roo Code, Cline, VS Code), type:
```text
setup <skill-name> skills
```
For example:
```text
setup maximal-effort skills
```
The AI agent will search local and global skill paths, locate the target `SKILL.md`, and register it in `AGENTS.md` at your project root.

### Method 2: Manual Link via AGENTS.md
Add the skill reference to `AGENTS.md` in your project root directory:

```markdown
# Skill Reference
- [<skill-name>](skills/<skill-name>/SKILL.md)
```

---

## IDE & Environment Compatibility

Liem Skills are completely environment-agnostic and work seamlessly with:
- Antigravity / Gemini CLI
- Claude Code (Anthropic)
- Cursor & Windsurf (Codeium)
- Roo Code & Cline
- VS Code Agentic Extensions

---

## License & Maintenance

Maintained by **Liem Product** (AxelS27).

Licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](LICENSE). Free for open-source and non-commercial use. Commercial use or monetization is prohibited.