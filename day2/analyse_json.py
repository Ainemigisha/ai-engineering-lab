import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError, field_validator

load_dotenv()
client = genai.Client()

MODEL = "gemini-3.5-flash-lite"        
PROMPT_FILE = Path("prompts/analyser_v3.md")
MAX_ATTEMPTS = 2


class JobAnalysis(BaseModel):
    title: str = Field(description="Job title, including the team name if one is given")
    seniority: Literal["Junior", "Mid-level", "Senior", "Not stated"] = Field(description="The exact words from the posting that support the seniority, or 'None' if nothing supports it")
    required_skills: list[str] = Field(  description="Short skill or technology names, 1 to 4 words each" )
    nice_to_have_skills: list[str] = Field( description="Short skill or technology names, 1 to 4 words each" )
    location_eligibility: str

    @field_validator("required_skills", "nice_to_have_skills")
    @classmethod
    def short_skills(cls, skills: list[str]) -> list[str]:
        for skill in skills:
            if len(skill.split()) > 4:
                raise ValueError(f"Skill too long, use 4 words or fewer: {skill}")
        return skills





def analyse(posting: str) -> JobAnalysis:
    system_prompt = PROMPT_FILE.read_text()
    user_message = f"<job_posting>\n{posting}\n</job_posting>"

    for attempt in range(1, MAX_ATTEMPTS + 1):
        response = client.models.generate_content(
            model=MODEL,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_json_schema=JobAnalysis.model_json_schema(),
            ),
        )
        try:
            return JobAnalysis.model_validate_json(response.text)
        except ValidationError as e:
            print(f"Attempt {attempt} failed: {e}")
            user_message += (
                f"\n\nYour previous answer failed validation:\n{e}\n"
                f"\nYour previous answer was:\n{response.text}\n"
                "Return corrected JSON."
            )

    raise RuntimeError("Could not get valid JSON from the model")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = analyse(Path(sys.argv[1]).read_text())
        print(result.model_dump_json(indent=2))
    else:
        Path("results").mkdir(exist_ok=True)
        for file in sorted(Path("postings").glob("*.txt")):
            result = analyse(file.read_text())
            out_file = Path("results") / f"{file.stem}.json"
            out_file.write_text(result.model_dump_json(indent=2))
            print(f"{file.name}: {result.title} ({result.seniority})")