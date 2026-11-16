def compare_skills(resume_skills: list[str], jd_skills: list[str]) -> dict:
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)

    if jd_set:
        score = round(len(matched) / len(jd_set) * 100)
    else:
        score = 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "score": score,
    }