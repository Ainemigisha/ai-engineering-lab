import asyncio
import os
import time

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
BASE_URL = os.environ["BASE_URL"]

#@dataclass
class Post(BaseModel):
    id: int
    title: str
    body: str


async def fetch_post(client: httpx.AsyncClient, post_id: int) -> Post:
    url = f"{BASE_URL}/posts/{post_id}"
    response = await client.get(url)
    response.raise_for_status()
    data = response.json()
    #return Post(id = data["id"], title=data["title"], body=data["body"])
    return Post.model_validate(data)


async def main() -> None:
    start = time.perf_counter()
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [fetch_post(client, i) for i in range(1,11)]
        posts = await asyncio.gather(*tasks)

    for post in posts:
        print(post.id, post.title)
        

    print(f"Done in {time.perf_counter() -  start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())