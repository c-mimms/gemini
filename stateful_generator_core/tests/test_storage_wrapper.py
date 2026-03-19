import tempfile
import unittest


class StorageWrapperTests(unittest.TestCase):
    def test_graph_store_update_content_allows_override(self):
        from stateful_generator_core.core.graph_store import GraphStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = GraphStore(str(tmpdir))
            node = store.create_node("Idea", "immutable", "agent_a")

            with self.assertRaises(ValueError):
                store.update_content(node.id, "changed")

            store.update_content(node.id, "changed", allow_immutable=True)
            reloaded = GraphStore(str(tmpdir))
            self.assertEqual(reloaded.get_node(node.id).content, "changed")

    def test_graph_store_get_node_returns_copy(self):
        from stateful_generator_core.core.graph_store import GraphStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = GraphStore(str(tmpdir))
            node = store.create_node(
                "Idea",
                "immutable",
                "agent_a",
                metadata={"content_mutable": False},
            )
            fetched = store.get_node(node.id)
            fetched.content = "bypassed"

            store.update_metadata(node.id, {"tag": "metadata-write"})
            reloaded = GraphStore(str(tmpdir))
            self.assertEqual(reloaded.get_node(node.id).content, "immutable")

    def test_storage_wrapper_enforces_immutability(self):
        from stateful_generator_core.core.storage_wrapper import StorageWrapper

        with tempfile.TemporaryDirectory() as tmpdir:
            storage = StorageWrapper(base_path=str(tmpdir))
            node = storage.create_node("Idea", "immutable", "agent_a", content_mutable=False)

            with self.assertRaises(ValueError):
                storage.update_content(node.id, "changed")

    def test_storage_wrapper_allows_mutable_update(self):
        from stateful_generator_core.core.storage_wrapper import StorageWrapper

        with tempfile.TemporaryDirectory() as tmpdir:
            storage = StorageWrapper(base_path=str(tmpdir))
            node = storage.create_node("Idea", "mutable", "agent_a", content_mutable=True)
            storage.update_content(node.id, "changed")

            reloaded = StorageWrapper(base_path=str(tmpdir))
            self.assertEqual(reloaded.get_node(node.id).content, "changed")

    def test_storage_wrapper_copies_metadata(self):
        from stateful_generator_core.core.storage_wrapper import StorageWrapper

        with tempfile.TemporaryDirectory() as tmpdir:
            storage = StorageWrapper(base_path=str(tmpdir))
            metadata = {"content_mutable": True, "tag": "source"}
            node = storage.create_node(
                "Idea",
                "immutable",
                "agent_a",
                metadata=metadata,
                content_mutable=False,
            )
            metadata["content_mutable"] = True

            reloaded = StorageWrapper(base_path=str(tmpdir))
            reloaded_node = reloaded.get_node(node.id)
            self.assertFalse(reloaded_node.metadata["content_mutable"])
            self.assertEqual(reloaded_node.metadata["tag"], "source")


if __name__ == "__main__":
    unittest.main()
