import re

def extract_sections(text):

    sections = {
        "skills": "",
        "education": "",
        "projects": "",
        "experience": ""
    }

    text = text.lower()

    skills_pattern = r"(skills|technical skills)(.*?)(education|projects|experience|$)"
    education_pattern = r"(education)(.*?)(skills|projects|experience|$)"
    projects_pattern = r"(projects)(.*?)(skills|education|experience|$)"
    experience_pattern = r"(experience)(.*?)(skills|education|projects|$)"

    skills = re.search(skills_pattern, text, re.DOTALL)
    education = re.search(education_pattern, text, re.DOTALL)
    projects = re.search(projects_pattern, text, re.DOTALL)
    experience = re.search(experience_pattern, text, re.DOTALL)

    if skills:
        sections["skills"] = skills.group(2)

    if education:
        sections["education"] = education.group(2)

    if projects:
        sections["projects"] = projects.group(2)

    if experience:
        sections["experience"] = experience.group(2)

    return sections