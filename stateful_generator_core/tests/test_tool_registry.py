import unittest


class ToolRegistryTests(unittest.TestCase):
    def test_tool_registry_enforces_allowlist(self):
        from stateful_generator_core.core.tool_registry import ToolRegistry

        registry = ToolRegistry()
        registry.register("web_search", lambda q: [])

        self.assertEqual(
            registry.call("web_search", {"q": "test"}, allowlist=["web_search"]),
            [],
        )

        with self.assertRaises(ValueError):
            registry.call("web_search", {"q": "test"}, allowlist=[])


if __name__ == "__main__":
    unittest.main()
