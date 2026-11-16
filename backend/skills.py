import re

# Canonical skill name -> ways it may be written in a resume
SKILLS = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript"],
    "C++": ["c++"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node.js", "nodejs"],
    "Express.js": ["express.js", "expressjs"],
    "FastAPI": ["fastapi"],
    "Tailwind CSS": ["tailwind css", "tailwind"],
    "MongoDB": ["mongodb"],
    "SQL": ["sql", "mysql", "postgresql"],
    "REST APIs": ["rest api", "rest apis", "restful"],
    "Git": ["git"],
    "GitHub": ["github"],
    "NLP": ["nlp", "natural language processing"],
    "LLM": ["llm", "llms"],
    "RAG": ["rag", "retrieval-augmented generation"],
    "Machine Learning": ["machine learning", "ml"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Matplotlib": ["matplotlib"],
    "OpenCV": ["opencv"],
    "Power BI": ["power bi"],
    "Docker": ["docker"],
}


def extract_skills(text: str) -> list[str]:
    found = []
    text_lower = text.lower()
    for skill, aliases in SKILLS.items():
        for alias in aliases:
            # match the alias only as a whole word/phrase
            pattern = r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])"
            if re.search(pattern, text_lower):
                found.append(skill)
                break
    return found