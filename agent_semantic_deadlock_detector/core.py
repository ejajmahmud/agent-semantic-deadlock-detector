"""Core Semantic Deadlock Detector."""
from typing import Dict, List, Set, Optional, Tuple
import time

class AgentWaitState:
    def __init__(self, agent_id: str, waiting_for_agent_id: str, reason: str, priority: int = 1):
        self.agent_id = agent_id
        self.waiting_for_agent_id = waiting_for_agent_id
        self.reason = reason
        self.priority = priority
        self.timestamp = time.time()

class DeadlockCycle:
    def __init__(self, cycle_path: List[str], victim_agent_id: str):
        self.cycle_path = cycle_path
        self.victim_agent_id = victim_agent_id

class DeadlockDetector:
    def __init__(self):
        self.wait_for_graph: Dict[str, AgentWaitState] = {}

    def register_wait(self, agent_id: str, waiting_for_id: str, reason: str, priority: int = 1) -> Optional[DeadlockCycle]:
        self.wait_for_graph[agent_id] = AgentWaitState(agent_id, waiting_for_id, reason, priority)
        return self.detect_deadlock()

    def release_wait(self, agent_id: str):
        if agent_id in self.wait_for_graph:
            del self.wait_for_graph[agent_id]

    def detect_deadlock(self) -> Optional[DeadlockCycle]:
        visited: Set[str] = set()
        stack: List[str] = []

        for start_agent in list(self.wait_for_graph.keys()):
            if start_agent not in visited:
                curr = start_agent
                path: List[str] = []
                local_visited: Set[str] = set()

                while curr in self.wait_for_graph:
                    if curr in local_visited:
                        # Found cycle
                        cycle_idx = path.index(curr)
                        cycle = path[cycle_idx:] + [curr]
                        # Select victim with lowest priority
                        victim = min(cycle[:-1], key=lambda a: self.wait_for_graph[a].priority)
                        return DeadlockCycle(cycle, victim)
                    
                    local_visited.add(curr)
                    visited.add(curr)
                    path.append(curr)
                    curr = self.wait_for_graph[curr].waiting_for_agent_id

        return None
