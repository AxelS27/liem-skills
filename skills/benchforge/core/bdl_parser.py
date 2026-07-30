"""BDL v6.0 Protocol Specification Parser and Validator for BenchForge."""

import os
import yaml
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class MetadataSpec:
    id: str = "BF-EV-00001"
    name: str = "benchmark-evaluation"
    version: str = "1.0.0"
    created: str = "2026-07-31"
    parent_id: Optional[str] = None
    commit_hash: Optional[str] = None
    author: str = "Agentic AI Team"
    license: str = "MIT"


@dataclass
class ScopeSpec:
    measures: List[str] = field(default_factory=lambda: ["quality", "performance"])
    does_not_measure: List[str] = field(default_factory=lambda: ["unrelated_features"])
    intended_users: List[str] = field(default_factory=lambda: ["developers"])
    validity_boundary: str = "General execution environment"


@dataclass
class ThreatModelSpec:
    benchmark_gaming: Dict[str, Any] = field(default_factory=lambda: {
        "severity": "HIGH", "mitigation": ["hidden_eval_split"]
    })
    evaluator_bias: Dict[str, Any] = field(default_factory=lambda: {
        "severity": "MEDIUM", "mitigation": ["blind_review"]
    })
    hardware_advantage: Dict[str, Any] = field(default_factory=lambda: {
        "severity": "HIGH", "mitigation": ["normalized_sandbox"]
    })


@dataclass
class SubjectSpec:
    name: str
    subject_ref: Optional[str] = None
    type: str = "agent"
    config: Dict[str, Any] = field(default_factory=dict)
    composition: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricSpec:
    name: str
    type: str  # quality, performance, efficiency, reliability
    unit: str
    weight: float = 0.25
    direction: str = "higher_is_better"


@dataclass
class EvaluationSpec:
    index_name: str = "Composite Evaluation Index"
    method: str = "weighted_average"
    justification: str = "Balanced multi-dimensional evaluation"
    metrics: Dict[str, MetricSpec] = field(default_factory=dict)


@dataclass
class BDLSpecification:
    api_version: str
    kind: str
    metadata: MetadataSpec
    scope: ScopeSpec
    threat_model: ThreatModelSpec
    baseline_subject: SubjectSpec
    candidate_subject: SubjectSpec
    dataset_ref: str
    workload_categories: List[str]
    evaluation: EvaluationSpec
    raw_dict: Dict[str, Any]


def parse_bdl_spec(file_path: str) -> BDLSpecification:
    """Parses a .bench.yaml file and returns a validated BDLSpecification instance."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"BDL specification file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid BDL specification format in {file_path}")

    api_version = data.get("apiVersion", "benchforge/v6.0")
    kind = data.get("kind", "Benchmark")

    # Metadata
    meta_raw = data.get("metadata", {})
    metadata = MetadataSpec(
        id=meta_raw.get("id", "BF-EV-00001"),
        name=meta_raw.get("name", "unnamed-benchmark"),
        version=meta_raw.get("version", "1.0.0"),
        created=meta_raw.get("created", "2026-07-31"),
        parent_id=meta_raw.get("parent_id"),
        commit_hash=meta_raw.get("commit_hash"),
        author=meta_raw.get("author", "Agentic AI Team"),
        license=meta_raw.get("license", "MIT")
    )

    # Scope
    scope_raw = data.get("scope", {})
    scope = ScopeSpec(
        measures=scope_raw.get("measures", ["quality", "performance"]),
        does_not_measure=scope_raw.get("does_not_measure", ["unrelated_features"]),
        intended_users=scope_raw.get("intended_users", ["developers"]),
        validity_boundary=scope_raw.get("validity_boundary", "General environment")
    )

    # Threat Model
    threat_raw = data.get("threat_model", {})
    threat_model = ThreatModelSpec(
        benchmark_gaming=threat_raw.get("benchmark_gaming", {"severity": "HIGH", "mitigation": ["hidden_tests"]}),
        evaluator_bias=threat_raw.get("evaluator_bias", {"severity": "MEDIUM", "mitigation": ["blind_review"]}),
        hardware_advantage=threat_raw.get("hardware_advantage", {"severity": "HIGH", "mitigation": ["normalized_sandbox"]})
    )

    # Subjects
    subjects_raw = data.get("subjects", {})
    base_raw = subjects_raw.get("baseline", {})
    cand_raw = subjects_raw.get("candidate", {})

    baseline_subject = SubjectSpec(
        name=base_raw.get("name", "Baseline"),
        subject_ref=base_raw.get("subject_ref"),
        type=base_raw.get("type", "agent"),
        config=base_raw.get("config", {}),
        composition=base_raw.get("composition", {})
    )

    candidate_subject = SubjectSpec(
        name=cand_raw.get("name", "Candidate"),
        subject_ref=cand_raw.get("subject_ref"),
        type=cand_raw.get("type", "agent"),
        config=cand_raw.get("config", {}),
        composition=cand_raw.get("composition", {})
    )

    # Workload
    workload_raw = data.get("workload", {})
    dataset_raw = workload_raw.get("dataset", {})
    dataset_ref = dataset_raw.get("ref", "datasets/manifests/default.yaml")
    workload_categories = dataset_raw.get("categories", [
        "code_generation", "complex_reasoning", "system_architecture", "technical_specs", "adversarial_edge_cases"
    ])

    # Evaluation
    eval_raw = data.get("evaluation", {})
    metrics_raw = eval_raw.get("metrics", {})
    metrics: Dict[str, MetricSpec] = {}

    for metric_key, metric_val in metrics_raw.items():
        if isinstance(metric_val, dict):
            metrics[metric_key] = MetricSpec(
                name=metric_key,
                type=metric_val.get("type", "quality"),
                unit=metric_val.get("unit", "%"),
                weight=float(metric_val.get("weight", 0.25)),
                direction=metric_val.get("direction", "higher_is_better")
            )

    evaluation = EvaluationSpec(
        index_name=eval_raw.get("index_name", "Composite Evaluation Index"),
        method=eval_raw.get("method", "weighted_average"),
        justification=eval_raw.get("justification", "Balanced multi-dimensional score"),
        metrics=metrics
    )

    return BDLSpecification(
        api_version=api_version,
        kind=kind,
        metadata=metadata,
        scope=scope,
        threat_model=threat_model,
        baseline_subject=baseline_subject,
        candidate_subject=candidate_subject,
        dataset_ref=dataset_ref,
        workload_categories=workload_categories,
        evaluation=evaluation,
        raw_dict=data
    )
