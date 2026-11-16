import { z } from "zod";

const BASE_URL = process.env.BASE_URL;

const Post = z.object({
    id : z.number(),
    title: z.string(),
    body: z.string()
});

type Post = z.infer<typeof Post>;

async function fetchPost(postId: number): Promise<Post> {
    const url = `${BASE_URL}/posts/${postId}`;

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error('Post ${postId} failed with status ${response.status}');
    }
    const data = await response.json();
    return Post.parse(data);
}

async function main(): Promise<void> {
    const start = performance.now();

    const ids = Array.from({length:10}, (_,i) => i+1);

    const tasks = ids.map((id) => (fetchPost(id)));

    const posts = await Promise.all(tasks);

    for (const post of posts){
        console.log(`Post id ${post.id} with title ${post.title}`);
    }

    console.log(`Done in ${((performance.now() - start)/1000).toFixed(2)}s`)
}

main();


