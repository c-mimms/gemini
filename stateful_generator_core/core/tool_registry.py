class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, fn):
        self.tools[name] = fn

    def call(self, name, params, allowlist):
        if name not in allowlist:
            raise ValueError("Tool not allowed")
        return self.tools[name](**params)
