import os
import json
from typing import Type, TypeVar
from pydantic import BaseModel
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

T = TypeVar('T', bound=BaseModel)

class GeneratorError(Exception):
    pass

def generate_structured(
    instructions: str, 
    user_prompt: str,
    response_schema: Type[T], 
    model_name: str = "gemini-2.5-flash"
) -> T:
    """
    Generates content matching the response_schema using the configured LLM.
    Prefers Google GenAI, falls back to OpenAI if configured.
    """
    if "gemini" in model_name.lower():
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key and genai:
            client = genai.Client(api_key=api_key)
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=instructions,
                        response_mime_type="application/json",
                        response_schema=response_schema,
                        temperature=0.7,
                    ),
                )
                return response_schema.model_validate_json(response.text)
            except Exception as e:
                raise GeneratorError(f"Generation failed: {e}")
        else:
            # Fall back to user's gemini CLI which is likely authenticated
            import subprocess
            system_instruction = instructions + "\n\nYou MUST return ONLY valid JSON matching this schema:\n" + json.dumps(response_schema.model_json_schema())
            full_prompt = f"System Instruction: {system_instruction}\n\nUser Task: {user_prompt}"
            try:
                print("Falling back to gemini cli subprocess...")
                output = subprocess.check_output(
                    ["gemini", "-p", full_prompt, "-y"],
                    text=True,
                    stderr=subprocess.STDOUT
                ).strip()
                
                # Extract JSON block
                if "```json" in output:
                    output = output.split("```json")[1].split("```")[0].strip()
                elif "```" in output:
                    output = output.split("```")[1].split("```")[0].strip()
                    
                return response_schema.model_validate_json(output)
            except Exception as e:
                raise GeneratorError(f"CLI Generation failed: {e}")

    elif "gpt" in model_name.lower() or "o1" in model_name.lower() or "o3" in model_name.lower():
        if not OpenAI:
            raise GeneratorError("openai missing. Run: pip install openai")
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise GeneratorError("OPENAI_API_KEY environment variable not set.")
            
        client = OpenAI(api_key=api_key)
        try:
            # We use structured outputs parsing
            completion = client.beta.chat.completions.parse(
                model=model_name,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=response_schema
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            raise GeneratorError(f"Generation failed: {e}")
            
    else:
        raise GeneratorError(f"Unsupported model: {model_name}")
