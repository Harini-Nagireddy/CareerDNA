import json

def load_courses():
    with open("data/courses.json", "r", encoding="utf-8") as file:
        return json.load(file)

def recommend_courses(missing_skills):

    course_data = load_courses()
    recommendations = {}

    for skill in missing_skills:
        if skill in course_data:
            recommendations[skill] = course_data[skill]

    return recommendations