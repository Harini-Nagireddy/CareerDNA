#new career path file

def classify_skill_levels(skills, resume_text):

    levels = {}

    text = resume_text.lower()

    for skill in skills:

        count = text.count(skill.lower())

        if count >= 3:
            levels[skill] = "Advanced"

        elif count >= 1:
            levels[skill] = "Intermediate"

        else:
            levels[skill] = "Beginner"

    return levels