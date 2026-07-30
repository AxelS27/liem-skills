"""Abstract Contract for BenchForge Domain Adapters (7-Phase Event-Driven Lifecycle)."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BenchmarkPlugin(ABC):
    """Abstract Contract for BenchForge Domain Adapters.
    
    All domain adapters MUST implement these 7 lifecycle hooks:
    1. on_environment_create: Initialize sandbox environment.
    2. on_subject_loaded: Triggered when baseline or candidate subject is loaded.
    3. on_task_start: Triggered immediately prior to workload execution.
    4. execute: Executes the core workload iteration.
    5. on_metric_emit: Extracts metrics and attaches provenance metadata.
    6. on_task_complete: Triggered post-execution metric emission.
    7. teardown: Cleans up sandbox resources and process handles.
    """

    @abstractmethod
    def on_environment_create(self, config: Dict[str, Any]) -> bool:
        """Initialize isolated sandbox environment and verify tool locks."""
        pass

    @abstractmethod
    def on_subject_loaded(self, subject: Dict[str, Any]) -> None:
        """Hook called when candidate or baseline subject composition is loaded."""
        pass

    @abstractmethod
    def on_task_start(self, task: Dict[str, Any]) -> None:
        """Hook called immediately prior to task execution."""
        pass

    @abstractmethod
    def execute(self, subject: Dict[str, Any], task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute core workload iteration and return raw execution outputs."""
        pass

    @abstractmethod
    def on_metric_emit(self, raw_output: Dict[str, Any]) -> Dict[str, Any]:
        """Extract multi-dimensional metrics with measurement provenance metadata."""
        pass

    @abstractmethod
    def on_task_complete(self, result: Dict[str, Any]) -> None:
        """Hook called after task metrics are logged."""
        pass

    @abstractmethod
    def teardown(self) -> None:
        """Tear down scratch resources and release sandbox locks."""
        pass
