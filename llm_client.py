import openai
import os
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

# Get API key from .env or environment
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not found in environment or .env file.")
def call_llm(prompt: str) -> str:
    """Call LLM with the prompt and return response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling LLM: {e}"

def build_prompt(user_message: str, memories: list) -> str:
    """Build complete prompt with memories."""
    system = (
        "You are a helpful assistant. "
        "You know some facts about the user from previous conversations. "
        "Use them naturally when relevant, but don't list them unless asked."
    )
    
    mem_text = ""
    if memories:
        facts = [f"{m['key']}: {m['value']}" for m in memories]
        mem_text = "User facts:\n" + "\n".join(facts) + "\n\n"
    
    return f"{system}\n\n{mem_text}User: {user_message}\nAssistant:"
