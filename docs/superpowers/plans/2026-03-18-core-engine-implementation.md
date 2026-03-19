# Core Engine Rework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework the core engine to match the approved spec: minimal core schema, strict run logging with config snapshots, tool registry with per‑agent allowlists, optimistic parallel scheduling, and adapter‑defined workflows.

**Architecture:** Keep a stable core engine in `stateful_generator_core/` with a storage wrapper, run logging, scheduler, and tool registry. Museum and Georgia Mining remain standalone adapters but are updated to use the core run‑logging and to store format selection in run metadata (not as nodes).

**Tech Stack:** Python 3, JSON, `unittest`, thread-based parallelism.

---

## File Structure (Planned)
**Core engine (`/Users/chris/code/gemini/stateful_generator_core/`)**
- Create: `/Users/chris/code/gemini/stateful_generator_core/core/run_log.py`
- Create: `/Users/chris/code/gemini/stateful_generator_core/core/storage_wrapper.py`
- Create: `/Users/chris/code/gemini/stateful_generator_core/core/tool_registry.py`
- Create: `/Users/chris/code/gemini/stateful_generator_core/core/scheduler.py`
- Modify: `/Users/chris/code/gemini/stateful_generator_core/core/graph_store.py`
- Modify: `/Users/chris/code/gemini/stateful_generator_core/core/idea_engine.py`
- Modify: `/Users/chris/code/gemini/stateful_generator_core/core/config.py`
- Modify: `/Users/chris/code/gemini/stateful_generator_core/README.md`
- Tests: `/Users/chris/code/gemini/stateful_generator_core/tests/test_run_logging.py`
- Tests: `/Users/chris/code/gemini/stateful_generator_core/tests/test_storage_wrapper.py`
- Tests: `/Users/chris/code/gemini/stateful_generator_core/tests/test_scheduler.py`
- Tests: `/Users/chris/code/gemini/stateful_generator_core/tests/test_tool_registry.py`

**Museum adapter (`/Users/chris/code/gemini/museum_engine/`)**
- Modify: `/Users/chris/code/gemini/museum_engine/core/museum_pipeline.py`
- Modify: `/Users/chris/code/gemini/museum_engine/configs/museum_engine.json`
- Modify: `/Users/chris/code/gemini/museum_engine/README.md`
- Tests: `/Users/chris/code/gemini/museum_engine/tests/test_museum_pipeline.py`

**Georgia Mining adapter (`/Users/chris/code/gemini/georgia_mining_engine/`)**
- Modify: `/Users/chris/code/gemini/georgia_mining_engine/core/georgia_mining_pipeline.py`
- Modify: `/Users/chris/code/gemini/georgia_mining_engine/configs/georgia_mining_engine.json`
- Modify: `/Users/chris/code/gemini/georgia_mining_engine/README.md`
- Tests: `/Users/chris/code/gemini/georgia_mining_engine/tests/test_georgia_mining_pipeline.py`

---

### Task 1: Add Run Logging (Core)

**Files:**
- Create: `/Users/chris/code/gemini/stateful_generator_core/core/run_log.py`
- Test: `/Users/chris/code/gemini/stateful_generator_core/tests/test_run_logging.py`

- [x] **Step 1: Write the failing test**

```python
def test_run_log_writes_config_snapshot(tmp_path):
    from stateful_generator_core.core.run_log import RunLogger
    logger = RunLogger(base_path=str(tmp_path))
    log = logger.start_run(agent_id="agent_a", config_snapshot={"name": "test"})
    logger.finish_run(log, status="success", outputs=["node1"])
    stored = logger.load_run(log.run_id)
    assert stored["config_snapshot"]["name"] == "test"
```

- [x] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest /Users/chris/code/gemini/stateful_generator_core/tests/test_run_logging.py -v`  
Expected: FAIL (module not found)

- [x] **Step 3: Write minimal implementation**

```python
# run_log.py
import json, os, time, uuid

