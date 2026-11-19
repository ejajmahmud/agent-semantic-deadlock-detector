"""Tests for Deadlock Detector."""
import unittest
from agent_semantic_deadlock_detector.core import DeadlockDetector

class TestDeadlockDetector(unittest.TestCase):
    def test_no_deadlock(self):
        d = DeadlockDetector()
        d.register_wait("a", "b", "need token")
        d.register_wait("b", "c", "need lock")
        self.assertIsNone(d.detect_deadlock())

    def test_cycle_and_victim_selection(self):
        d = DeadlockDetector()
        d.register_wait("a", "b", "r1", priority=10)
        d.register_wait("b", "c", "r2", priority=5)
        cycle = d.register_wait("c", "a", "r3", priority=2)
        
        self.assertIsNotNone(cycle)
        self.assertEqual(cycle.victim_agent_id, "c") # lowest priority
