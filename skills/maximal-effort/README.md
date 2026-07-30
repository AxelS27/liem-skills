# `maximal-effort` Skill — Execution Quality Governor

[![Skill Name](https://img.shields.io/badge/Skill-maximal--effort-blue.svg)]()
[![Suite](https://img.shields.io/badge/Suite-Liem%20Skills-brightgreen.svg)]()
[![Type](https://img.shields.io/badge/Type-Passive%20Execution%20Policy-orange.svg)]()

> **Part of the Liem Skills suite.**  
> A universal behavioral policy and execution quality governor designed to eliminate **Quality Dilution** (Effort Dilution) during multi-file, large-scale AI agent tasks.

---

## Purpose & Problem Statement

When an AI Coding Agent is assigned multi-artifact tasks — such as scaffolding 10–20 complex modules or drafting extensive documentation — increasing workload queue length often causes **quality degradation**:
- Early deliverables receive meticulous detail.
- Later deliverables degrade into brief outlines, incomplete code snippets, or explicit placeholder shortcuts (`// TODO: Implement logic here`).

The **`maximal-effort`** skill enforces the principle that **the quantity of work is strictly an execution concern, never a quality concern**.

---

## Key Pillars & Guarantees

### 1. Deliverable Isolation Principle
Each deliverable in a task queue is evaluated independently. Focus allocated to the active item MUST NOT be diminished by remaining items in the queue.

### 2. Strict Anti-Shortcut Barrier
The agent is strictly prohibited from emitting explicit placeholders (`TODO`, `FIXME`, `implement here`) or implicit placeholders (truncated code blocks, omitted logic). All generated code is production-ready and *Fit for Intended Use*.

### 3. Complexity-Proportional Effort Allocation
Analytical depth and implementation effort scale strictly with the **intrinsic complexity** of the deliverable — **NOT** by raw line count or token volume:
> *A 50-line configuration file requiring strict security rules and a 2,000-line backend architecture module both receive 100% effort matched to their respective intrinsic complexity.*

### 4. Automated 4-Step Quality Governor Audit
Before emitting any deliverable, the agent executes an internal verification gate:
1. **Scope & Intent Audit**: Verifies user constraints are met without unrequested scope creep.
2. **Placeholder & Shortcut Detection**: Scans for zero `TODO`s or omitted code blocks.
3. **Edge Case & Complexity Verification**: Confirms edge case handling matches intrinsic complexity.
4. **Quality Drift Benchmark**: Ensures zero quality regression compared to baseline.

### 5. Context Boundary Turn Splitting
When execution approaches physical LLM token boundaries, the agent splits execution into sequential turns with scratch-file state preservation (`.specify/memory/scratch/turn-split-state.json`) rather than compressing output content.

### 6. Environment-Agnostic Auto-Setup
Recognizes natural language trigger commands (`setup maximal-effort skills`) to discover `SKILL.md` across any Agentic IDE (Antigravity, Claude Code, Cursor, Windsurf, Roo Code, VS Code) and automatically link it in `AGENTS.md`.

---

## Comparison: Standard Execution vs. Liem `maximal-effort` Execution

| Workload Aspect | Standard AI Agent Execution | Liem `maximal-effort` Execution |
| :--- | :--- | :--- |
| **Multi-File Tasks (e.g. 10 files)** | Quality deteriorates after file 3; file 8–10 get `// TODO` shortcuts. | **Zero quality drift**. File 10 receives identical quality and rigor as File 1. |
| **Placeholder Code** | Frequently emits `// TODO: Implement later` under context pressure. | **Strictly prohibited**. All emitted code is complete and syntactically sound. |
| **Token Limit Boundaries** | Compresses output, omits logic, or summarizes prematurely. | **Turn Splitting**. Preserves state in scratch files and resumes cleanly in a new turn. |
| **Brevity Requests** | Either ignores brevity constraint or outputs superficial content. | Respects brevity constraint while maximizing technical precision *within* requested bounds. |

---

## Quickstart & Usage

### Method A: Automated Natural Language Setup
In any AI session, simply type:
```text
setup maximal-effort skills
```
The agent will discover `skills/maximal-effort/SKILL.md` (local or global) and register it in `AGENTS.md`.

### Method B: Direct `AGENTS.md` Linking
Add the following line to `AGENTS.md` at your repository root:

```markdown
# Execution Policy
- All tasks in this workspace are governed by the passive default [maximal-effort skill](skills/maximal-effort/SKILL.md).
```

---

## Core Specification & References

- **Skill Entry Point**: [SKILL.md](SKILL.md)
- **Detailed RFC Specification Guide**: [docs/guide.md](docs/guide.md)
- **Suite Home**: [Liem Skills Root README](../../README.md)
