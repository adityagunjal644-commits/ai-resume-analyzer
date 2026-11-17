import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000),  # 30 seconds
)
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


def get_ai_feedback(resume_text, job_description, matched, missing):
    prompt = f"""You are an expert resume reviewer and career coach.

Compare the resume with the job description and give honest, specific feedback.

Rules:
- Plain text only. No markdown symbols like ** or #.
- Use exactly these 3 headings: Summary, Resume Improvements, Next Steps.
- Under each heading write 2 to 4 short lines starting with "- ".
- Never suggest adding skills or experience the candidate does not have.
- Be specific to this resume, not generic.

Skills already matched: {', '.join(matched) or 'none'}
Skills missing: {', '.join(missing) or 'none'}

JOB DESCRIPTION:
{job_description[:3000]}

RESUME:
{resume_text[:6000]}
"""
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return response.text
    except Exception as e:
        print("AI feedback failed:", e)
        return None