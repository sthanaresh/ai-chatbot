import httpx
from fastapi import FastAPI
from pypdf import PdfReader

app = FastAPI(title="PDF Question Answer App")


def textExtractor() -> str:
    reader = PdfReader("Research.pdf")
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        full_text += text
    return full_text


@app.post("/pdf")
def pdf_answer():
    url = "http://localhost:11434/api/chat"
    Ques = "Summarize the PDF"

    pdf_text = textExtractor()
    contents = f"Answer the following question using the PDF content.Question: {Ques}, PDF Content:{pdf_text}"

    messages = [{"role": "user", "content": contents}]

    payload = {"model": "llama3.2:1b", "messages": messages, "stream": False}

    try:
        response = httpx.post(url, json=payload, timeout=12)
        response.raise_for_status()

    except httpx as e:
        raise (f"Error: {e}")

    data = response.json()
    return data["message"]
