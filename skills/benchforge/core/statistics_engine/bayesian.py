"""Bayesian Statistical Module for BenchForge (Posterior Analysis & P(A > B))."""

import random
from typing import List, Tuple


def calculate_bayesian_superiority(candidate_data: List[float], baseline_data: List[float], num_samples: int = 2000) -> float:
    """Computes posterior probability P(Candidate > Baseline) via Monte Carlo Sampling."""
    if not candidate_data or not baseline_data:
        return 50.0

    wins = 0
    for _ in range(num_samples):
        cand_sample = random.choice(candidate_data)
        base_sample = random.choice(baseline_data)
        if cand_sample > base_sample:
            wins += 1
        elif cand_sample == base_sample:
            wins += 0.5

    prob = (wins / num_samples) * 100.0
    return round(prob, 2)
