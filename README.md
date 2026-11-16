# ai-engineering-lab

Python and Typescript day1 ai engineering conepts.

- **day1/**: Python. Async httpx post fetcher, Pydantic models with a FastAPI `/posts` endpoint, and a first Gemini call with a system prompt and token usage. Run with `cd day1 && uv run fastapi dev app.py` or `uv run python llm_call.py` (needs `BASE_URL` and `GEMINI_API_KEY`).
- **day1-ts/**: TypeScript port. Zod-validated parallel fetches with `Promise.all`, plus the same Gemini call. Run with `cd day1-ts && npm install && npx tsx fetchPosts.ts` or `npx tsx llmCall.ts` (same env vars, but it doesn't read `.env`, so export them in your shell first).
