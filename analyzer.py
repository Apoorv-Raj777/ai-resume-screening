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

def normalize_text(text):
    """
    Normalize text for better matching:
    - Lowercase
    - Remove dots (node.js → nodejs)
    """
    return text.lower().replace(".", "")

def extract_skills_from_text(text):
    normalized_text = normalize_text(text)
    found_skills = []

    for skill in SKILLS_DB:
        normalized_skill = normalize_text(skill)

        if normalized_skill in normalized_text:
            found_skills.append(skill)  # keep original skill name

    return set(found_skills)

def skill_gap_analysis(resume_text, jd_text):
    resume_skills = extract_skills_from_text(resume_text)
    jd_skills = extract_skills_from_text(jd_text)

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    return {
        "matched": sorted(list(matched)),
        "missing": sorted(list(missing))
    }