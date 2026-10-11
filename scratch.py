import httpx

payload = {
    "model": "llama3.2:3b",  # use the model you actually pulled
    "messages": [{"role": "user", "content": "Say hello in 5 words."}],
    "stream": False,
}

response = httpx.post("http://localhost:11434/api/chat", json=payload, timeout=120)
data = response.json()
print(data.keys())
print(data["message"])
