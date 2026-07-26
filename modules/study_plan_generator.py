def generate_study_plan(missing_skills):

    study_plan = []

    week = 1

    for skill in missing_skills:

        plan = {
            "week": f"Week {week}",
            "task": f"Learn {skill}"
        }

        study_plan.append(plan)
        week += 1

    # Final revision / project week
    study_plan.append({
        "week": f"Week {week}",
        "task": "Build a mini project using learned skills"
    })

    return study_plan