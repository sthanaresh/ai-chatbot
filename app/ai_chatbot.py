import httpx
from fastapi import FastAPI

app = FastAPI(title="My AI Chat API")


@app.post("/chat")
def chat(request: str):
    url = "http://localhost:11434/api/chat"
    messages = [{"role": "user", "content": request}]

    payload = {"model": "llama3.2:1b", "messages": messages, "stream": False}

    try:
        response = httpx.post(url, json=payload, timeout=120)
        response.raise_for_status()

    except httpx as e:
        raise (f"Error: {e}")

    data = response.json()
    return data["message"]
