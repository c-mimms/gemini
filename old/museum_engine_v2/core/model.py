import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ModelResponse:
    text: str


class ModelClient:
    def generate(self, system_prompt: str, user_prompt: str) -> ModelResponse:
        raise NotImplementedError


class StubModel(ModelClient):
    def generate(self, system_prompt: str, user_prompt: str) -> ModelResponse:
        # Deterministic, minimal HTML output for tests and offline runs.
        html = (
            "<main class=\"museum-body\">"
            "<div class=\"metadata\" style=\"display:none;\">"
            "<meta name=\"title\" content=\"Stub Museum Article\">"
            "<meta name=\"description\" content=\"Stub content.\">"
            "<meta name=\"tag\" content=\"Stub | Museum\">"
            "</div>"
            "<h1>Stub Museum Article</h1>"
            "<p>This is a stubbed museum article body.</p>"
            "</main>"
        )
        return ModelResponse(text=html)


class OpenAIModel(ModelClient):
    def __init__(self, model: Optional[str] = None):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required for OpenAIModel.")
        try:
            from openai import OpenAI  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("openai package is required for OpenAIModel.") from exc
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, system_prompt: str, user_prompt: str) -> ModelResponse:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = response.output_text.strip()
        return ModelResponse(text=text)


class GeminiCLIModel(ModelClient):
    def generate(self, system_prompt: str, user_prompt: str) -> ModelResponse:
        import subprocess
        import sys
        full_prompt = f"System Instruction: {system_prompt}\n\nUser Task: {user_prompt}"
        try:
            output = subprocess.check_output(
                ["gemini", "-p", full_prompt, "-y"],
                text=True,
                stderr=sys.stderr
            )
            return ModelResponse(text=output.strip())
        except subprocess.CalledProcessError as e:
            return ModelResponse(text=f"Error from Gemini CLI: {e.output}")


def load_model() -> ModelClient:
    mode = os.getenv("MUSEUM_ENGINE_MODEL", "gemini").lower()
    if mode == "openai":
        return OpenAIModel()
    elif mode == "gemini":
        return GeminiCLIModel()
    return StubModel()
