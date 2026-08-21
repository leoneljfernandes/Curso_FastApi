from fastapi import FastAPI, Request
# pyrefly: ignore [missing-import]
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="./templates")

posts: list[dict] = [
    {
        "id": 1,
        "title": "Post 1",
        "content": "Content 1",
        "author": "Author 1",
        "date_posted": "2026-08-19T21:30:14-03:00",
    },
    {
        "id": 2,
        "title": "Post 2",
        "content": "Content 2",
        "author": "Author 2",
        "date_posted": "2026-08-19T21:30:14-03:00",
    },
    {
        "id": 3,
        "title": "Post 3",
        "content": "Content 3",
        "author": "Author 3",
        "date_posted": "2026-08-19T21:30:14-03:00",
    },
]

@app.get("/",include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})

@app.get("/api/posts")
def get_posts():
    return posts