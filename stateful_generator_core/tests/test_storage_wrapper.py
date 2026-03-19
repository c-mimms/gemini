import tempfile
import unittest


class StorageWrapperTests(unittest.TestCase):
    def test_storage_wrapper_enforces_immutability(self):
        from stateful_generator_core.core.storage_wrapper import StorageWrapper

        with tempfile.TemporaryDirectory() as tmpdir:
            storage = StorageWrapper(base_path=str(tmpdir))
            node = storage.create_node("Idea", "immutable", "agent_a", content_mutable=False)

            with self.assertRaises(ValueError):
                storage.update_content(node.id, "changed")


if __name__ == "__main__":
    unittest.main()
