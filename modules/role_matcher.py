def match_roles(user_skills):
    roles = {
        "Data Scientist":          ["python", "machine learning", "pandas", "numpy", "nlp", "statistics", "scikit-learn"],
        "Data Analyst":            ["python", "sql", "excel", "power bi", "data analysis", "tableau"],
        "Machine Learning Engineer":["python", "tensorflow", "deep learning", "docker", "machine learning", "pytorch"],
        "Full Stack Developer":    ["html", "css", "javascript", "react", "flask", "node.js", "sql"],
        "DevOps Engineer":         ["linux", "docker", "kubernetes", "aws", "ci/cd", "terraform"],
        "Cloud Architect":         ["aws", "azure", "gcp", "terraform", "docker", "networking"],
        "Cybersecurity Analyst":   ["networking", "linux", "python", "penetration testing", "siem"],
        "AI Research Scientist":   ["python", "pytorch", "deep learning", "nlp", "statistics", "mathematics"],
        "Product Manager":         ["roadmapping", "agile", "sql", "user research", "stakeholder management"],
        "UI/UX Designer":          ["figma", "user research", "wireframing", "prototyping", "html", "css"],
    }

    results = {}
    user_skills_lower = [s.lower() for s in user_skills]

    for role, required in roles.items():
        matched = len(set(user_skills_lower) & set(required))
        score = int((matched / len(required)) * 100)
        results[role] = score

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
