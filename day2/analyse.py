import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

MODEL = "gemini-3.5-flash-lite"
PROMPT_FILE = Path("prompts/analyser_v2.md")

def analyse(posting: str) -> str:
    system_prompt = PROMPT_FILE.read_text()
    user_message = f"<job_posting>\n{posting}\n</job_posting>"

    response = client.models.generate_content(
        model=MODEL,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            thinking_config=types.ThinkingConfig(thinking_level="low")
        )
    )

    return response.text


if __name__ == "__main__":
    posting_file = Path(sys.argv[1])
    print(analyse(posting_file.read_text()))