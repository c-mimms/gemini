import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .config import EngineConfig
from .graph_store import GraphStore, Node
from .run_log import RunLogger
from .storage_wrapper import StorageWrapper
from .tool_registry import ToolRegistry
from .scheduler import Scheduler


@dataclass
class RunResult:
    agent_id: str
    created_nodes: List[Node]
    created_edges: List[Any]


class ValidationError(Exception):
    pass


class IdeaEngine:
    def __init__(
        self,
        config: EngineConfig,
        storage: StorageWrapper,
        run_logger: Optional[RunLogger] = None,
        tool_registry: Optional[ToolRegistry] = None,
        seed: Optional[int] = None,
    ):
        self.config = config
        self.storage = storage
        self.store = storage._store
        self.run_logger = run_logger
        self.tool_registry = tool_registry
        self.scheduler = Scheduler(config.run_policy.get("agent_weights", {}), seed=seed)
        self.random = random.Random(seed)

    def run(self, agent_id: Optional[str] = None) -> RunResult:
        agent = self._select_agent(agent_id)
        run_record = None
        if self.run_logger:
            snapshot = getattr(self.config, "raw", {})
            run_record = self.run_logger.start_run(agent_id=agent["id"], config_snapshot=snapshot)

        inputs = self._select_inputs(agent)
        outputs, edges = self._generate_outputs(agent, inputs)
        max_outputs = self.config.run_policy.get("max_outputs_per_run")
        if isinstance(max_outputs, int) and max_outputs >= 0:
            outputs = outputs[:max_outputs]
            allowed_indices = {o["output_index"] for o in outputs}
            edges = [e for e in edges if e.get("output_index") in allowed_indices]
        self._validate(outputs, edges, agent)
        created_nodes = []
        created_edges = []
        output_id_map: Dict[int, str] = {}
        for node in outputs:
            created = self.storage.create_node(
                node_type=node["type"],
                content=node["content"],
                created_by=agent["id"],
                metadata=node.get("metadata", {}),
            )
            created_nodes.append(created)
            output_id_map[node["output_index"]] = created.id
        for edge in edges:
            from_id = edge["from_id"]
            if from_id == "__pending_output__":
                from_id = output_id_map[edge["output_index"]]
            created_edges.append(
                self.store.create_edge(
                    from_id=from_id,
                    to_id=edge["to_id"],
                    edge_type=edge["type"],
                    metadata=edge.get("metadata", {}),
                )
            )
        if run_record:
            # We don't have native tool calls yet, but we will pass empty list
            self.run_logger.finish_run(run_record, status="success", outputs=[n.id for n in created_nodes])
        return RunResult(agent_id=agent["id"], created_nodes=created_nodes, created_edges=created_edges)

    def _select_agent(self, agent_id: Optional[str]) -> Dict[str, Any]:
        if agent_id:
            return self.config.agent_by_id(agent_id)
        weights = self.config.run_policy.get("agent_weights", {})
        if not weights:
            return self.random.choice(self.config.agents)
        picked = self.scheduler.pick()
        return self.config.agent_by_id(picked)

    def _select_inputs(self, agent: Dict[str, Any]) -> List[Node]:
        perms = agent.get("permissions", {})
        read_types = perms.get("read_types", [])
        max_nodes = agent.get("input_policy", {}).get("max_nodes", 5)
        nodes = self.store.list_nodes(read_types if read_types else None)
        nodes = sorted(nodes, key=lambda n: n.created_at, reverse=True)
        return nodes[:max_nodes]

    def _generate_outputs(self, agent: Dict[str, Any], inputs: List[Node]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        output_policy = agent.get("output_policy", {})
        outputs = []
        edges = []
        for index, spec in enumerate(output_policy.get("outputs", [])):
            content = self._render_template(spec.get("content_template", ""), agent, inputs)
            outputs.append(
                {
                    "type": spec["type"],
                    "content": content,
                    "metadata": spec.get("metadata", {}),
                    "output_index": index,
                }
            )
        link_type = output_policy.get("link_to_inputs")
        if link_type:
            for output in outputs:
                # Edges are created after nodes, so we temporarily store input refs.
                for node in inputs:
                    edges.append(
                        {
                            "from_id": "__pending_output__",
                            "output_index": output["output_index"],
                            "to_id": node.id,
                            "type": link_type,
                        }
                    )
        cite_inputs = output_policy.get("cite_inputs", False)
        if cite_inputs:
            for output in outputs:
                for node in inputs:
                    edges.append(
                        {
                            "from_id": "__pending_output__",
                            "output_index": output["output_index"],
                            "to_id": node.id,
                            "type": "cites",
                        }
                    )
        return outputs, edges

    def _render_template(self, template: str, agent: Dict[str, Any], inputs: List[Node]) -> str:
        input_ids = ",".join([n.id for n in inputs]) if inputs else "none"
        input_types = ",".join(sorted({n.type for n in inputs})) if inputs else "none"
        return template.format(
            agent_id=agent["id"],
            role=agent.get("role", ""),
            input_ids=input_ids,
            input_types=input_types,
        )

    def _validate(self, outputs: List[Dict[str, Any]], edges: List[Dict[str, Any]], agent: Dict[str, Any]) -> None:
        validators = self.config.validators
        if validators.get("schema", False):
            for output in outputs:
                if output["type"] not in self.config.node_types:
                    raise ValidationError(f"Unknown node type: {output['type']}")
                if not output["content"]:
                    raise ValidationError("Empty content is not allowed")

        format_rules = validators.get("format", {})
        for output in outputs:
            rule = format_rules.get(output["type"])
            if not rule:
                continue
            must_include = rule.get("must_include", [])
            for fragment in must_include:
                if fragment not in output["content"]:
                    raise ValidationError(f"Missing required fragment for {output['type']}: {fragment}")

        citation_rules = validators.get("citation_requirements", {})
        for output in outputs:
            rule = citation_rules.get(output["type"])
            if not rule:
                continue
            required = rule.get("min", 0)
            edge_type = rule.get("edge_type", "cites")
            count = sum(1 for e in edges if e["type"] == edge_type)
            if count < required:
                raise ValidationError(f"{output['type']} requires at least {required} {edge_type} edges")

        perms = agent.get("permissions", {})
        allowed_types = set(perms.get("write_types", []))
        for output in outputs:
            if allowed_types and output["type"] not in allowed_types:
                raise ValidationError(f"Agent {agent['id']} cannot write node type: {output['type']}")
