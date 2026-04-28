from matcher import calculate_similarity
from analyzer import skill_gap_analysis
from parser.pdf_parser import extract_text_from_pdf
from parser.docx_parser import extract_text_from_docx

def process_resume(file_path, jd_text):
    # Extract text
    if file_path.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        resume_text = extract_text_from_docx(file_path)
    else:
        return None

    # Score
    score = calculate_similarity(resume_text, jd_text)

    # Skill analysis
    analysis = skill_gap_analysis(resume_text, jd_text)

    return {
        "filename": file_path.split("\\")[-1],
        "ats_score": round(score, 2),
        "matched_skills": analysis["matched"],
        "missing_skills": analysis["missing"]
    }

def rank_resumes(file_paths, jd_text):
    results = []

    for path in file_paths:
        data = process_resume(path, jd_text)
        if data:
            results.append(data)

    # Sort by score (descending)
    results.sort(key=lambda x: x["ats_score"], reverse=True)

    return results