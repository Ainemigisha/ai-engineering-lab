from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

SYSTEM_PROMPT = ("You are a URA tax officer helping a small-business owner in Kampala who has no tax background. "
        "Answer in short, plain language and avoid jargon. Do not state fees, penalties or deadlines unless you are certain of them. " 
        "End by advising the person to confirm the details with URA.");
TEMP = 1.5

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="What is TIN registration and do I need it for my shop?",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=TEMP
    )
)

print(response.text)
usage = response.usage_metadata
print(f"prompt tokens:   {usage.prompt_token_count}")
print(f"output tokens:   {usage.candidates_token_count}")
print(f"thinking tokens: {usage.thoughts_token_count}")
print(f"total tokens:    {usage.total_token_count}")
