# State Layer Schemas

These schemas define the "Architecture as State" that the agents must adhere to.

## World State Schema (`world_state.schema.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "World State Node",
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "name": { "type": "string" },
    "type": { "enum": ["Entity", "Location", "Event", "Concept"] },
    "attributes": { "type": "object" },
    "established_facts": {
      "type": "array",
      "items": { "type": "string" }
    },
    "relationships": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "target_id": { "type": "string" },
          "relation_type": { "type": "string" }
        }
      }
    }
  },
  "required": ["id", "name", "type"]
}
```

## Agent Registry Schema (`agent_registry.schema.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Persona",
  "type": "object",
  "properties": {
    "role": { "type": "string" },
    "objective": { "type": "string" },
    "boundary_rules": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```
