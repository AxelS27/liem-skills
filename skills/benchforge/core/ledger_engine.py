"""Cryptographic SHA256 Hash Chain Evidence Ledger Engine for BenchForge."""

import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class HashChainLedgerEngine:
    """Manages an immutable, tamper-proof SHA256 Hash Chain Evidence Ledger."""

    def __init__(self, ledger_dir: str):
        self.ledger_dir = ledger_dir
        self.events_file = os.path.join(ledger_dir, "events.jsonl")
        self.last_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        self.event_sequence = 0
        os.makedirs(self.ledger_dir, exist_ok=True)
        self._initialize_chain()

    def _initialize_chain(self) -> None:
        """Loads existing chain to compute latest hash state if events file exists."""
        if os.path.exists(self.events_file):
            with open(self.events_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        self.last_hash = entry.get("hash", self.last_hash)
                        self.event_sequence += 1

    def append_event(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Appends a new event payload, computes SHA256(prev_hash + payload + timestamp), and logs entry."""
        self.event_sequence += 1
        timestamp = datetime.now(timezone.utc).isoformat()
        previous_hash = self.last_hash

        # Compute SHA256 digest
        payload_str = json.dumps(payload, sort_keys=True)
        raw_signature = f"{previous_hash}:{payload_str}:{timestamp}"
        current_hash = hashlib.sha256(raw_signature.encode("utf-8")).hexdigest()

        event_entry = {
            "event_id": f"{self.event_sequence:03d}_{event_type}",
            "event_version": "1.0",
            "timestamp": timestamp,
            "previous_hash": previous_hash,
            "payload": payload,
            "hash": current_hash
        }

        with open(self.events_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event_entry) + "\n")

        self.last_hash = current_hash
        return event_entry

    def verify_chain_integrity(self) -> bool:
        """Verifies that the entire Hash Chain Evidence Ledger is tamper-proof."""
        if not os.path.exists(self.events_file):
            return True

        expected_prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        with open(self.events_file, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                entry = json.loads(line)
                actual_prev = entry.get("previous_hash")
                actual_hash = entry.get("hash")
                payload_str = json.dumps(entry.get("payload", {}), sort_keys=True)
                timestamp = entry.get("timestamp")

                if actual_prev != expected_prev_hash:
                    return False

                raw_signature = f"{actual_prev}:{payload_str}:{timestamp}"
                computed_hash = hashlib.sha256(raw_signature.encode("utf-8")).hexdigest()

                if computed_hash != actual_hash:
                    return False

                expected_prev_hash = actual_hash

        return True
