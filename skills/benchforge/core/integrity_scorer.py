"""Mathematical Benchmark Integrity Score Calculator for BenchForge."""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class IntegrityScoreResult:
    dataset_quality: float
    reproducibility: float
    baseline_fairness: float
    leakage_protection: float
    statistical_power: float
    overall_integrity_score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_quality": round(self.dataset_quality, 2),
            "reproducibility": round(self.reproducibility, 2),
            "baseline_fairness": round(self.baseline_fairness, 2),
            "leakage_protection": round(self.leakage_protection, 2),
            "statistical_power": round(self.statistical_power, 2),
            "overall_integrity_score": round(self.overall_integrity_score, 2),
            "status": "HIGH CREDIBILITY (PASS)" if self.overall_integrity_score >= 85.0 else "MODERATE CREDIBILITY (PASS)"
        }


def calculate_integrity_score(spec_data: Dict[str, Any], sample_size_N: int = 10) -> IntegrityScoreResult:
    """Computes the mathematical Benchmark Integrity Score based on spec criteria."""
    
    # 1. Dataset Quality Score (25%)
    workload = spec_data.get("workload", {})
    categories = workload.get("dataset", {}).get("categories", [])
    dataset_quality = min(100.0, max(50.0, len(categories) * 20.0))

    # 2. Reproducibility Score (25%)
    constraints = spec_data.get("experiment", {}).get("constraints", {})
    has_hardware = "hardware" in constraints
    reproducibility = 95.0 if has_hardware else 80.0

    # 3. Baseline Fairness Score (20%)
    subjects = spec_data.get("subjects", {})
    has_baseline = "baseline" in subjects and subjects["baseline"].get("name") is not None
    baseline_fairness = 100.0 if has_baseline else 0.0

    # 4. Leakage Protection Score (15%)
    threat = spec_data.get("threat_model", {})
    gaming_mitigations = threat.get("benchmark_gaming", {}).get("mitigation", [])
    has_hidden_split = "hidden_eval_split" in gaming_mitigations or "hidden_tests" in str(workload)
    leakage_protection = 98.0 if has_hidden_split else 70.0

    # 5. Statistical Power Score (15%)
    if sample_size_N >= 30:
        statistical_power = 100.0
    elif sample_size_N >= 15:
        statistical_power = 90.0
    elif sample_size_N >= 10:
        statistical_power = 85.0
    elif sample_size_N >= 5:
        statistical_power = 70.0
    else:
        statistical_power = 50.0

    # Weighted Overall Score Calculation
    overall = (
        0.25 * dataset_quality +
        0.25 * reproducibility +
        0.20 * baseline_fairness +
        0.15 * leakage_protection +
        0.15 * statistical_power
    )

    return IntegrityScoreResult(
        dataset_quality=dataset_quality,
        reproducibility=reproducibility,
        baseline_fairness=baseline_fairness,
        leakage_protection=leakage_protection,
        statistical_power=statistical_power,
        overall_integrity_score=overall
    )
