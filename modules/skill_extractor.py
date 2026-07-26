def load_skills():

    with open("data/skills.txt", "r") as file:
        skills = file.read().splitlines()

    return [skill.lower() for skill in skills]


def extract_skills(text):

    skills_list = load_skills()
    text = text.lower()

    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills