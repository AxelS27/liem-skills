"""Sandbox Harness Process Executor for BenchForge."""

import os
import yaml
from typing import Dict, Any, List
from skills.benchforge.domains.ai_agents.plugin import AIAgentPlugin
from skills.benchforge.core.ledger_engine import HashChainLedgerEngine


class ExperimentManager:
    """Orchestrates isolated sandbox workload execution for Candidate vs Baseline subjects."""

    def __init__(self, results_dir: str):
        self.results_dir = results_dir
        self.ledger_dir = os.path.join(results_dir, "ledger")
        self.ledger_engine = HashChainLedgerEngine(self.ledger_dir)
        self.plugin = AIAgentPlugin()

    def run_experiment(self, bdl_spec: Any, iterations: int = 5) -> List[Dict[str, Any]]:
        """Executes candidate and baseline workloads over N iterations in isolated sandbox."""
        os.makedirs(self.results_dir, exist_ok=True)
        
        self.ledger_engine.append_event("environment_initialized", {
            "spec_id": bdl_spec.metadata.id,
            "benchmark_name": bdl_spec.metadata.name,
            "iterations": iterations,
            "sandbox_type": "runtime"
        })

        dataset_path = bdl_spec.dataset_ref
        tasks = self._load_dataset_tasks(dataset_path)

        collected_results = []
        subjects = [
            {"id": "baseline", "name": bdl_spec.baseline_subject.name, "config": bdl_spec.baseline_subject.config},
            {"id": "candidate", "name": bdl_spec.candidate_subject.name, "config": bdl_spec.candidate_subject.config}
        ]

        self.plugin.on_environment_create({"results_dir": self.results_dir})

        for subj in subjects:
            self.plugin.on_subject_loaded(subj)
            for it in range(1, iterations + 1):
                for task in tasks:
                    self.plugin.on_task_start(task)
                    
                    self.ledger_engine.append_event("task_started", {
                        "subject": subj["name"],
                        "task_id": task["id"],
                        "iteration": it,
                        "category": task["category"]
                    })

                    raw_out = self.plugin.execute(subj, task)
                    emitted = self.plugin.on_metric_emit(raw_out)
                    
                    result_entry = {
                        "subject": subj["name"],
                        "subject_type": subj["id"],
                        "task_id": task["id"],
                        "category": task["category"],
                        "iteration": it,
                        "metrics": emitted["metrics"],
                        "provenance": emitted["provenance"]
                    }

                    self.ledger_engine.append_event("task_completed", result_entry)
                    collected_results.append(result_entry)
                    self.plugin.on_task_complete(result_entry)

        self.plugin.teardown()
        return collected_results

    def _load_dataset_tasks(self, dataset_ref: str) -> List[Dict[str, Any]]:
        """Helper to load tasks from dataset manifest."""
        abs_path = os.path.abspath(dataset_ref)
        if not os.path.exists(abs_path):
            fallback = os.path.join("skills", "benchforge", "datasets", "manifests", "ai_coding_tasks.yaml")
            abs_path = os.path.abspath(fallback)

        if os.path.exists(abs_path):
            with open(abs_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data.get("tasks", [])

        return [
            {"id": "task-001", "name": "Code Gen", "category": "code_generation"},
            {"id": "task-002", "name": "Reasoning", "category": "complex_reasoning"},
            {"id": "task-003", "name": "Architecture", "category": "system_architecture"},
            {"id": "task-004", "name": "Docs", "category": "technical_specs"},
            {"id": "task-005", "name": "Edge Cases", "category": "adversarial_edge_cases"}
        ]
