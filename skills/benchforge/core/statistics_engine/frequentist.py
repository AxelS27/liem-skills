"""Frequentist Statistical Module for BenchForge (t-test, Cohen's d, CI95)."""

import math
from typing import List, Dict, Any, Tuple


def calculate_mean(data: List[float]) -> float:
    if not data:
        return 0.0
    return sum(data) / len(data)


def calculate_stddev(data: List[float], mean: float) -> float:
    if len(data) <= 1:
        return 0.0
    variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
    return math.sqrt(variance)


def calculate_confidence_interval(data: List[float], mean: float, stddev: float, confidence: float = 0.95) -> Tuple[float, float]:
    n = len(data)
    if n <= 1 or stddev == 0.0:
        return (mean, mean)
    margin_of_error = 1.96 * (stddev / math.sqrt(n))
    return (mean - margin_of_error, mean + margin_of_error)


def calculate_cohens_d(candidate_data: List[float], baseline_data: List[float]) -> Tuple[float, str]:
    """Calculates Cohen's d effect size magnitude."""
    n1, n2 = len(candidate_data), len(baseline_data)
    if n1 <= 1 or n2 <= 1:
        return (0.0, "Negligible")

    mean1 = calculate_mean(candidate_data)
    mean2 = calculate_mean(baseline_data)
    std1 = calculate_stddev(candidate_data, mean1)
    std2 = calculate_stddev(baseline_data, mean2)

    pooled_std = math.sqrt(((n1 - 1) * (std1 ** 2) + (n2 - 1) * (std2 ** 2)) / (n1 + n2 - 2))
    if pooled_std == 0.0:
        return (0.0, "Negligible")

    d = (mean1 - mean2) / pooled_std
    abs_d = abs(d)

    if abs_d >= 0.8:
        magnitude = "Large Effect (PASS)"
    elif abs_d >= 0.5:
        magnitude = "Medium Effect"
    elif abs_d >= 0.2:
        magnitude = "Small Effect"
    else:
        magnitude = "Negligible"

    return (d, magnitude)


def calculate_welchs_ttest(candidate_data: List[float], baseline_data: List[float]) -> float:
    """Calculates Welch's t-test p-value approximation."""
    n1, n2 = len(candidate_data), len(baseline_data)
    if n1 <= 1 or n2 <= 1:
        return 1.0

    m1, m2 = calculate_mean(candidate_data), calculate_mean(baseline_data)
    v1 = calculate_stddev(candidate_data, m1) ** 2
    v2 = calculate_stddev(baseline_data, m2) ** 2

    se = math.sqrt((v1 / n1) + (v2 / n2))
    if se == 0.0:
        return 0.0 if m1 != m2 else 1.0

    t_stat = abs((m1 - m2) / se)
    p_approx = math.exp(-0.717 * t_stat - 0.416 * (t_stat ** 2))
    return min(1.0, max(0.0001, p_approx))
