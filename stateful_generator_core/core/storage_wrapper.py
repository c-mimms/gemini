from .graph_store import GraphStore


class StorageWrapper:
    def __init__(self, base_path):
        self.store = GraphStore(base_path)

    def create_node(self, node_type, content, created_by, metadata=None, content_mutable=False):
        meta = dict(metadata or {})
        meta["content_mutable"] = bool(content_mutable)
        return self.store.create_node(node_type, content, created_by, meta)

    def update_content(self, node_id, new_content):
        node = self.store.nodes.get(node_id)
        if not node:
            raise ValueError("Node not found")
        if not node.metadata.get("content_mutable"):
            raise ValueError("Content is immutable")
        node.content = new_content
        self.store._rewrite_nodes()
        return node
