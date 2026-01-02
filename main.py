from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import re

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")


# Load the knowledge base
with open("kb.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/search")
def search(q: str):
    q = q.lower().rstrip("s")
    results = []

    # build word-boundary regex: \bwork\b
    pattern = re.compile(rf"\b{re.escape(q)}s?\b")

    for item in kb:
        question = item.get("question", "").lower()
        answer = item.get("answer", "").lower()

        if pattern.search(question) or pattern.search(answer):
            results.append(item)

    return results


