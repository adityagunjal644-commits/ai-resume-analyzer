import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from skills import extract_skills
from scoring import compare_skills
from recommendation import generate_recommendations
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

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), job_description: str = Form(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    contents = await file.read()
    reader = PdfReader(io.BytesIO(contents))

    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from this PDF")

    resume_skills = extract_skills(text)
    jd_skills = extract_skills(job_description)
    result = compare_skills(resume_skills, jd_skills)

    recs = generate_recommendations(
        result["matched_skills"], result["missing_skills"], result["score"]
    )

    return {
        "filename": file.filename,
        "resume_skills": resume_skills,
        "job_skills": jd_skills,
        **result,
        **recs,
    }