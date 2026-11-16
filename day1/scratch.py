from fetch_posts import Post
from pydantic import ValidationError

post = Post.model_validate({"id": "5", "title": "x", "body": "y"})

print(post)
print(type(post.id))

try:
    Post.model_validate({"id": "abc", "title": "x", "body": "y"})
except ValidationError as e:
    print(e)

try:
    Post.model_validate({"id": "1", "title": "x"})
except ValidationError as e:
    print(e)