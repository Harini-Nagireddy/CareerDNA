from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
import os, json, uuid, time

from modules.resume_parser import extract_text
from modules.section_extractor import extract_sections
from modules.skill_extractor import extract_skills
from modules.ats_calculator import calculate_ats_score
from modules.skill_gap_analyzer import analyze_skill_gap
from modules.course_recommender import recommend_courses
from modules.study_plan_generator import generate_study_plan
from modules.role_matcher import match_roles
from modules.career_path_predictor import predict_career_path, ALL_CAREER_PATHS
from modules.skill_level_classifier import classify_skill_levels
from modules.career_dna_analyzer import generate_career_dna
from modules.career_readiness import calculate_career_readiness
from modules.resume_optimizer import generate_optimization_tips   # ← NEW

app = Flask(__name__)
app.secret_key = "resumedna_secret_2024"
app.config["UPLOAD_FOLDER"] = "uploads"

USERS_FILE = "data/users.json"

# ── User store helpers ──────────────────────────────────────
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f:
            return json.load(f)
    return {"admin": "password123", "student": "college2024"}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


# ── Unique filename helper ───────────────────────────────────
def make_unique_filepath(original_filename):
    """
    Generate a unique filepath so we NEVER overwrite an existing file.
    Fixes PermissionError [Errno 13] on Windows where files stay locked.
    """
    ext  = os.path.splitext(original_filename)[1].lower()
    stem = os.path.splitext(original_filename)[0]
    uid  = str(int(time.time())) + "_" + uuid.uuid4().hex[:4]
    unique_name = f"{uid}_{stem}{ext}"
    return os.path.join(app.config["UPLOAD_FOLDER"], unique_name)


