#new career path file

def generate_career_dna(skills):

    profile = {}

    if "machine learning" in skills or "python" in skills:
        profile["type"] = "AI/Data Innovator"

    elif "javascript" in skills or "react" in skills:
        profile["type"] = "Web Technology Builder"

    else:
        profile["type"] = "Technology Explorer"

    profile["strengths"] = skills[:5]

    profile["growth_areas"] = [
        "Cloud Computing",
        "System Design",
        "Industry Projects"
    ]

    return profile