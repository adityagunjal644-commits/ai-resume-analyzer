# Skill-specific advice for common missing skills
TIPS = {
    "Docker": "Learn Docker basics and containerize one of your projects (e.g., your FastAPI backend).",
    "SQL": "Practice SQL queries and add a small project using MySQL or PostgreSQL.",
    "AWS": "Try AWS free tier: deploy a small app on EC2 or S3.",
    "Machine Learning": "Complete a beginner ML course and build one small ML project.",
    "Java": "Build a small Java project to show OOP skills.",
}


def generate_recommendations(matched: list[str], missing: list[str], score: int) -> dict:
    strengths = []
    suggestions = []

    if matched:
        strengths.append(f"Your resume already covers {len(matched)} required skills: {', '.join(matched)}.")

    if score >= 80:
        strengths.append("Strong match for this job.")
    elif score >= 50:
        suggestions.append("Decent match. Closing the skill gaps below can raise your score.")
    else:
        suggestions.append("Low match. Consider building projects with the missing skills before applying.")

    for skill in missing:
        tip = TIPS.get(
            skill,
            f"Learn {skill} and add a project or experience line that uses it.",
        )
        suggestions.append(tip)

    if missing:
        suggestions.append(
            "Only add a skill to your resume if you have actually used it. Mention it in a project or experience bullet."
        )

    return {"strengths": strengths, "suggestions": suggestions}