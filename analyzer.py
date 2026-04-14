SKILLS_DB = [
    # Languages
    "python", "java", "c++",

    # Web
    "html", "css", "javascript", "react", "node.js",

    # AI/ML
    "machine learning", "deep learning", "nlp",
    "tensorflow", "pytorch",

    # DB
    "sql", "mongodb",

    # Tools
    "git", "docker", "kubernetes"
]

def extract_skills_from_text(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return set(found_skills)

def skill_gap_analysis(resume_text, jd_text):
    resume_skills = extract_skills_from_text(resume_text)
    jd_skills = extract_skills_from_text(jd_text)

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    return {
        "matched": list(matched),
        "missing": list(missing)
    }