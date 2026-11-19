"""CLI for Deadlock Detector."""
import argparse
from .core import DeadlockDetector

def main():
    parser = argparse.ArgumentParser(description="Agent Semantic Deadlock Detector CLI")
    parser.add_argument("--demo", action="store_true", help="Run deadlock detection demo")
    args = parser.parse_args()

    det = DeadlockDetector()
    det.register_wait("agent-a", "agent-b", "Waiting for data", priority=2)
    cycle = det.register_wait("agent-b", "agent-a", "Waiting for approval", priority=1)
    
    if cycle:
        print(f"Deadlock detected! Cycle: {' -> '.join(cycle.cycle_path)}, Victim to preempt: {cycle.victim_agent_id}")

if __name__ == "__main__":
    main()
