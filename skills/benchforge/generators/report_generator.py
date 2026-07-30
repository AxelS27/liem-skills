"""Report Generator Engine for BenchForge (Dual-Tier Reports)."""

import os
import json
from jinja2 import Template


def generate_dual_reports(results_dir: str = "./benchmarks/results") -> None:
    """Reads analysis.json and generates BENCHMARK_SUMMARY.md and BENCHMARK.md."""
    analysis_file = os.path.join(results_dir, "analysis.json")
    if not os.path.exists(analysis_file):
        raise FileNotFoundError(f"Analysis file not found: {analysis_file}")

    with open(analysis_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    summary_tmpl_path = os.path.join(templates_dir, "benchmark_summary.md.j2")
    bench_tmpl_path = os.path.join(templates_dir, "benchmark.md.j2")

    # Load templates
    with open(summary_tmpl_path, "r", encoding="utf-8") as f:
        summary_template = Template(f.read())

    with open(bench_tmpl_path, "r", encoding="utf-8") as f:
        bench_template = Template(f.read())

    # Render reports
    summary_content = summary_template.render(**data)
    bench_content = bench_template.render(**data)

    # Write output files
    summary_output_path = os.path.join(results_dir, "BENCHMARK_SUMMARY.md")
    bench_output_path = os.path.join(results_dir, "BENCHMARK.md")

    with open(summary_output_path, "w", encoding="utf-8") as f:
        f.write(summary_content)

    with open(bench_output_path, "w", encoding="utf-8") as f:
        f.write(bench_content)

    print(f"[PASS] Tier 1 GitHub Summary Card: {summary_output_path}")
    print(f"[PASS] Tier 2 Scientific Report: {bench_output_path}")
