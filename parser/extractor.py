import re
import spacy

nlp = spacy.load("en_core_web_sm")

# Extract email
def extract_email(text):
    match = re.findall(r'\S+@\S+', text)
    return match[0] if match else None

# Extract name
def extract_name(text):
    doc = nlp(text[:1000])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

# Simple skills list (you can expand later)
SKILLS_DB = ["Python", "Java", "C++", "Machine Learning", "SQL", "React", "Node.js"]

def extract_skills(text):
    skills_found = []
    for skill in SKILLS_DB:
        if skill.lower() in text.lower():
            skills_found.append(skill)
    return skills_found