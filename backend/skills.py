import re

# Canonical skill name -> ways it may be written in a resume
SKILLS = {
    # Languages
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript"],
    "TypeScript": ["typescript"],
    "C++": ["c++"],
    "C#": ["c#"],
    "PHP": ["php"],
    "Kotlin": ["kotlin"],
    # Frontend
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "React": ["react", "react.js", "reactjs"],
    "Next.js": ["next.js", "nextjs"],
    "Vue.js": ["vue", "vue.js", "vuejs"],
    "Angular": ["angular"],
    "Redux": ["redux"],
    "Tailwind CSS": ["tailwind css", "tailwind"],
    "Bootstrap": ["bootstrap"],
    # Backend
    "Node.js": ["node.js", "nodejs"],
    "Express.js": ["express.js", "expressjs"],
    "FastAPI": ["fastapi"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Spring Boot": ["spring boot", "springboot"],
    "REST APIs": ["rest api", "rest apis", "restful"],
    "GraphQL": ["graphql"],
    # Databases
    "SQL": ["sql", "mysql", "postgresql", "sqlite"],
    "MongoDB": ["mongodb"],
    "Firebase": ["firebase"],
    "Redis": ["redis"],
    # Cloud and DevOps
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "CI/CD": ["ci/cd", "cicd"],
    "Linux": ["linux"],
    # Tools
    "Git": ["git"],
    "GitHub": ["github"],
    "Postman": ["postman"],
    "Jira": ["jira"],
    "Figma": ["figma"],
    # AI / ML / Data
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "NLP": ["nlp", "natural language processing"],
    "LLM": ["llm", "llms"],
    "RAG": ["rag", "retrieval-augmented generation"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Matplotlib": ["matplotlib"],
    "OpenCV": ["opencv"],
    "Power BI": ["power bi"],
    "Data Visualization": ["data visualization"],
    # Concepts
    "OOP": ["oop", "object-oriented"],
    "Data Structures": ["data structures"],
    "Agile": ["agile", "scrum"],
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