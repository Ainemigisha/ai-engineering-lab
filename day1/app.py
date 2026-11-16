import asyncio

import httpx
from fastapi import FastAPI
from fetch_posts import Post, fetch_post
from pydantic import BaseModel

app = FastAPI()

class PostRequest(BaseModel):
    post_ids: list[int]


@app.post("/posts")
async def get_posts(request: PostRequest) -> list[Post]:
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [fetch_post(client, i) for i in request.post_ids]
        posts = await asyncio.gather(*tasks)

        return posts
