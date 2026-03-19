import copy
import json
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class Node:
    id: str
    type: str
    content: str
    metadata: Dict[str, Any]
    created_at: str
    created_by: str


@dataclass
class Edge:
    from_id: str
    to_id: str
    type: str
    metadata: Dict[str, Any]


class GraphStore:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.graph_path = os.path.join(base_path, "graph")
        self.nodes_path = os.path.join(self.graph_path, "nodes.jsonl")
        self.edges_path = os.path.join(self.graph_path, "edges.jsonl")
        os.makedirs(self.graph_path, exist_ok=True)

        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.nodes_path):
            with open(self.nodes_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    raw = json.loads(line)
                    self.nodes[raw["id"]] = Node(**raw)
        if os.path.exists(self.edges_path):
            with open(self.edges_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    raw = json.loads(line)
                    self.edges.append(Edge(**raw))

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def create_node(
        self,
        node_type: str,
        content: str,
        created_by: str,
        metadata: Optional[Dict[str, Any]] = None,
        node_id: Optional[str] = None,
    ) -> Node:
        if node_id is None:
            node_id = str(uuid.uuid4())
        if node_id in self.nodes:
            raise ValueError(f"Node id already exists: {node_id}")
        meta = copy.deepcopy(metadata) if metadata else {}
        node = Node(
            id=node_id,
            type=node_type,
            content=content,
            metadata=meta,
            created_at=self._now_iso(),
            created_by=created_by,
        )
        self.nodes[node.id] = node
        with open(self.nodes_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(node.__dict__) + "\n")
        return self._clone_node(node)

    def update_metadata(self, node_id: str, patch: Dict[str, Any]) -> Node:
        node = self._get_node_ref(node_id)
        node.metadata.update(copy.deepcopy(patch))
        self._rewrite_nodes()
        return self._clone_node(node)

    def get_node(self, node_id: str) -> Node:
        node = self._get_node_ref(node_id)
        return self._clone_node(node)

    def update_content(self, node_id: str, content: str, *, allow_immutable: bool = False) -> Node:
        node = self._get_node_ref(node_id)
        if not allow_immutable and not node.metadata.get("content_mutable", False):
            raise ValueError("Content is immutable")
        node.content = content
        self._rewrite_nodes()
        return self._clone_node(node)

    def update_content(self, node_id: str, content: str) -> Node:
        node = self.nodes.get(node_id)
        if not node:
            raise ValueError(f"Node not found: {node_id}")
        node.content = content
        self._rewrite_nodes()
        return node

    def _rewrite_nodes(self) -> None:
        with open(self.nodes_path, "w", encoding="utf-8") as f:
            for node in self.nodes.values():
                f.write(json.dumps(node.__dict__) + "\n")

    def create_edge(
        self,
        from_id: str,
        to_id: str,
        edge_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Edge:
        if from_id not in self.nodes or to_id not in self.nodes:
            raise ValueError("Edge references unknown node")
        edge = Edge(from_id=from_id, to_id=to_id, type=edge_type, metadata=metadata or {})
        self.edges.append(edge)
        with open(self.edges_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(edge.__dict__) + "\n")
        return edge

    def list_nodes(self, types: Optional[Iterable[str]] = None) -> List[Node]:
        if types is None:
            return [self._clone_node(n) for n in self.nodes.values()]
        type_set = set(types)
        return [self._clone_node(n) for n in self.nodes.values() if n.type in type_set]

    def list_edges(self, edge_type: Optional[str] = None) -> List[Edge]:
        if edge_type is None:
            return list(self.edges)
        return [e for e in self.edges if e.type == edge_type]

    @staticmethod
    def _clone_node(node: Node) -> Node:
        return Node(
            id=node.id,
            type=node.type,
            content=node.content,
            metadata=copy.deepcopy(node.metadata),
            created_at=node.created_at,
            created_by=node.created_by,
        )

    def _get_node_ref(self, node_id: str) -> Node:
        node = self.nodes.get(node_id)
        if not node:
            raise ValueError(f"Node not found: {node_id}")
        return node
