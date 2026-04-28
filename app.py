from fastapi import FastAPI, UploadFile, File
import shutil
import os

from ranker import rank_resumes
from fastapi import UploadFile, File, Form
from typing import List

from fastapi import Request

from matcher import calculate_similarity
from fastapi import Form
from analyzer import skill_gap_analysis
from parser.pdf_parser import extract_text_from_pdf
from parser.docx_parser import extract_text_from_docx
from parser.extractor import extract_email, extract_name, extract_skills

app = FastAPI()

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "AI Resume Screening API Running 🚀"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file format"}

    # Extract data
    data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text)
    }

    return data

@app.post("/match")
async def match_resume_jd(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # Extract text
    if resume.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    elif resume.filename.endswith(".docx"):
        resume_text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file format"}

    score = calculate_similarity(resume_text, job_description)

    analysis = skill_gap_analysis(resume_text, job_description)

    return {
       "ats_score": round(score, 2),
       "matched_skills": analysis["matched"],
       "missing_skills": analysis["missing"]
    }
    
@app.post("/rank")
async def rank_candidates(
    resumes: list[UploadFile] = File(...),   # 👈 CHANGE HERE
    job_description: str = Form(...)
):
    file_paths = []

    for file in resumes:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_paths.append(file_path)

    ranked_results = rank_resumes(file_paths, job_description)

    return {
        "ranked_candidates": ranked_results
    }