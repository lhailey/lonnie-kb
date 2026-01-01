import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import re
import os

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

# Load the knowledge base
with open("kb.json", "r", encoding="utf-8") as f:
    kb = json.load(f)



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    password = request.query_params.get("password")
    expected = os.environ.get("KB_PASSWORD")

    if password != expected:
        return HTMLResponse(
            """
            <html>
              <head><title>Internal Access</title></head>
              <body style="font-family: Arial; text-align:center; margin-top:80px;">
                <h2>RTLS Operations Knowledge Base</h2>
                <p>Internal access only</p>
                <form method="get">
                  <input type="password" name="password" placeholder="Enter password">
                  <br><br>
                  <button type="submit">Enter</button>
                </form>
              </body>
            </html>
            """,
            status_code=401
        )

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



