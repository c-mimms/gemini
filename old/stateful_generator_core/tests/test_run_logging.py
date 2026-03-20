import tempfile
import unittest


class RunLoggingTests(unittest.TestCase):
    def test_run_log_writes_config_snapshot(self):
        from stateful_generator_core.core.run_log import RunLogger

        logger = RunLogger(base_path=str(tempfile.mkdtemp()))
        log = logger.start_run(agent_id="agent_a", config_snapshot={"name": "test"})
        logger.finish_run(log, status="success", outputs=["node1"])
        stored = logger.load_run(log.run_id)

        self.assertEqual(stored["config_snapshot"]["name"], "test")


if __name__ == "__main__":
    unittest.main()
