def extract_keywords(text):
    return set(text.lower().split())

def skill_gap_analysis(resume_text, jd_text):
    resume_words = extract_keywords(resume_text)
    jd_words = extract_keywords(jd_text)

    missing_skills = jd_words - resume_words
    matched_skills = jd_words & resume_words

    return {
        "matched": list(matched_skills)[:10],
        "missing": list(missing_skills)[:10]
    }