import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader

app = FastAPI(title="Upload PDF, Ask Question, Get Answer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ask-pdf")
def ask_pdf(fileUpload: UploadFile = File(...), question: str = Form(...)):
    url = "http://localhost:11434/api/chat"
    pdf_text = textExtractor(fileUpload)
    contents = (
        f"Answer the questions using the pdf content below"
        f"Question: {question}, PDF Content:{pdf_text}"
    )

    messages = [{"role": "user", "content": contents}]

    payload = {"model": "llama3.2:1b", "messages": messages, "stream": False}
    try:
        response = httpx.post(url, json=payload, timeout=120)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

    response.raise_for_status()

    data = response.json()
    print(f"Result: {data ["message"]}")
    return data["message"]["content"]


def textExtractor(fileUpload) -> str:
    reader = PdfReader(fileUpload.file)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        full_text += text
    return full_text
