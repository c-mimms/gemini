import unittest

class SchedulerTests(unittest.TestCase):
    def test_scheduler_selects_weighted_agents(self):
        from stateful_generator_core.core.scheduler import Scheduler
        
        # With seed=1, the sequence of picks should be deterministic
        scheduler = Scheduler({"a": 3, "b": 1}, seed=1)
        picks = [scheduler.pick() for _ in range(10)]
        
        self.assertIn("a", picks)
        self.assertIn("b", picks)

if __name__ == "__main__":
    unittest.main()
