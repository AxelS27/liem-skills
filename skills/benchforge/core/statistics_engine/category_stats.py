"""Per-Category Workload Breakdown Statistics Module for BenchForge."""

from typing import List, Dict, Any
from skills.benchforge.core.statistics_engine.frequentist import calculate_mean, calculate_cohens_d


def compute_category_breakdown(raw_results: List[Dict[str, Any]], candidate_name: str, baseline_name: str) -> List[Dict[str, Any]]:
    """Calculates pass rate mean and Cohen's d effect size breakdown per workload category."""
    categories = list(set(r["category"] for r in raw_results))
    breakdown = []

    for cat in categories:
        cand_cat_pass = [r["metrics"]["quality_pass_rate"] for r in raw_results if r["subject"] == candidate_name and r["category"] == cat]
        base_cat_pass = [r["metrics"]["quality_pass_rate"] for r in raw_results if r["subject"] == baseline_name and r["category"] == cat]

        cand_mean = calculate_mean(cand_cat_pass) if cand_cat_pass else 0.0
        base_mean = calculate_mean(base_cat_pass) if base_cat_pass else 0.0

        d_val, mag = calculate_cohens_d(cand_cat_pass, base_cat_pass)

        breakdown.append({
            "category": cat,
            "sample_size": len(cand_cat_pass),
            "baseline_pass_mean": round(base_mean, 2),
            "candidate_pass_mean": round(cand_mean, 2),
            "cohens_d": round(d_val, 2),
            "effect_magnitude": mag
        })

    return breakdown