# ── Resume text helper ──────────────────────────────────────
def get_resume_text(req, template, **tpl_kwargs):
    input_mode = req.form.get("input_mode", "file")

    if input_mode == "bio":
        text = req.form.get("bio_text", "").strip()
        if not text:
            return None, None, render_template(
                template, error="Please enter your bio text.", **tpl_kwargs)
        return text, None, None

    file = req.files.get("resume")
    if not file or file.filename == "":
        return None, None, render_template(
            template, error="Please upload a resume file.", **tpl_kwargs)

    allowed = {".pdf", ".docx"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        return None, None, render_template(
            template, error="Only PDF and DOCX files are accepted.", **tpl_kwargs)

    filepath = make_unique_filepath(file.filename)
    try:
        file.save(filepath)
    except PermissionError:
        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"], "tmp_" + uuid.uuid4().hex + ext)
        file.save(filepath)
    except Exception as e:
        return None, None, render_template(
            template, error=f"Could not save file: {str(e)}. Try again.", **tpl_kwargs)

    text = extract_text(filepath)
    if not text.strip():
        try:
            os.remove(filepath)
        except Exception:
            pass
        return None, None, render_template(
            template,
            error="Could not read text from this file. Make sure it is a real PDF or DOCX and not password-protected.",
            **tpl_kwargs)

    return text, filepath, None


# ═══════════════════════════════════════════════
# SIGNUP
# ═══════════════════════════════════════════════
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    success = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm  = request.form.get("confirm", "").strip()
        year     = request.form.get("year", "").strip()
        users = load_users()
        if not username or not password:
            error = "Username and password are required."
        elif len(username) < 3:
            error = "Username must be at least 3 characters."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif password != confirm:
            error = "Passwords do not match."
        elif username in users:
            error = f"Username '{username}' already exists. Choose another."
        else:
            users[username] = password
            save_users(users)
            success = "Account created successfully! You can now log in."
    return render_template("signup.html", error=error, success=success)


# ═══════════════════════════════════════════════
# LOGIN / LOGOUT
# ═══════════════════════════════════════════════
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        users = load_users()
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("home"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ═══════════════════════════════════════════════
# HOME — two option dashboard
# ═══════════════════════════════════════════════
@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session["user"])


# ═══════════════════════════════════════════════
# ATS CHECK  (resume/bio + JD required)
# ═══════════════════════════════════════════════
@app.route("/ats-check", methods=["GET", "POST"])
def ats_check():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("ats_check.html", username=session["user"])

    resume_text, filepath, err_response = get_resume_text(
        request, "ats_check.html", username=session["user"])
    if err_response:
        return err_response

    job_description = request.form.get("job_description", "").strip()
    if not job_description:
        return render_template("ats_check.html",
            error="Please paste a Job Description to calculate the ATS score.",
            username=session["user"])

    sections     = extract_sections(resume_text)
    skills_found = extract_skills(resume_text)

    ats_score, feedback, matched_kw, missing_kw = calculate_ats_score(
        resume_text=resume_text,
        sections=sections,
        job_description=job_description,
        filepath=filepath
    )

    # ── Resume Optimizer (shown when score < 75) ──────────────────────
    optimization_tips, projected_score = generate_optimization_tips(
        resume_text=resume_text,
        sections=sections,
        skills_found=skills_found,
        missing_keywords=missing_kw,
        ats_score=ats_score,
        job_description=job_description
    )

    return render_template("ats_result.html",
        ats_score=ats_score,
        feedback=feedback,
        matched_keywords=matched_kw,
        missing_keywords=missing_kw,
        skills=skills_found,
        education=sections.get("education", ""),
        projects=sections.get("projects", ""),
        experience=sections.get("experience", ""),
        optimization_tips=optimization_tips,        # ← NEW
        projected_score=projected_score,            # ← NEW
        username=session["user"]
    )


# ═══════════════════════════════════════════════
# CAREER PATH  (resume/bio only — no JD needed)
# ═══════════════════════════════════════════════
@app.route("/career-path", methods=["GET", "POST"])
def career_path():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("career_path.html", username=session["user"])

    resume_text, filepath, err_response = get_resume_text(
        request, "career_path.html", username=session["user"])
    if err_response:
        return err_response

    sections      = extract_sections(resume_text)
    skills_found  = extract_skills(resume_text)
    match_result  = match_roles(skills_found)
    skill_levels  = classify_skill_levels(skills_found, resume_text)
    career_dna    = generate_career_dna(skills_found)
    career_ready  = calculate_career_readiness(
        skills_found, sections.get("projects", ""), sections.get("experience", ""))
    top_role = list(match_result.keys())[0] if match_result else "Data Scientist"

    return render_template("career_result.html",
        skills=skills_found,
        skill_levels=skill_levels,
        results=match_result,
        career_paths=predict_career_path(top_role),
        top_role=top_role,
        career_dna=career_dna,
        career_readiness=career_ready,
        education=sections.get("education", ""),
        projects=sections.get("projects", ""),
        experience=sections.get("experience", ""),
        all_paths=ALL_CAREER_PATHS,
        username=session["user"]
    )


# ═══════════════════════════════════════════════
# SKILL GAP
# ═══════════════════════════════════════════════
@app.route("/skill-gap", methods=["POST"])
def skill_gap():
    if "user" not in session:
        return redirect(url_for("login"))

    user_skills = request.form.getlist("skills")
    role        = request.form.get("role")
    education   = request.form.get("education", "")
    projects    = request.form.get("projects", "")
    experience  = request.form.get("experience", "")

    required_skills, missing_skills = analyze_skill_gap(user_skills, role)
    courses_dict = recommend_courses(missing_skills)
    study_plan   = generate_study_plan(missing_skills)

    courses_list = [
        (skill, courses_dict[skill])
        for skill in missing_skills
        if skill in courses_dict
    ]

    return render_template("skill_gap.html",
        role=role,
        required_skills=required_skills,
        missing_skills=missing_skills,
        courses_list=courses_list,
        study_plan=study_plan,
        user_skills=user_skills,
        education=education,
        projects=projects,
        experience=experience,
        username=session["user"]
    )


# ═══════════════════════════════════════════════
# GENERATE RESUME
# ═══════════════════════════════════════════════
@app.route("/generate-resume", methods=["POST"])
def create_resume():
    if "user" not in session:
        return redirect(url_for("login"))

    from modules.resume_generator import generate_resume

    name            = request.form.get("name")
    role            = request.form.get("role")
    filetype        = request.form.get("filetype")
    original_skills = request.form.getlist("original_skills")
    required_skills = request.form.getlist("required_skills")
    education       = request.form.get("education", "")
    projects        = request.form.get("projects", "")
    experience      = request.form.get("experience", "")
    final_skills    = list(set(original_skills + required_skills))

    filename = generate_resume(name, role, final_skills, education, projects, experience, filetype)
    return send_from_directory("uploads", filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
