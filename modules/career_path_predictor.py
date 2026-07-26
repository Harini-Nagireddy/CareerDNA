# 10 tech career paths with progression levels and required skills

ALL_CAREER_PATHS = {
    "Data Scientist": {
        "icon": "🔬",
        "description": "Analyze complex data, build ML models, and derive business insights.",
        "levels": ["Junior Data Scientist", "Data Scientist", "Senior Data Scientist", "Principal Data Scientist", "Chief Data Officer"],
        "core_skills": ["Python", "Statistics", "Machine Learning", "Pandas", "SQL", "Data Visualization"],
        "salary_range": "₹6L – ₹35L"
    },
    "Machine Learning Engineer": {
        "icon": "🤖",
        "description": "Design, deploy, and scale ML systems in production environments.",
        "levels": ["ML Intern", "Junior ML Engineer", "ML Engineer", "Senior ML Engineer", "ML Architect"],
        "core_skills": ["Python", "TensorFlow/PyTorch", "MLOps", "Docker", "Cloud (AWS/GCP)", "APIs"],
        "salary_range": "₹8L – ₹45L"
    },
    "Data Analyst": {
        "icon": "📊",
        "description": "Transform raw data into actionable business insights using SQL and BI tools.",
        "levels": ["Junior Analyst", "Data Analyst", "Senior Analyst", "Analytics Manager", "Director of Analytics"],
        "core_skills": ["SQL", "Excel", "Power BI / Tableau", "Python", "Data Storytelling"],
        "salary_range": "₹4L – ₹22L"
    },
    "Full Stack Developer": {
        "icon": "💻",
        "description": "Build end-to-end web applications — from UI to backend APIs and databases.",
        "levels": ["Junior Developer", "Full Stack Developer", "Senior Developer", "Tech Lead", "Engineering Manager"],
        "core_skills": ["HTML/CSS", "JavaScript", "React", "Node.js / Flask", "SQL", "Git"],
        "salary_range": "₹5L – ₹30L"
    },
    "DevOps Engineer": {
        "icon": "⚙️",
        "description": "Bridge development and operations — CI/CD, cloud infrastructure, and automation.",
        "levels": ["Junior DevOps", "DevOps Engineer", "Senior DevOps", "Site Reliability Engineer", "Platform Architect"],
        "core_skills": ["Linux", "Docker", "Kubernetes", "CI/CD", "Terraform", "AWS/Azure"],
        "salary_range": "₹6L – ₹35L"
    },
    "Cybersecurity Analyst": {
        "icon": "🔒",
        "description": "Protect systems from threats through monitoring, penetration testing, and incident response.",
        "levels": ["Security Intern", "Security Analyst", "Senior Analyst", "Security Engineer", "CISO"],
        "core_skills": ["Networking", "Linux", "SIEM Tools", "Python", "Penetration Testing", "Risk Management"],
        "salary_range": "₹5L – ₹28L"
    },
    "Cloud Architect": {
        "icon": "☁️",
        "description": "Design and oversee cloud infrastructure strategy for enterprise applications.",
        "levels": ["Cloud Support", "Cloud Engineer", "Cloud Architect", "Solutions Architect", "Principal Architect"],
        "core_skills": ["AWS/GCP/Azure", "Networking", "Terraform", "Security", "Cost Optimization", "Docker"],
        "salary_range": "₹8L – ₹50L"
    },
    "AI Research Scientist": {
        "icon": "🧠",
        "description": "Push the boundaries of AI with novel research in NLP, CV, and deep learning.",
        "levels": ["Research Intern", "Research Engineer", "Research Scientist", "Senior Researcher", "Research Director"],
        "core_skills": ["Python", "Deep Learning", "Math/Statistics", "NLP/CV", "Paper Writing", "PyTorch"],
        "salary_range": "₹10L – ₹70L"
    },
    "Product Manager (Tech)": {
        "icon": "🎯",
        "description": "Define product vision and drive execution across engineering and design teams.",
        "levels": ["Associate PM", "Product Manager", "Senior PM", "Group PM", "VP of Product"],
        "core_skills": ["Roadmapping", "Agile/Scrum", "SQL basics", "User Research", "Stakeholder Management"],
        "salary_range": "₹8L – ₹40L"
    },
    "UI/UX Designer": {
        "icon": "🎨",
        "description": "Create intuitive, beautiful user experiences that delight and convert.",
        "levels": ["Junior Designer", "UX Designer", "Senior Designer", "UX Lead", "Head of Design"],
        "core_skills": ["Figma", "User Research", "Wireframing", "Prototyping", "HTML/CSS basics", "Design Systems"],
        "salary_range": "₹4L – ₹25L"
    },
}


def predict_career_path(role):
    """Returns the progression levels for a given role."""
    if role in ALL_CAREER_PATHS:
        return ALL_CAREER_PATHS[role]["levels"]
    # Fuzzy match
    role_lower = role.lower()
    for key in ALL_CAREER_PATHS:
        if role_lower in key.lower() or key.lower() in role_lower:
            return ALL_CAREER_PATHS[key]["levels"]
    return ["Junior Engineer", "Software Engineer", "Senior Engineer", "Tech Lead", "Engineering Manager"]
