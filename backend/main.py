import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from skills import extract_skills
from scoring import compare_skills
from recommendations import generate_recommendations
from llm import get_ai_feedback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
MIN_JD_LENGTH = 30
MAX_JD_LENGTH = 20000


async def read_pdf_text(file: UploadFile):
    """Validate the upload and return (text, page_count)."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed. Upload your resume as a PDF.",
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="This PDF is larger than 5 MB. Upload a smaller file.",
        )

    try:
        reader = PdfReader(io.BytesIO(contents))
        pages = len(reader.pages)
        text = "".join((page.extract_text() or "") + "\n" for page in reader.pages)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read this PDF. It may be corrupted or password protected.",
        )

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No text found in this PDF. It may be a scanned image. "
            "Upload a text-based PDF exported from Word or Google Docs.",
        )

    return text, pages


@app.get("/")
def home():
    return {"message": "Resume Analyzer API is running"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    text, pages = await read_pdf_text(file)
    return {
        "filename": file.filename,
        "pages": pages,
        "skills": extract_skills(text),
        "text": text,
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), job_description: str = Form(...)):
    job_description = job_description.strip()

    if len(job_description) < MIN_JD_LENGTH:
        raise HTTPException(
            status_code=400,
            detail="The job description is too short. Paste the full job posting.",
        )
    if len(job_description) > MAX_JD_LENGTH:
        raise HTTPException(
            status_code=400,
            detail="The job description is too long. Paste only the key sections.",
        )

    text, _ = await read_pdf_text(file)

    resume_skills = extract_skills(text)
    jd_skills = extract_skills(job_description)
    result = compare_skills(resume_skills, jd_skills)

    recs = generate_recommendations(
        result["matched_skills"], result["missing_skills"], result["score"]
    )

    ai_feedback = get_ai_feedback(
        text, job_description, result["matched_skills"], result["missing_skills"]
    )

    return {
        "filename": file.filename,
        "resume_skills": resume_skills,
        "job_skills": jd_skills,
        **result,
        **recs,
        "ai_feedback": ai_feedback,
    }