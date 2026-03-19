from .graph_store import GraphStore


class StorageWrapper:
    def __init__(self, base_path):
        self._store = GraphStore(base_path)

    def create_node(self, node_type, content, created_by, metadata=None, content_mutable=False):
        meta = dict(metadata or {})
        meta["content_mutable"] = bool(content_mutable)
        return self._store.create_node(node_type, content, created_by, meta)

    def get_node(self, node_id):
        return self._store.get_node(node_id)

    def update_content(self, node_id, new_content):
        return self._store.update_content(node_id, new_content)
