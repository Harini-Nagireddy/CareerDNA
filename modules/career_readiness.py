#new career path file

def calculate_career_readiness(skills, projects, experience):

    score = 0

    if len(skills) >= 6:
        score += 40

    if projects.strip():
        score += 30

    if experience.strip():
        score += 30

    return score