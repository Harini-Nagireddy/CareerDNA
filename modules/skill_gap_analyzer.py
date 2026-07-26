import json

def load_job_roles():
    with open("data/job_roles.json", "r") as file:
        return json.load(file)


def analyze_skill_gap(user_skills, selected_role):

    roles = load_job_roles()

    required_skills = roles.get(selected_role, [])

    missing_skills = []

    for skill in required_skills:
        if skill not in user_skills:
            missing_skills.append(skill)

    return required_skills, missing_skills