import os
import json
import re
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

# Load the knowledge base
with open("kb.json", "r", encoding="utf-8") as f:
    kb = json.load(f)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    auth = request.cookies.get("kb_auth")
    expected = os.environ.get("KB_PASSWORD", "")

    if auth != expected:
        return HTMLResponse(
            """
            <html>
              <head><title>Internal Access</title></head>
              <body style="font-family: Arial; text-align:center; margin-top:80px;">
                <h2>RTLS Operations Knowledge Base</h2>
                <p>Internal access only</p>
                <form method="post" action="/login">
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
def search(request: Request, q: str):
    auth = request.cookies.get("kb_auth")
    expected = os.environ.get("KB_PASSWORD", "")

    if auth != expected:
        return []

    q = q.lower().rstrip("s")
    results = []

    pattern = re.compile(rf"\b{re.escape(q)}s?\b")

    for item in kb:
        question = item.get("question", "").lower()
        answer = item.get("answer", "").lower()

        if pattern.search(question) or pattern.search(answer):
            results.append(item)

    return results


@app.post("/login")
async def login(request: Request):
    form = await request.form()
    password = form.get("password", "")
    expected = os.environ.get("KB_PASSWORD", "")

    print("DEBUG password entered:", repr(password))
    print("DEBUG expected password:", repr(expected))

    if password.strip().lower() != expected.strip().lower():
        return HTMLResponse("<h3>Invalid password</h3>", status_code=401)

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="kb_auth",
        value=expected.strip().lower(),
        httponly=True,
        secure=True,
        samesite="lax"
    )
    return response








