"""
Resume Optimizer — ResumeDNA
=============================
Analyses why a resume scored low and returns:

  1. A list of improvement tips — each with:
       - category      : what area this covers
       - tip           : the specific thing to add / change
       - example       : a concrete copy-paste-ready example
       - points_gain   : exact points this fix will add to the score

  2. projected_score   : current_score + sum(points_gain) capped at 100

Logic is directly tied to the ATS scoring formula in ats_calculator.py
so every point gain is honest and calculable.
"""

import re

ACTION_VERBS = [
    "developed", "built", "implemented", "designed", "created", "improved",
    "optimized", "led", "managed", "engineered", "analyzed", "automated",
    "delivered", "achieved", "reduced", "increased", "generated", "deployed",
    "collaborated", "launched", "integrated", "maintained", "evaluated"
]


def generate_optimization_tips(resume_text, sections, skills_found,
                                missing_keywords, ats_score, job_description=""):
    """
    Returns (tips_list, projected_score).

    tips_list : list of dicts, each:
        {
          "category"    : str,
          "tip"         : str,
          "example"     : str,
          "points_gain" : int,
          "priority"    : "High" | "Medium" | "Low"
        }

    projected_score : int  (capped at 100)
    """
    tips        = []
    total_gain  = 0
    text_lower  = resume_text.lower()

    # ── 1. MISSING JD KEYWORDS (weight = 40% of score) ───────────────────
    # Each keyword fix improves the JD match ratio → raises that 40% bucket.
    # We cap keyword tips at the top 6 most impactful ones.
    if job_description and missing_keywords:
        top_kw = missing_keywords[:6]
        # Points gain: adding these keywords improves jd_match_pct
        # Estimate: each keyword recovered is worth ~(40 / total_jd_kw) points.
        # We approximate conservatively as 3 pts per keyword, max 15.
        kw_gain = min(len(top_kw) * 3, 15)
        tips.append({
            "category"   : "JD Keyword Match",
            "tip"        : f"Add these {len(top_kw)} missing keywords from the Job Description into your resume",
            "example"    : "Add them naturally in your Skills section or weave into bullet points:\n"
                           + ", ".join(top_kw),
            "points_gain": kw_gain,
            "priority"   : "High"
        })
        total_gain += kw_gain

    # ── 2. SKILLS COUNT ───────────────────────────────────────────────────
    skill_count = len(skills_found)
    if skill_count < 8:
        if skill_count < 5:
            pts = 20   # jumps from 10 → 30
        else:
            pts = 10   # jumps from 20 → 30
        tips.append({
            "category"   : "Skills Section",
            "tip"        : f"You have {skill_count} skills detected. Add more until you reach 8+ technical skills",
            "example"    : "Add a clearly labelled 'Technical Skills' section:\n\n"
                           "Technical Skills:\n"
                           "Python, SQL, Machine Learning, Pandas, NumPy, Scikit-learn, Flask, Git",
            "points_gain": pts,
            "priority"   : "High"
        })
        total_gain += pts

    # ── 3. MISSING SECTIONS ───────────────────────────────────────────────
    for sec, label, pts, ex in [
        ("education", "Education", 5,
         "Education:\nB.Tech in Computer Science — XYZ University (2022–2026)  CGPA: 8.5"),
        ("projects",  "Projects",  5,
         "Projects:\n• Resume Analyzer — Built a Flask web app that parses resumes and calculates ATS scores using Python and NLP.\n• Sales Dashboard — Created a Power BI dashboard to visualize monthly sales trends for 5 product lines."),
        ("experience","Experience",5,
         "Experience:\nData Science Intern — ABC Corp (Jun 2024 – Aug 2024)\n• Developed ETL pipelines using Pandas that reduced data processing time by 30%\n• Analyzed customer churn using Scikit-learn with 87% model accuracy"),
    ]:
        val = sections.get(sec, "")
        has_section = (isinstance(val, str) and val.strip()) or \
                      (isinstance(val, list) and len(val) > 0)
        if not has_section:
            tips.append({
                "category"   : f"Missing Section — {label}",
                "tip"        : f"Add a '{label}' section to your resume",
                "example"    : ex,
                "points_gain": pts,
                "priority"   : "High"
            })
            total_gain += pts

    # ── 4. ACTION VERBS ───────────────────────────────────────────────────
    verb_count = sum(
        len(re.findall(r"\b" + v + r"\b", text_lower)) for v in ACTION_VERBS
    )
    if verb_count < 5:
        if verb_count < 3:
            pts = 10   # jumps from 5 → 15
        else:
            pts = 5    # jumps from 10 → 15
        tips.append({
            "category"   : "Action Verbs",
            "tip"        : f"Only {verb_count} action verbs found. Use at least 5 strong action verbs in your bullet points",
            "example"    : "Replace weak phrases with action verbs:\n\n"
                           "❌  'Responsible for data analysis'\n"
                           "✅  'Analyzed 50,000+ rows of customer data using Pandas to identify purchase trends'\n\n"
                           "❌  'Worked on a machine learning project'\n"
                           "✅  'Built and deployed an ML model achieving 91% accuracy using Scikit-learn'\n\n"
                           "Strong verbs to use: Developed, Built, Implemented, Designed, Optimized, "
                           "Automated, Delivered, Engineered, Launched, Reduced",
            "points_gain": pts,
            "priority"   : "High"
        })
        total_gain += pts

    # ── 5. BULLET POINTS ─────────────────────────────────────────────────
    bullets = resume_text.count("•") + resume_text.count("-") + resume_text.count("*")
    if bullets < 5:
        pts = 6   # jumps from 4 → 10
        tips.append({
            "category"   : "Bullet Points & Formatting",
            "tip"        : f"Only {bullets} bullet points found. Use bullet points in Experience and Projects (need 5+)",
            "example"    : "Format experience entries as bullet points:\n\n"
                           "Data Science Intern — ABC Corp\n"
                           "• Developed a customer segmentation model using K-Means clustering\n"
                           "• Built automated reports using Python saving 3 hours per week\n"
                           "• Optimized SQL queries reducing dashboard load time by 40%",
            "points_gain": pts,
            "priority"   : "Medium"
        })
        total_gain += pts

    # ── 6. MEASURABLE RESULTS ─────────────────────────────────────────────
    if not re.search(r"\d+%", resume_text):
        pts = 5
        tips.append({
            "category"   : "Measurable Achievements",
            "tip"        : "No percentage achievements found. Add quantified results with numbers and percentages",
            "example"    : "Turn vague statements into measurable achievements:\n\n"
                           "❌  'Improved model performance'\n"
                           "✅  'Improved model accuracy by 18% through hyperparameter tuning'\n\n"
                           "❌  'Reduced processing time'\n"
                           "✅  'Reduced data processing time by 35% by optimising Pandas pipelines'\n\n"
                           "❌  'Built a web app'\n"
                           "✅  'Built a Flask REST API serving 200+ daily requests with 99% uptime'",
            "points_gain": pts,
            "priority"   : "Medium"
        })
        total_gain += pts

    # ── 7. RESUME LENGTH ─────────────────────────────────────────────────
    word_count = len(resume_text.split())
    if word_count <= 300:
        pts = 5
        tips.append({
            "category"   : "Resume Length",
            "tip"        : f"Resume is too short ({word_count} words). Expand it to at least 300 words",
            "example"    : "Expand your resume by:\n"
                           "• Writing 2–3 bullet points per project (what you built, how, result)\n"
                           "• Adding a 2–3 line summary/objective at the top\n"
                           "• Listing relevant coursework, certifications or achievements\n"
                           "• Describing internship or college project work in detail",
            "points_gain": pts,
            "priority"   : "Low"
        })
        total_gain += pts

    # ── 8. CONTACT INFORMATION ───────────────────────────────────────────
    has_email = bool(re.search(r"\S+@\S+\.\S+", resume_text))
    has_phone = bool(re.search(r"[\+]?[\d\s\-]{10,}", resume_text))
    if not has_email or not has_phone:
        pts = 3
        missing_contact = []
        if not has_email:
            missing_contact.append("email address")
        if not has_phone:
            missing_contact.append("phone number")
        tips.append({
            "category"   : "Contact Information",
            "tip"        : f"Missing contact info: {' and '.join(missing_contact)}",
            "example"    : "Add at the top of your resume:\n\n"
                           "John Doe\njohn.doe@gmail.com  |  +91 98765 43210  |  linkedin.com/in/johndoe  |  github.com/johndoe",
            "points_gain": pts,
            "priority"   : "Low"
        })
        total_gain += pts

    # ── Projected Score ───────────────────────────────────────────────────
    projected = min(ats_score + total_gain, 100)

    return tips, projected
