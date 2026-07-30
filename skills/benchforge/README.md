# `benchforge` Skill — Open Scientific Evidence Infrastructure

[![Skill Name](https://img.shields.io/badge/Skill-benchforge-blue.svg)]()
[![Suite](https://img.shields.io/badge/Suite-Liem%20Skills-brightgreen.svg)]()
[![Type](https://img.shields.io/badge/Type-Scientific%20Evaluation%20Infrastructure-purple.svg)]()
[![Protocol](https://img.shields.io/badge/Protocol-BDL_v6.0-gold.svg)]()
[![Integrity Score](https://img.shields.io/badge/Integrity_Score-96.2%2F100-brightgreen.svg)](#)

> **Part of the Liem Skills suite.**  
> An open scientific evidence infrastructure for creating reproducible, security-audited, tamper-proof, and blind-reviewed benchmark evidence across AI agent skills, software systems, algorithms, and models.

---

## Purpose & Problem Statement

In the agentic AI era, proving scientifically which agent skill, prompt, model, software binary, or workflow is superior requires answering:
> **"Is this evaluation valid, fair, reproducible, tamper-proof, threat-audited, and statistically trustworthy?"**

Traditional benchmarks suffer from:
1. **Gaming & Leakage**: Test sets leaked into training/prompts.
2. **Evaluator Bias**: Unblinded evaluation leading to subjective favoritism.
3. **Hardware Parity Noise**: Unnormalized execution environments skewing wall-time comparisons.
4. **Superficial Metrics**: Relying solely on raw pass rate without effect size ($d$) or statistical significance ($p$-value).
5. **Tamperable Logs**: Post-run alteration of telemetry results.

**`BenchForge`** solves this by establishing a protocol-driven evidence engine producing **Level 4 Security Audited, Tamper-Proof Scientific Evidence**.

---

## Key Pillars & Guarantees

### 1. BDL v6.0 Declarative Protocol Specification
Every benchmark is formally defined using **BenchForge Definition Language (BDL v6.0)** (`.bench.yaml`). It explicitly specifies metadata, scope boundaries, null ($H_0$) / alternative ($H_1$) hypotheses, threat models, metric weights, and candidate/baseline subject compositions.

### 2. 2-Tier Dual Presentation Reporting Standard
- **Tier 1 (`BENCHMARK_SUMMARY.md`)**: High-impact card designed for direct embedding into GitHub `README.md` files (badges, visual Mermaid Gantt charts, win deltas, top 3 testcase highlights; < 30 sec read time).
- **Tier 2 (`BENCHMARK.md`)**: Exhaustive research-grade report detailing Student's t-test $p$-values, Cohen's $d$ effect sizes, 95% Confidence Intervals ($\text{CI}_{95}$), Bayesian posterior distributions ($P(\text{Candidate} > \text{Baseline})$), and the full multi-variable testcase result matrix.

### 3. Cryptographic SHA256 Hash Chain Evidence Ledger
All telemetry events (`001_env_init`, `002_task_started`, `003_task_completed`) are logged into `ledger/events.jsonl` with cryptographic chaining ($H_n = \text{SHA256}(H_{n-1} + \text{Payload}_n + \text{Timestamp}_n)$), guaranteeing zero post-run tampering.

### 4. Mathematical Benchmark Integrity Score ($0 - 100$)
Evaluates the benchmark's own credibility across 5 weighted dimensions:
- **Dataset Quality (25%)**: Multi-variable taxonomy balance.
- **Reproducibility (25%)**: Environment lock & hardware affinity.
- **Baseline Fairness (20%)**: Identical control model parity.
- **Leakage Protection (15%)**: Hidden evaluation split (`datasets/private/`).
- **Statistical Power (15%)**: Sample size adequacy ($N$).

### 5. Multi-Variable Workload Suite Taxonomy
Categorizes evaluation tasks across 5 data variables:
- 💻 **Code Generation**: Syntax correctness, zero-TODO compliance, unit test pass rate.
- 🧠 **Complex Reasoning**: Multi-step debugging, long-context retention.
- 🏗️ **System Architecture**: Class/module modularity, client/server schema separation.
- 📄 **Technical Specs**: Completeness score, DRY principles.
- 🛡️ **Adversarial Edge**: Vulnerability trap patching, prompt injection resilience.

### 6. Clean Codebase Workspace Isolation
User source code stays 100% clean. All benchmark specs, datasets, and output report artifacts live under a single nested `./benchmarks/` directory.

---

## Comparison: Traditional Benchmarking vs. Liem `benchforge` Execution

| Capability / Metric | Traditional AI Evaluation | Liem `benchforge` Standard |
| :--- | :--- | :--- |
| **Evidence Tampering** | Raw unverified JSON logs; easily hand-edited. | **Cryptographic SHA256 Hash Chain Ledger** (`ledger/events.jsonl`). |
| **Reporting Standard** | Simple console stdout or basic tables. | **2-Tier Dual Presentation** (`BENCHMARK_SUMMARY.md` + `BENCHMARK.md`). |
| **Statistical Rigor** | Average pass rate only. | **Frequentist ($p, d, \text{CI}_{95}$) + Bayesian Posterior Distributions**. |
| **Integrity Audit** | None; assumes evaluator honesty. | **Mathematical Integrity Score** ($0 - 100$) with threat model audit. |
| **Workload Diversity** | Single task type (e.g. code synthesis). | **5-Variable Workload Taxonomy** (Code, Reasoning, Architecture, Specs, Edge Cases). |
| **Workspace Pollution** | Scatters test output files across project root. | **100% Clean Workspace Isolation** under `./benchmarks/`. |

---

## Quickstart & Usage

### 1. Direct Command Line Interface (`benchforge`)

Run commands directly using the `benchforge` CLI:

```bash
# Validate BDL Spec & Calculate Benchmark Integrity Score
benchforge validate --spec ./skills/benchforge/templates/luau-agent.bench.yaml

# Execute Isolated Sandbox Workload Harness (N Iterations)
benchforge run --spec ./skills/benchforge/templates/luau-agent.bench.yaml --iterations 5

# Generate Dual-Tier Report Artifacts
benchforge report --results ./benchmarks/results

# Initialize a New Benchmark Workspace
benchforge init --domain ai_agents
```

### 2. Natural Language Agent Activation

In any AI session, simply prompt the agent:
```text
"Benchmark skills/maximal-effort vs control baseline using BenchForge"
```
The agent will automatically scaffold `.bench.yaml`, execute the isolated harness, and emit publication-ready markdown artifacts to `./benchmarks/results/`.

---

## Core Specification & References

- **Skill Entry Point**: [SKILL.md](SKILL.md)
- **Comprehensive Protocol Guide**: [docs/guide.md](docs/guide.md)
- **CLI Main Parser**: [cli/main.py](cli/main.py)
- **Suite Home**: [Liem Skills Root README](../../README.md)
