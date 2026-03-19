import json
import uuid
from typing import Dict, List, Any

class StateManager:
    """Manages the strict State Graph of the simulated universe."""
    def __init__(self):
        self.entities = {
            "CEO": {"id": "CEO_01", "name": "Alice Innovator", "status": "Optimistic"},
            "DB": {"id": "DB_PRIMARY", "type": "PostgreSQL", "status": "Online"}
        }
        self.events_ledger = []
    
    def get_context(self) -> str:
        return json.dumps(self.entities, indent=2)

    def apply_patch(self, patch: Dict[str, Any]):
        """Applies a state mutation resulting from an agent action."""
        for entity_id, updates in patch.items():
            if entity_id in self.entities:
                self.entities[entity_id].update(updates)
            else:
                self.entities[entity_id] = updates
        self.events_ledger.append({"patch_applied": patch})

class MockAgent:
    """Simulates an LLM agent that reads state and outputs markdown + stater mutations."""
    def __init__(self, role: str):
        self.role = role

    def generate(self, context: str, trigger: str) -> Dict[str, Any]:
        """Mock LLM generation based on context and trigger."""
        print(f"[{self.role}] Analyzing Trigger: {trigger}")
        
        # In a real system, this would be an LLM API call.
        if "outage" in trigger.lower():
            markdown_content = f"# Incident Report\n\nDatabase `{json.loads(context)['DB']['type']}` went offline."
            state_mutation = {"DB": {"status": "Offline"}}
            slack_log = "**DevOps_Bob:** THE DB IS DOWN. PANIC."
        else:
            markdown_content = "# Daily Log\n\nEverything is operating normally."
            state_mutation = {}
            slack_log = "**DevOps_Bob:** All systems green."
            
        return {
            "artifact_html": markdown_content,
            "slack_transcript": slack_log,
            "state_mutation": state_mutation
        }

class AgenticOrchestrator:
    """The main event bus and pipeline execution engine."""
    def __init__(self):
        self.state = StateManager()
        self.agent = MockAgent(role="Crisis Responder")
        
    def run_tick(self, trigger_event: str):
        print(f"\n--- TICK START: {trigger_event} ---")
        
        # 1. Provide restricted context to agent
        current_state_json = self.state.get_context()
        print(f"System State before tick:\n{current_state_json}")
        
        # 2. Agent Generation
        response = self.agent.generate(context=current_state_json, trigger=trigger_event)
        
        # 3. Save Artifacts (Mock)
        artifact_id = str(uuid.uuid4())[:8]
        print(f"\n[Artifact Generated - {artifact_id}.md]")
        print(response["artifact_html"])
        print(f"\n[Slack Log Generated - {artifact_id}_slack.md]")
        print(response["slack_transcript"])
        
        # 4. Apply State Mutations
        if response["state_mutation"]:
             print(f"\n[Applying State Patch]: {response['state_mutation']}")
             self.state.apply_patch(response["state_mutation"])
             
        print("--- TICK COMPLETE ---\n")

if __name__ == "__main__":
    print("Initializing Stateful Agentic Generator Prototype...")
    orchestrator = AgenticOrchestrator()
    
    # Tick 1: Normal operational day
    orchestrator.run_tick("Perform routine system check.")
    
    # Tick 2: A crisis occurs
    orchestrator.run_tick("CRITICAL: Database connection timeout outage detected.")
    
    # Tick 3: Post-crisis check (State should reflect the database is now Offline)
    print("Final State Verification:")
    print(orchestrator.state.get_context())
