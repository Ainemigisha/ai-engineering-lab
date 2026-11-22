# ai-engineering-lab

A hands-on lab where I am learning to build reliable LLM applications, in Python and TypeScript. Each folder is one step, built and tested before moving on.

## Highlights

### Structured job-posting analyser (`day2/`)
Takes a raw job posting and returns structured JSON (title, seniority, required and nice-to-have skills, location eligibility) using Gemini.

- **Schema-first output:** the response shape is defined once as a Pydantic model and passed to the model as a JSON schema.
- **Validation:** custom validators reject answers that break the rules (for example, skill names longer than four words).
- **Self-correcting retries:** when validation fails, the error and the previous answer are sent back so the model can fix its own output.
- **Prompt iteration:** three versions of the system prompt are kept in `prompts/` so changes can be compared, with results for five real postings saved in `results/`.

Run it:

    cd day2
    uv run python analyse_json.py                    # analyse all postings in postings/
    uv run python analyse_json.py postings/job1.txt  # analyse one posting

### Foundations (`day1/`, `day1-ts/`)
- **Python:** async HTTP calls with httpx, Pydantic models, a small FastAPI endpoint, and a first Gemini call with a system prompt and token usage reporting.
- **TypeScript:** the same work ported with Zod validation and parallel requests using `Promise.all`.

## Setup
Create a `.env` file (never committed) with:

    GEMINI_API_KEY=your-key
    BASE_URL=https://jsonplaceholder.typicode.com   # any API that serves /posts/{id}

The TypeScript scripts do not read `.env`, so export the variables in your shell first.

## Next steps
- Score analyser output against a small hand-labelled set, so prompt changes can be measured instead of judged by eye.
- Record the model name and prompt version with every result.
- Test the analyser against prompt-injection attempts hidden inside job postings.
