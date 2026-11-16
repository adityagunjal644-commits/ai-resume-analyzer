import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from skills import extract_skills

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Resume Analyzer API is running"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    contents = await file.read()
    reader = PdfReader(io.BytesIO(contents))

    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from this PDF")

    skills = extract_skills(text)
    return {
        "filename": file.filename,
        "pages": len(reader.pages),
        "skills": skills,
        "text": text,
    }