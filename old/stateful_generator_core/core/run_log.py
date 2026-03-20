import json
import os
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class RunRecord:
    run_id: str
    agent_id: str
    inputs: List[Any]
    outputs: List[Any]
    tool_calls: List[Any]
    timing: Dict[str, float]
    token_usage: Dict[str, Any]
    status: str
    config_snapshot: Dict[str, Any]


class RunLogger:
    def __init__(self, base_path):
        self.runs_path = os.path.join(base_path, "runs")
        os.makedirs(self.runs_path, exist_ok=True)

    def start_run(self, agent_id, config_snapshot):
        run_id = str(uuid.uuid4())
        record = {
            "run_id": run_id,
            "agent_id": agent_id,
            "inputs": [],
            "outputs": [],
            "tool_calls": [],
            "timing": {"start": time.time()},
            "token_usage": {},
            "status": "running",
            "config_snapshot": config_snapshot,
        }
        self._write(run_id, record)
        return RunRecord(**record)

    def finish_run(self, run_record, status, outputs):
        record = self.load_run(run_record.run_id)
        record["status"] = status
        record["outputs"] = outputs
        record["timing"]["end"] = time.time()
        self._write(run_record.run_id, record)

    def load_run(self, run_id):
        with open(os.path.join(self.runs_path, f"{run_id}.json"), "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, run_id, record):
        with open(os.path.join(self.runs_path, f"{run_id}.json"), "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)