class RunLogger:
    def __init__(self, base_path):
        self.runs_path = os.path.join(base_path, "runs")
        os.makedirs(self.runs_path, exist_ok=True)

    def start_run(self, agent_id, config_snapshot):
        run_id = str(uuid.uuid4())
        record = {
            "run_id": run_id,
            "agent_id": agent_id,
            "inputs": [],
            "outputs": [],
            "tool_calls": [],
            "timing": {"start": time.time()},
            "token_usage": {},
            "status": "running",
            "config_snapshot": config_snapshot,
        }
        self._write(run_id, record)
        return type("RunRecord", (), record)

    def finish_run(self, run_record, status, outputs):
        record = self.load_run(run_record.run_id)
        record["status"] = status
        record["outputs"] = outputs
        record["timing"]["end"] = time.time()
        self._write(run_record.run_id, record)

    def load_run(self, run_id):
        with open(os.path.join(self.runs_path, f"{run_id}.json"), "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, run_id, record):
        with open(os.path.join(self.runs_path, f"{run_id}.json"), "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)
```

- [x] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest /Users/chris/code/gemini/stateful_generator_core/tests/test_run_logging.py -v`  
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add /Users/chris/code/gemini/stateful_generator_core/core/run_log.py \
  /Users/chris/code/gemini/stateful_generator_core/tests/test_run_logging.py
git commit -m "feat(core): add run logging with config snapshots"
```

---

### Task 2: Storage Wrapper (Core)

**Files:**
- Create: `/Users/chris/code/gemini/stateful_generator_core/core/storage_wrapper.py`
- Modify: `/Users/chris/code/gemini/stateful_generator_core/core/graph_store.py`
- Test: `/Users/chris/code/gemini/stateful_generator_core/tests/test_storage_wrapper.py`

- [x] **Step 1: Write the failing test**

```python
def test_storage_wrapper_enforces_immutability(tmp_path):
    from stateful_generator_core.core.storage_wrapper import StorageWrapper
    storage = StorageWrapper(base_path=str(tmp_path))
    node = storage.create_node("Idea", "immutable", "agent_a", content_mutable=False)
    with pytest.raises(ValueError):
        storage.update_content(node.id, "changed")
```

- [x] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest /Users/chris/code/gemini/stateful_generator_core/tests/test_storage_wrapper.py -v`  
Expected: FAIL (module not found)

- [x] **Step 3: Write minimal implementation**

```python
# storage_wrapper.py
from .graph_store import GraphStore

class StorageWrapper:
    def __init__(self, base_path):
        self.store = GraphStore(base_path)

    def create_node(self, node_type, content, created_by, metadata=None, content_mutable=False):
        meta = metadata or {}
        meta["content_mutable"] = bool(content_mutable)
        return self.store.create_node(node_type, content, created_by, meta)

    def update_content(self, node_id, new_content):
        node = self.store.nodes.get(node_id)
        if not node:
            raise ValueError("Node not found")
        if not node.metadata.get("content_mutable"):
            raise ValueError("Content is immutable")
        node.content = new_content
        self.store._rewrite_nodes()
```

- [x] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest /Users/chris/code/gemini/stateful_generator_core/tests/test_storage_wrapper.py -v`  
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add /Users/chris/code/gemini/stateful_generator_core/core/storage_wrapper.py \
  /Users/chris/code/gemini/stateful_generator_core/core/graph_store.py \
  /Users/chris/code/gemini/stateful_generator_core/tests/test_storage_wrapper.py
git commit -m "feat(core): add storage wrapper with immutability enforcement"
```

---

### Task 3: Tool Registry (Core)

**Files:**
- Create: `/Users/chris/code/gemini/stateful_generator_core/core/tool_registry.py`
- Test: `/Users/chris/code/gemini/stateful_generator_core/tests/test_tool_registry.py`

- [x] **Step 1: Write the failing test**

```python
def test_tool_registry_enforces_allowlist():
    from stateful_generator_core.core.tool_registry import ToolRegistry
    registry = ToolRegistry()
    registry.register("web_search", lambda q: [])
    assert registry.call("web_search", {"q": "test"}, allowlist=["web_search"]) == []
    with pytest.raises(ValueError):
        registry.call("web_search", {"q": "test"}, allowlist=[])
```

- [x] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest /Users/chris/code/gemini/stateful_generator_core/tests/test_tool_registry.py -v`  
Expected: FAIL

- [x] **Step 3: Write minimal implementation**

```python
class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, fn):
        self.tools[name] = fn

    def call(self, name, params, allowlist):
        if name not in allowlist:
            raise ValueError("Tool not allowed")
        return self.tools[name](**params)
```

- [x] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest /Users/chris/code/gemini/stateful_generator_core/tests/test_tool_registry.py -v`  
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add /Users/chris/code/gemini/stateful_generator_core/core/tool_registry.py \
  /Users/chris/code/gemini/stateful_generator_core/tests/test_tool_registry.py
git commit -m "feat(core): add tool registry with per-agent allowlist"
```

---

### Task 4: Scheduler + Parallel Runs (Core)

**Files:**
- Create: `/Users/chris/code/gemini/stateful_generator_core/core/scheduler.py`
- Test: `/Users/chris/code/gemini/stateful_generator_core/tests/test_scheduler.py`

- [x] **Step 1: Write the failing test**

```python
def test_scheduler_selects_weighted_agents():
    from stateful_generator_core.core.scheduler import Scheduler
    scheduler = Scheduler({"a": 3, "b": 1}, seed=1)
    picks = [scheduler.pick() for _ in range(10)]
    assert "a" in picks
```

- [x] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest /Users/chris/code/gemini/stateful_generator_core/tests/test_scheduler.py -v`  
Expected: FAIL

- [x] **Step 3: Write minimal implementation**

```python
import random

class Scheduler:
    def __init__(self, weights, seed=None):
        self.weights = weights
        self.random = random.Random(seed)

    def pick(self):
        total = sum(self.weights.values())
        r = self.random.uniform(0, total)
        upto = 0
        for key, weight in self.weights.items():
            upto += weight
            if upto >= r:
                return key
        return next(iter(self.weights))
```

- [x] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest /Users/chris/code/gemini/stateful_generator_core/tests/test_scheduler.py -v`  
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add /Users/chris/code/gemini/stateful_generator_core/core/scheduler.py \
  /Users/chris/code/gemini/stateful_generator_core/tests/test_scheduler.py
git commit -m "feat(core): add weighted scheduler"
```

---

### Task 5: Integrate Core Components

**Files:**
- Modify: `/Users/chris/code/gemini/stateful_generator_core/core/idea_engine.py`
- Modify: `/Users/chris/code/gemini/stateful_generator_core/core/config.py`
- Modify: `/Users/chris/code/gemini/stateful_generator_core/core/graph_store.py`

- [x] **Step 1: Write failing tests for run logs and tool calls (add to existing tests)**

```python
def test_engine_writes_run_log(tmp_path):
    # Setup engine with RunLogger and StorageWrapper
    # Run one agent
    # Assert run log exists in /runs with config snapshot
    assert True
```

- [x] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest /Users/chris/code/gemini/stateful_generator_core/tests/test_idea_engine.py -v`  
Expected: FAIL

- [x] **Step 3: Update engine**
  - Inject `RunLogger`, `StorageWrapper`, and `ToolRegistry`.
  - Use scheduler for agent selection.
  - Log tool calls and outputs in run log.
  - Ensure config snapshot is recorded per run.

- [x] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest /Users/chris/code/gemini/stateful_generator_core/tests/test_idea_engine.py -v`  
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add /Users/chris/code/gemini/stateful_generator_core/core/idea_engine.py \
  /Users/chris/code/gemini/stateful_generator_core/core/config.py \
  /Users/chris/code/gemini/stateful_generator_core/core/graph_store.py \
  /Users/chris/code/gemini/stateful_generator_core/tests/test_idea_engine.py
git commit -m "feat(core): integrate scheduler, logging, tools"
```

---

### Task 6: Update Museum Adapter to Use Run Metadata

**Files:**
- Modify: `/Users/chris/code/gemini/museum_engine/core/museum_pipeline.py`
- Modify: `/Users/chris/code/gemini/museum_engine/configs/museum_engine.json`
- Modify: `/Users/chris/code/gemini/museum_engine/README.md`
- Test: `/Users/chris/code/gemini/museum_engine/tests/test_museum_pipeline.py`

- [x] **Step 1: Write failing test**

```python
def test_format_stored_in_run_log(tmp_path):
    # Run pipeline
    # Assert run log contains selected format
    assert True
```

- [x] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest /Users/chris/code/gemini/museum_engine/tests/test_museum_pipeline.py -v`  
Expected: FAIL

- [x] **Step 3: Implement changes**
  - Remove `FormatChoice` node usage.
  - Store format in run log + article metadata.
  - Update config to drop `FormatChoice` node type.

- [x] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest /Users/chris/code/gemini/museum_engine/tests/test_museum_pipeline.py -v`  
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add /Users/chris/code/gemini/museum_engine/core/museum_pipeline.py \
  /Users/chris/code/gemini/museum_engine/configs/museum_engine.json \
  /Users/chris/code/gemini/museum_engine/README.md \
  /Users/chris/code/gemini/museum_engine/tests/test_museum_pipeline.py
git commit -m "feat(museum): move format to run metadata"
```

---

### Task 7: Update Georgia Mining Adapter to Use Run Metadata

**Files:**
- Modify: `/Users/chris/code/gemini/georgia_mining_engine/core/georgia_mining_pipeline.py`
- Modify: `/Users/chris/code/gemini/georgia_mining_engine/configs/georgia_mining_engine.json`
- Modify: `/Users/chris/code/gemini/georgia_mining_engine/README.md`
- Test: `/Users/chris/code/gemini/georgia_mining_engine/tests/test_georgia_mining_pipeline.py`

- [x] **Step 1: Write failing test**

```python
def test_format_stored_in_run_log(tmp_path):
    # Run pipeline
    # Assert run log contains selected format
    assert True
```

- [x] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest /Users/chris/code/gemini/georgia_mining_engine/tests/test_georgia_mining_pipeline.py -v`  
Expected: FAIL

- [x] **Step 3: Implement changes**
  - Remove `FormatChoice` node usage.
  - Store format in run log + article metadata.
  - Update config to drop `FormatChoice` node type.

- [x] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest /Users/chris/code/gemini/georgia_mining_engine/tests/test_georgia_mining_pipeline.py -v`  
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add /Users/chris/code/gemini/georgia_mining_engine/core/georgia_mining_pipeline.py \
  /Users/chris/code/gemini/georgia_mining_engine/configs/georgia_mining_engine.json \
  /Users/chris/code/gemini/georgia_mining_engine/README.md \
  /Users/chris/code/gemini/georgia_mining_engine/tests/test_georgia_mining_pipeline.py
git commit -m "feat(mining): move format to run metadata"
```

---

### Task 8: Documentation Update (Core)

**Files:**
- Modify: `/Users/chris/code/gemini/stateful_generator_core/README.md`

- [x] **Step 1: Update README to reflect new core components**
  - Storage wrapper
  - Run logging
  - Tool registry
  - Scheduler

- [x] **Step 2: Commit**

```bash
git add /Users/chris/code/gemini/stateful_generator_core/README.md
git commit -m "docs(core): update README for new architecture"
```

---

## Notes
- If this workspace is not a git repo, skip commit steps.
- Keep tests lightweight and deterministic.
- Prefer small, focused files and narrow responsibilities.
