"""Command Line Interface Entrypoint for benchforge CLI."""

import sys
import os
import argparse
from skills.benchforge.core.bdl_parser import parse_bdl_spec
from skills.benchforge.core.integrity_scorer import calculate_integrity_score
from skills.benchforge.generators.card_generator import generate_artifact_cards


def main():
    parser = argparse.ArgumentParser(
        prog="benchforge",
        description="BenchForge: Open Scientific Evidence Infrastructure for the Agentic Era"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command 1: init
    init_parser = subparsers.add_parser("init", help="Initialize a benchmark spec template")
    init_parser.add_argument("--domain", default="ai_agents", help="Domain adapter name")
    init_parser.add_argument("--output", default="./benchmarks", help="Output directory")

    # Command 2: validate
    val_parser = subparsers.add_parser("validate", help="Validate BDL spec & calculate Integrity Score")
    val_parser.add_argument("--spec", required=True, help="Path to BDL .bench.yaml file")

    # Command 3: run
    run_parser = subparsers.add_parser("run", help="Execute benchmark harness")
    run_parser.add_argument("--spec", required=True, help="Path to BDL .bench.yaml file")
    run_parser.add_argument("--iterations", type=int, default=5, help="Iteration sample size N")

    # Command 4: report
    rep_parser = subparsers.add_parser("report", help="Generate dual-tier report artifacts")
    rep_parser.add_argument("--results", default="./benchmarks/results", help="Path to results directory")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "validate":
        print(f"[Validating BDL Spec]: {args.spec}")
        spec = parse_bdl_spec(args.spec)
        integrity = calculate_integrity_score(spec.raw_dict)
        print(f"[PASS] BDL v6.0 parsed successfully for: {spec.metadata.name}")
        print(f"  - Baseline Target: {spec.baseline_subject.name}")
        print(f"  - Candidate Target: {spec.candidate_subject.name}")
        print(f"  - Benchmark Integrity Score: {integrity.overall_integrity_score}/100 [{integrity.to_dict()['status']}]")

    elif args.command == "init":
        os.makedirs(args.output, exist_ok=True)
        print(f"[PASS] Initialized BenchForge workspace in: {args.output}")

    elif args.command == "run":
        print(f"[Running BenchForge Harness]: {args.spec} (N={args.iterations})")
        from skills.benchforge.core.benchmark_engine import BenchmarkEngine
        engine = BenchmarkEngine(spec_path=args.spec, iterations=args.iterations)
        engine.run_benchmark()
        generate_artifact_cards(results_dir=engine.results_dir)
        print("[PASS] Benchmark execution complete.")

    elif args.command == "report":
        print(f"[Generating Dual-Tier Reports]: {args.results}")
        from skills.benchforge.generators.report_generator import generate_dual_reports
        generate_dual_reports(results_dir=args.results)
        generate_artifact_cards(results_dir=args.results)
        print("[PASS] Reports generated successfully.")


if __name__ == "__main__":
    main()
