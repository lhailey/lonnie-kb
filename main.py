from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import re

app = FastAPI()

INDEX_KEYWORDS = {"all", "index", "list"}

@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}

app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/docs", StaticFiles(directory="docs"), name="docs")

# Load the knowledge base
with open("kb.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

WHITELIST = {"ha", "mv", "db", "ip", "rf", "sql", "ale", "vm", "kb", "rma", "hm", "dm", "t15"}
STOPWORDS = {"and", "or", "the", "to", "of", "in", "on", "at", "for", "with", "us", "use"}

@app.get("/search")
def search(q: str):
    q = q.lower().strip()
    
    # replace above with this
    if q.isdigit(): 
        return []

    # Return question-only index
    if q in INDEX_KEYWORDS:
        return [{"question": item["question"], "answer": ""} for item in kb]
    
    if not q or q in STOPWORDS or (len(q) < 3 and q not in WHITELIST):
        return []
    
    q = q.rstrip("s")
    results = []
    
    if q == "t15":
        pattern = re.compile(rf"\b{re.escape(q)}\w*\b", re.IGNORECASE)
    elif q == "ha":
        pattern = re.compile(rf"\b{re.escape(q)}\b", re.IGNORECASE)
    else:
        pattern = re.compile(rf"\b{re.escape(q)}s?\b", re.IGNORECASE)

    for item in kb:
        question = item.get("question", "").lower()
        answer = item.get("answer", "").lower()  # still needed for highlighting

        if pattern.search(question):
            results.append(item)

    return results


INDEX_KEYWORDS = {"all", "index", "list"}

@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}

app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/docs", StaticFiles(directory="docs"), name="docs")

# Load the knowledge base
with open("kb.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

WHITELIST = {"ha", "mv", "db", "ip", "rf", "sql", "ale", "vm", "kb", "rma", "hm", "dm", "t15"}
STOPWORDS = {"and", "or", "the", "to", "of", "in", "on", "at", "for", "with", "us", "use"}

@app.get("/search")
def search(q: str):
    q = q.lower().strip()
    
    # replace above with this
    if q.isdigit(): 
        return []

    # Return question-only index
    if q in INDEX_KEYWORDS:
        return [{"question": item["question"], "answer": ""} for item in kb]
    
    if not q or q in STOPWORDS or (len(q) < 3 and q not in WHITELIST):
        return []
    
    q = q.rstrip("s")
    results = []
    
    if q == "t15":
        pattern = re.compile(rf"\b{re.escape(q)}\w*\b", re.IGNORECASE)
    elif q == "ha":
        pattern = re.compile(rf"\b{re.escape(q)}\b", re.IGNORECASE)
    else:
        pattern = re.compile(rf"\b{re.escape(q)}s?\b", re.IGNORECASE)

    for item in kb:
        question = item.get("question", "").lower()
        answer = item.get("answer", "").lower()  # still needed for highlighting

        if pattern.search(question):
            results.append(item)

    return results


