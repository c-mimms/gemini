import json
from typing import Any, Dict, List
from stateful_generator_core.core.idea_engine import IdeaEngine, Node

class LLMIdeaEngine(IdeaEngine):
    def __init__(self, config, storage, run_logger, tool_registry, model, seed=None):
        super().__init__(config, storage, run_logger=run_logger, tool_registry=tool_registry, seed=seed)
        self.model = model

    def _render_template(self, template: str, agent: Dict[str, Any], inputs: List[Node]) -> str:
        # Get the default formatting from the original template
        formatted_inputs = super()._render_template(template, agent, inputs)
        
        system_prompt = f"You are acting in the role of: {agent.get('role', 'Helpful Assistant')}."
        user_prompt = f"Instructions/Template details: {formatted_inputs}\n\n"
        
        # Add contents of any inputs to the prompt
        if inputs:
            user_prompt += "Here are the input nodes available to you:\n"
            for node in inputs:
                user_prompt += f"--- NODE TYPE: {node.type} ---\n{node.content}\n\n"
                
        # Handle tools if the format requires it
        perms = agent.get("permissions", {})
        if perms.get("web_search") and inputs:
            # Simple heuristic: If allowed to web search, search the content of the first input (Topic)
            if self.tool_registry:
                try:
                    search_results = self.tool_registry.call("web_search", {"query": inputs[0].content}, allowlist=["web_search"])
                    user_prompt += f"--- WEB SEARCH RESULTS FOR '{inputs[0].content}' ---\n"
                    # Format standard web_search results which are dicts
                    if isinstance(search_results, list):
                        for res in search_results:
                            url = res.get("url", "unknown_url")
                            snippet_text = res.get("text", "")[:400]
                            user_prompt += f"URL: {url}\nSnippet: {snippet_text}\n\n"
                except ValueError:
                    pass

        # Send to the LLM model
        response = self.model.generate(system_prompt=system_prompt, user_prompt=user_prompt)
        return response.text.strip()
