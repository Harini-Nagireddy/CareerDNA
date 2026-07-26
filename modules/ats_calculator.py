"""
ATS Score Calculator — ResumeDNA v2
====================================
FORMULA (100 points total):

  A) Without Job Description (structure-based only):
     ┌─────────────────────────────────────────┬────────┐
     │ Component                               │ Points │
     ├─────────────────────────────────────────┼────────┤
     │ Skills count (≥8=30, ≥5=20, else=10)   │  30    │
     │ Sections present (edu+exp+proj+skills)  │  20    │
     │ Action verbs (≥5=15, ≥3=10, else=5)    │  15    │
     │ Common tech keywords hit               │  15    │
     │ Bullet points present                  │  10    │
     │ Measurable results (% numbers)         │   5    │
     │ Resume length (>300 words)             │   5    │
     └─────────────────────────────────────────┴────────┘

  B) With Job Description (JD keyword-weighted):
     score = 0.40 × jd_keyword_match_score
           + 0.35 × structure_score          (from above components)
           + 0.15 × action_verb_score
           + 0.10 × format_score
     Result mapped to 0–100.

  JD Keyword Match Score:
     matched_keywords / total_jd_keywords × 100
     (with synonym expansion: ml↔machine learning, etc.)
"""

import re
from collections import Counter

ACTION_VERBS = [
    "developed", "built", "implemented", "designed", "created", "improved",
    "optimized", "led", "managed", "engineered", "analyzed", "automated",
    "delivered", "achieved", "reduced", "increased", "generated", "deployed",
    "collaborated", "architected", "launched", "integrated", "migrated",
    "maintained", "trained", "evaluated"
]

TECH_KEYWORDS = [
    "python", "java", "sql", "machine learning", "data analysis",
    "pandas", "numpy", "nlp", "deep learning", "power bi",
    "excel", "tableau", "tensorflow", "scikit-learn", "javascript",
    "react", "flask", "django", "aws", "docker"
]

SYNONYMS = {
    "machine learning": ["ml"],
    "natural language processing": ["nlp"],
    "artificial intelligence": ["ai"],
    "react": ["react.js", "reactjs"],
    "node.js": ["nodejs", "node"],
    "javascript": ["js"],
    "kubernetes": ["k8s"],
    "continuous integration": ["ci", "ci/cd"],
}


def _normalize(text):
    return re.sub(r"[^a-zA-Z0-9 ]", " ", text.lower())


def _expand_keywords(keywords):
    expanded = set()
    for kw in keywords:
        kw = kw.lower().strip()
        if not kw:
            continue
        expanded.add(kw)
        if kw in SYNONYMS:
            expanded.update(SYNONYMS[kw])
        for key, vals in SYNONYMS.items():
            if kw in vals:
                expanded.add(key)
    return expanded


def _structure_score(skills, sections, resume_text):
    """Returns (score 0-65, feedback list)"""
    score = 0
    feedback = []
    text_lower = resume_text.lower()

    # Skills (30 pts)
    skill_count = len(skills)
    if skill_count >= 8:
        score += 30
    elif skill_count >= 5:
        score += 20
        feedback.append("Add more relevant technical skills (aim for 8+)")
    else:
        score += 10
        feedback.append("Too few skills detected — add technical skills")

    # Sections (20 pts)
    for sec, pts, msg in [
        ("education", 5, "Education section missing"),
        ("projects",  5, "Projects section missing — add personal/college projects"),
        ("experience",5, "Experience / Internships section missing"),
        ("skills",    5, "Skills section not clearly labelled"),
    ]:
        val = sections.get(sec, "")
        if isinstance(val, str) and val.strip():
            score += pts
        elif isinstance(val, list) and val:
            score += pts
        elif sec == "skills" and "skill" in text_lower:
            score += pts
        else:
            feedback.append(msg)

    # Action verbs (15 pts)
    verb_count = sum(len(re.findall(r"\b" + v + r"\b", text_lower)) for v in ACTION_VERBS)
    if verb_count >= 5:
        score += 15
    elif verb_count >= 3:
        score += 10
        feedback.append("Use more strong action verbs (developed, implemented, optimized…)")
    else:
        score += 5
        feedback.append("Add impact-driven action verbs to bullet points")

    # Bullet points (10 pts)
    bullets = resume_text.count("•") + resume_text.count("-") + resume_text.count("*")
    if bullets >= 5:
        score += 10
    else:
        score += 4
        feedback.append("Use bullet points for experience and projects")

    # Measurable results (5 pts)
    if re.search(r"\d+%", resume_text):
        score += 5
    else:
        feedback.append("Add measurable achievements e.g. 'improved accuracy by 20%'")

    # Length (5 pts)
    if len(resume_text.split()) > 300:
        score += 5
    else:
        feedback.append("Resume is too short — aim for 300+ words")

    return score, feedback


def calculate_ats_score(resume_text, sections, job_description="", filepath=None):
    """
    Returns (ats_score: int, feedback: list, matched_keywords: list, missing_keywords: list)
    """
    skills = [s for s in sections.get("skills", []) if s]
    # Fall back to empty list if skills section is a string
    if isinstance(skills, str):
        skills = []

    struct_score, feedback = _structure_score(skills, sections, resume_text)

    matched_kw = []
    missing_kw = []

    if job_description.strip():
        # ── JD-weighted mode ──────────────────────────────────────────────
        norm_resume = _normalize(resume_text)
        norm_jd     = _normalize(job_description)

        jd_words = set(norm_jd.split())
        # Remove stopwords (very short words)
        stopwords = {"a","an","the","and","or","in","of","to","for","with","on",
                     "at","by","from","is","are","was","were","be","been","has",
                     "have","had","will","would","can","could","should","this",
                     "that","it","as","we","you","they","their","our","your"}
        jd_words = {w for w in jd_words if len(w) > 2 and w not in stopwords}
        jd_words = _expand_keywords(jd_words)

        resume_words = Counter(norm_resume.split())

        for kw in sorted(jd_words):
            if kw in resume_words:
                matched_kw.append(kw)
            else:
                missing_kw.append(kw)

        if jd_words:
            jd_match_pct = len(matched_kw) / len(jd_words)   # 0.0 – 1.0
        else:
            jd_match_pct = 0.5

        # Action verb sub-score (0-1)
        text_lower = resume_text.lower()
        verb_count = sum(len(re.findall(r"\b" + v + r"\b", text_lower)) for v in ACTION_VERBS)
        verb_ratio = min(verb_count / 8, 1.0)

        # Format sub-score (0-1): bullet points + length
        bullet_ok  = 1 if (resume_text.count("•") + resume_text.count("-")) >= 5 else 0.5
        length_ok  = 1 if len(resume_text.split()) > 300 else 0.5
        fmt_score  = (bullet_ok + length_ok) / 2

        # Weighted total
        raw = (
            0.40 * jd_match_pct * 100 +
            0.35 * (struct_score / 65) * 100 +
            0.15 * verb_ratio * 100 +
            0.10 * fmt_score * 100
        )
        ats_score = round(min(raw, 100))

        if missing_kw:
            top_missing = missing_kw[:8]
            feedback.insert(0, f"JD keywords missing from resume: {', '.join(top_missing)}")

    else:
        # ── Structure-only mode ───────────────────────────────────────────
        ats_score = round(min(struct_score, 100))

    return ats_score, feedback, matched_kw, missing_kw
