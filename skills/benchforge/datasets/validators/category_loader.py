"""Multi-Variable Workload Category Loader and Validator for BenchForge."""

from typing import List, Dict, Any


DEFAULT_WORKLOAD_CATEGORIES = [
    "code_generation",
    "complex_reasoning",
    "system_architecture",
    "technical_specs",
    "adversarial_edge_cases"
]


def validate_workload_categories(categories: List[str]) -> List[str]:
    """Ensures workload categories match or extend BenchForge multi-variable taxonomy."""
    if not categories:
        return DEFAULT_WORKLOAD_CATEGORIES
    return list(set(categories))
