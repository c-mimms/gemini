import json
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class EngineConfig:
    name: str
    version: int
    node_types: Dict[str, Dict[str, Any]]
    edge_types: Dict[str, Dict[str, Any]]
    agents: List[Dict[str, Any]]
    validators: Dict[str, Any]
    run_policy: Dict[str, Any]

    @staticmethod
    def load(path: str) -> "EngineConfig":
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        required = ["name", "version", "node_types", "edge_types", "agents", "validators", "run_policy"]
        for key in required:
            if key not in raw:
                raise ValueError(f"Missing required config key: {key}")

        return EngineConfig(
            name=raw["name"],
            version=raw["version"],
            node_types=raw["node_types"],
            edge_types=raw["edge_types"],
            agents=raw["agents"],
            validators=raw["validators"],
            run_policy=raw["run_policy"],
        )

    def agent_by_id(self, agent_id: str) -> Dict[str, Any]:
        for agent in self.agents:
            if agent.get("id") == agent_id:
                return agent
        raise ValueError(f"Unknown agent id: {agent_id}")
