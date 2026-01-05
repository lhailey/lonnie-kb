from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import re

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.mount("/images", StaticFiles(directory="images"), name="images")

# Load the knowledge base
with open("kb.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

WHITELIST = {"ha", "mv", "db", "ip", "rf", "sql", "ale", "vm", "kb", "rma"}
STOPWORDS = {"and", "or", "the", "to", "of", "in", "on", "at", "for", "with"}

@app.get("/search")
def search(q: str):
    q = q.lower().strip()
    
    # replace this  
    # if q.isdigit(): return []
    # if not q or len(q) < 3:
    #    return []

    # replace above with this
    if q.isdigit(): 
        return []

    # replace this with below
    # if not q or (len(q) < 3 and q not in WHITELIST):
    # return []

    # replace code allows whitelist and ignores stopwords
    if not q or q in STOPWORDS or (len(q) < 3 and q not in WHITELIST):
        return []

    
    q = q.rstrip("s")
    results = []
    
    # build word-boundary regex: \bwork\b
    pattern = re.compile(rf"\b{re.escape(q)}s?\b")

    for item in kb:
        question = item.get("question", "").lower()
        answer = item.get("answer", "").lower()

        if pattern.search(question) or pattern.search(answer):
            # change to this to remove cluttered results
            # if pattern.search(question):
            results.append(item)

    return results





