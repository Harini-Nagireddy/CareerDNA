# 🧬 CareerDNA — AI-Powered Career Intelligence Platform

> A Python Flask web application that analyzes student resumes, calculates ATS scores,
> predicts career paths, identifies skill gaps, and recommends learning resources.
> Built as a 3rd Year B.Tech Mini Project.

---

## 📋 Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [How CareerDNA Solves It](#2-how-CareerDNA-solves-it)
3. [What This Project Does](#3-what-this-project-does)
4. [Project Folder Structure](#4-project-folder-structure)
5. [Tools and Libraries Used](#5-tools-and-libraries-used)
6. [ATS Score Formula](#6-ats-score-formula)
7. [Setting Up the Virtual Environment](#7-setting-up-the-virtual-environment)
8. [How to Install and Run](#8-how-to-install-and-run)
9. [Line-by-Line Code Explanation](#9-line-by-line-code-explanation)
   - [app.py](#apppy)
   - [modules/resume_parser.py](#modulesresume_parserpy)
   - [modules/section_extractor.py](#modulessection_extractorpy)
   - [modules/skill_extractor.py](#modulesskill_extractorpy)
   - [modules/ats_calculator.py](#modulesats_calculatorpy)
   - [modules/role_matcher.py](#modulesrole_matcherpy)
   - [modules/career_path_predictor.py](#modulescareer_path_predictorpy)
   - [modules/skill_gap_analyzer.py](#modulesskill_gap_analyzerpy)
   - [modules/course_recommender.py](#modulescourse_recommenderpy)
   - [modules/study_plan_generator.py](#modulesstudy_plan_generatorpy)
   - [modules/skill_level_classifier.py](#modulesskill_level_classifierpy)
   - [modules/career_dna_analyzer.py](#modulescareer_dna_analyzerpy)
   - [modules/career_readiness.py](#modulescareer_readinesspy)
10. [Page-by-Page Template Explanation](#10-page-by-page-template-explanation)
11. [Data Files Explanation](#11-data-files-explanation)
12. [User Flow Diagram](#12-user-flow-diagram)
13. [Demo Credentials](#13-demo-credentials)
14. [Known Limitations & Future Scope](#14-known-limitations--future-scope)

---

## 1. Problem Statement

Every year, thousands of engineering students graduate and apply for jobs or internships.
Most of them face the same silent problem — **their resumes never even reach a human recruiter.**

Modern companies use **ATS (Applicant Tracking Systems)** — software that automatically scans resumes and filters out candidates before a human ever reads them. A resume is rejected if:

- It is missing important keywords from the job description
- It lacks proper sections (Skills, Education, Experience, Projects)
- It uses non-standard formatting or fonts
- It does not use action verbs or measurable achievements

Beyond the resume problem, students — especially in 1st and 2nd year — have **no idea which
career path suits them** based on their current skills, what skills they are missing, or what courses they should take next.

**There is no single free tool that:**
- Tells a student exactly why their resume is failing ATS
- Compares their resume against a real job description
- Recommends a personalized career path from their existing skills
- Shows a week-by-week plan to fill the skill gaps

---

## 2. How CareerDNA Solves It

CareerDNA is a two-in-one platform built specifically for engineering students:

### 🔵 Path 1 — ATS Score Checker (for 3rd & 4th year students applying for jobs/internships)
The student uploads their resume and pastes a Job Description from LinkedIn or Naukri.
CareerDNA compares the two using a weighted formula and produces:
- A score out of 100
- Which keywords from the JD are present/missing in the resume
- Specific tips to improve the resume

### 🟣 Path 2 — Career Path Explorer (for 1st & 2nd year students with no JD)
The student uploads their resume or types a short bio about themselves.
CareerDNA reads their skills and produces:
- A ranked list of tech roles that best match their skills
- A full career progression ladder (e.g. Junior → Senior → Architect)
- Skill gap analysis against any target role
- Course recommendations (free + paid) for every missing skill
- A week-by-week study plan

---

## 3. What This Project Does

| Feature | Description |
|---|---|
| 🔐 Signup / Login | Students create accounts. Credentials stored in `data/users.json` |
| 📄 Resume Upload | Accepts PDF and DOCX files, extracts plain text automatically |
| ✏️ Bio Input | Students who don't have a resume can type their skills and background |
| 📊 ATS Score | Compares resume with job description using a weighted scoring formula |
| 🗺️ Career Path | Matches skills to 10 tech roles and shows a full progression roadmap |
| 🔍 Skill Gap | Shows which skills are missing for any target role |
| 📚 Courses | Recommends free (YouTube, freeCodeCamp) and paid (Udemy, Coursera) courses |
| 🗓️ Study Plan | Generates a week-by-week learning schedule |


---

## 4. Project Folder Structure

```
CareerDNA/
│
├── app.py                          ← Main Flask application (all routes)
│
├── requirements.txt                ← All Python libraries to install
│
├── data/
│   ├── skills.txt                  ← Master list of tech skills (one per line)
│   ├── job_roles.json              ← Required skills for each of 10 tech roles
│   ├── courses.json                ← Free + paid course links for each skill
│   └── users.json                  ← Registered user accounts (auto-created)
│
├── modules/
│   ├── resume_parser.py            ← Extracts text from PDF and DOCX files
│   ├── section_extractor.py        ← Finds Education, Skills, Experience sections
│   ├── skill_extractor.py          ← Detects skills mentioned in resume text
│   ├── ats_calculator.py           ← Calculates ATS score (with or without JD)
│   ├── role_matcher.py             ← Matches user skills to 10 tech roles
│   ├── career_path_predictor.py    ← Returns career progression levels per role
│   ├── skill_gap_analyzer.py       ← Finds missing skills for a target role
│   ├── course_recommender.py       ← Looks up courses for missing skills
│   ├── study_plan_generator.py     ← Creates week-by-week learning schedule
│   ├── skill_level_classifier.py   ← Rates each skill as Beginner/Intermediate/Advanced
│   ├── career_dna_analyzer.py      ← Generates a career profile type from skills
│   ├── career_readiness.py         ← Calculates a career readiness score (0–100)
|
│
├── templates/
│   ├── login.html                  ← Login page
│   ├── signup.html                 ← Registration page
│   ├── index.html                  ← Dashboard — two option buttons after login
│   ├── ats_check.html              ← ATS Check input page (resume/bio + JD)
│   ├── ats_result.html             ← ATS score results page
│   ├── career_path.html            ← Career path input page (resume/bio only)
│   ├── career_result.html          ← Career path results page
│   ├── skill_gap.html              ← Skill gap + courses + study plan
│   └── (legacy templates)          ← result.html, career_dashboard.html, etc.
│
└── uploads/
    └── (resume files saved here)
```

---

## 5. Tools and Libraries Used

### Backend

| Library | Version | Why It Is Used |
|---|---|---|
| **Flask** | latest | The web framework. Handles all routes, form submissions, sessions, and renders HTML templates |
| **pdfplumber** | latest | Opens PDF files and extracts all the text from each page |
| **python-docx** | latest | Opens `.docx` Word files and extracts paragraph text. Also used to generate new DOCX resumes |
| **re** (built-in) | stdlib | Python's regex library. Used for pattern matching: finding section headers, phone numbers, email addresses, percentages |
| **json** (built-in) | stdlib | Reads and writes `.json` data files (job roles, courses, users) |
| **os** (built-in) | stdlib | Handles file paths, checks if files exist, joins directory names |
| **collections.Counter** | stdlib | Counts word frequency in resume text for JD keyword matching |

### Frontend

| Technology | Why It Is Used |
|---|---|
| **HTML5** | Structure of every page |
| **CSS3** | Styling — gradients, cards, responsive layout, animations |
| **Vanilla JavaScript** | Toggle between file upload and bio text mode, drag-and-drop file zone, show selected filename |
| **Google Fonts (Inter)** | Clean, modern font used across all pages |
| **Jinja2** | Flask's built-in template engine — used to inject Python variables into HTML (e.g. `{{ ats_score }}`) |

### Data Storage

| File | Format | Purpose |
|---|---|---|
| `data/users.json` | JSON | Stores registered usernames and passwords |
| `data/skills.txt` | Plain text | One skill per line — master list used to detect skills in resume text |
| `data/job_roles.json` | JSON | Maps each of 10 roles to the list of required skills |
| `data/courses.json` | JSON | Maps each skill to free and paid course objects with name and link |

> **Note:** This project does not use a database like MySQL or SQLite.
> All data is stored in JSON files. For a production version, replace `users.json`
> with a proper database (e.g. SQLite with Flask-SQLAlchemy).

---

## 6. ATS Score Formula

### Mode A — With Job Description (used in ATS Check page)

```
ATS Score = (0.40 × JD Keyword Match Score)
           + (0.35 × Structure Score)
           + (0.15 × Action Verb Score)
           + (0.10 × Formatting Score)
```

| Component | Weight | How It Is Measured |
|---|---|---|
| **JD Keyword Match** | 40% | How many words from the JD appear in the resume. Stopwords removed. Synonyms expanded (e.g. "ml" counts as "machine learning") |
| **Structure Score** | 35% | Are Skills, Education, Experience, Projects sections present? Are there 8+ skills? |
| **Action Verb Score** | 15% | Count of power verbs like "developed", "built", "optimized", "deployed" (need 5+) |
| **Formatting Score** | 10% | Are there bullet points (5+)? Is the resume more than 300 words? |

### Mode B — Without Job Description (used inside Career Path page)

```
ATS Score = Skills Score (30)
           + Sections Score (20)
           + Action Verbs Score (15)
           + Keyword Hits Score (15)
           + Bullet Points Score (10)
           + Measurable Results Score (5)
           + Length Score (5)
           = Maximum 100
```

---

## 7. Setting Up the Virtual Environment

A virtual environment keeps this project's libraries separate from your system Python.
Always use a virtual environment for Flask projects.

### Step 1 — Make sure Python is installed

```bash
python --version
# Should show Python 3.8 or higher
```

If Python is not installed, download it from https://www.python.org/downloads/

### Step 2 — Navigate to the project folder

```bash
cd path/to/CareerDNA
# Example on Windows:  cd C:\Users\YourName\Desktop\CareerDNA
# Example on Mac/Linux: cd ~/Desktop/CareerDNA
```

### Step 3 — Create the virtual environment

```bash
python -m venv venv
```

This creates a folder called `venv` inside your project. It contains a private copy of Python
and pip. You will not see it in your templates or modules — it is only for dependencies.

### Step 4 — Activate the virtual environment

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**On Mac / Linux:**
```bash
source venv/bin/activate
```

After activation, your terminal prompt will change to show `(venv)` at the beginning.
This means the virtual environment is active and any `pip install` will go into it.

### Step 5 — Deactivate when done

```bash
deactivate
```

---

## 8. How to Install and Run

### Step 1 — Clone or extract the project

If you downloaded the zip file, extract it. If using Git:

```bash
git clone https://github.com/yourname/CareerDNA.git
cd CareerDNA
```

### Step 2 — Activate the virtual environment (see Section 7 above)

```bash
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install all dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, pdfplumber, python-docx, docx2pdf, and all other libraries.

> **If docx2pdf fails on Linux/Mac**, it requires LibreOffice to be installed.
> Install it with: `sudo apt install libreoffice` (Ubuntu) or `brew install libreoffice` (Mac)

### Step 4 — Make sure the uploads folder exists

```bash
# Windows:
mkdir uploads

# Mac/Linux:
mkdir -p uploads
```

### Step 5 — Run the Flask application

```bash
python app.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 6 — Open in browser

Go to: **http://127.0.0.1:5000**

You will see the Login page. Use the demo credentials or create a new account.

### Demo Credentials

| Username | Password |
|---|---|
| admin | password123 |
| student | college2024 |

---

## 9. Line-by-Line Code Explanation

---

### `app.py`

This is the main file that runs the entire web application. Every page the user visits,
every form they submit, is handled here.

```python
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
```
> Imports the core Flask tools:
> - `Flask` — creates the app
> - `render_template` — loads an HTML file from the `templates/` folder
> - `request` — reads form data and uploaded files the user submitted
> - `send_from_directory` — sends a file (like a generated resume) as a download
> - `redirect` — sends the user to a different URL
> - `url_for` — generates a URL from a function name (avoids hardcoding URLs)
> - `session` — stores login state in the browser (like "who is logged in")

```python
import os, json
```
> - `os` — used to build file paths and check if files exist
> - `json` — used to read/write the users.json file

```python
from modules.resume_parser import extract_text
from modules.section_extractor import extract_sections
# ... (all other module imports)
```
> Imports all the functions from the separate module files. Each module handles one job.
> This keeps the code organised — `app.py` only handles routes, not logic.

```python
app = Flask(__name__)
```
> Creates the Flask application object. `__name__` tells Flask where to look for templates
> and static files (relative to this file's location).

```python
app.secret_key = "CareerDNA_secret_2024"
```
> A secret key used to encrypt the session cookie stored in the browser.
> Without this, Flask cannot securely store login information between requests.
> In production, this should be a long random string stored in an environment variable.

```python
app.config["UPLOAD_FOLDER"] = "uploads"
```
> Tells Flask where to save uploaded resume files.
> All PDFs and DOCX files the user uploads get saved into the `uploads/` folder.

```python
USERS_FILE = "data/users.json"
```
> Path to the file that stores all registered users. Using a constant makes it
> easy to change the path in one place if needed.

```python
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f:
            return json.load(f)
    return {"admin": "password123", "student": "college2024"}
```
> Opens `data/users.json` and returns a dictionary like `{"admin": "password123"}`.
> If the file does not exist yet (first run), returns the two default accounts.
> `os.path.exists` checks if the file is present before trying to open it.

```python
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
```
> Takes the updated users dictionary and writes it back to `data/users.json`.
> `indent=2` makes the JSON file readable with proper indentation.

```python
def get_resume_text(request, template, **tpl_kwargs):
```
> A shared helper function called by both the ATS Check route and the Career Path route.
> Both pages need to either accept a file upload or a bio text input, so instead of
> writing the same code twice, it is put here once.

```python
    input_mode = request.form.get("input_mode", "file")
```
> Reads which mode the user chose — "file" (upload) or "bio" (text box).
> The HTML toggle buttons set a hidden input field called `input_mode`.

```python
    if input_mode == "bio":
        text = request.form.get("bio_text", "").strip()
```
> If bio mode, reads the text the user typed into the textarea. `.strip()` removes
> any leading or trailing whitespace.

```python
    else:
        file = request.files.get("resume")
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        text = extract_text(filepath)
```
> If file mode: gets the uploaded file from the form, builds the full path
> (e.g. `uploads/myresume.pdf`), saves it to disk, then calls `extract_text()`
> to convert the file into a plain text string.

```python
@app.route("/signup", methods=["GET", "POST"])
def signup():
```
> Registers a new URL route. `methods=["GET", "POST"]` means this function handles
> both visiting the page (GET) and submitting the signup form (POST).

```python
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm  = request.form.get("confirm", "").strip()
```
> When the form is submitted, reads all three fields the user typed.
> `.strip()` removes accidental spaces.

```python
        users = load_users()
        if username in users:
            error = f"Username '{username}' already exists."
        else:
            users[username] = password
            save_users(users)
            success = "Account created successfully!"
```
> Loads existing users, checks if the username is already taken, and if not,
> adds the new user and saves the updated dictionary back to the JSON file.

```python
@app.route("/", methods=["GET", "POST"])
def login():
    ...
    if username in users and users[username] == password:
        session["user"] = username
        return redirect(url_for("home"))
```
> The login route at the root URL `/`. On a successful login:
> - `session["user"] = username` saves the username in the session cookie.
>   This is what keeps the user "logged in" across page refreshes.
> - `redirect(url_for("home"))` sends the user to the `/home` page.

```python
@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session["user"])
```
> The dashboard page. The `if "user" not in session` check is the login guard —
> if someone tries to visit `/home` without logging in, they get sent back to login.
> `render_template` loads `templates/index.html` and passes the username variable
> so the HTML can display "Welcome back, admin!".

```python
@app.route("/ats-check", methods=["GET", "POST"])
def ats_check():
    if request.method == "GET":
        return render_template("ats_check.html", username=session["user"])
```
> The ATS Check page. On a GET request (user just navigated here), it shows the form.
> On a POST request (user submitted the form), it runs the analysis.

```python
    job_description = request.form.get("job_description", "").strip()
    if not job_description:
        return render_template("ats_check.html",
            error="Please paste a Job Description to calculate the ATS score.",
            username=session["user"])
```
> Checks that the user actually pasted a JD. If the field is empty, the page
> reloads with an error message. The ATS Check requires a JD — it is not optional.

```python
    ats_score, feedback, matched_kw, missing_kw = calculate_ats_score(
        resume_text=resume_text,
        sections=sections,
        job_description=job_description,
        filepath=filepath
    )
```
> Calls the ATS calculator with all four pieces of information.
> Returns four values: the score (0-100), a list of improvement tips,
> a list of JD keywords found in the resume, and a list of JD keywords missing.

```python
@app.route("/career-path", methods=["GET", "POST"])
def career_path():
```
> The Career Path page. This route does NOT require a job description.
> It only needs the resume or bio text.

```python
    match_result  = match_roles(skills_found)
    top_role = list(match_result.keys())[0] if match_result else "Data Scientist"
```
> `match_roles()` returns a dictionary sorted by match percentage (highest first).
> `.keys()[0]` gets the first key — the best matching role.

```python
@app.route("/skill-gap", methods=["POST"])
def skill_gap():
    ...
    courses_list = [(skill, courses_dict[skill]) for skill in missing_skills if skill in courses_dict]
```
> **This is the bug fix.** The original code passed `courses` as a Python dict to Jinja.
> In Jinja, `courses["node.js"]` fails because the dot in "node.js" is interpreted as
> attribute access (`courses.node`, then `.js`), which does not exist.
> The fix converts the dict into a **list of tuples**: `[("node.js", {...}), ("docker", {...})]`.
> In the template, `{% for skill, course_data in courses_list %}` safely unpacks each tuple
> without any dot-notation lookup.

---

### `modules/resume_parser.py`

```python
import os

def extract_text(file_path):
    if file_path is None:
        return ""
```
> Guards against `None` being passed (when user chose bio mode, filepath is None).

```python
    if file_path.endswith(".pdf"):
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
```
> Uses `pdfplumber` to open the PDF. Loops through every page, extracts the text,
> and appends it. The `if content:` check skips blank pages that return `None`.

```python
    elif file_path.endswith(".docx"):
        from docx import Document
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
```
> Uses `python-docx` to open a Word document. A Word file is made of paragraphs —
> this loops through all of them and joins their text with newlines.

---

### `modules/section_extractor.py`

```python
import re

def extract_sections(text):
    sections = {"skills": "", "education": "", "projects": "", "experience": ""}
    text = text.lower()
```
> Converts text to lowercase so "SKILLS", "Skills", and "skills" all match.

```python
    skills_pattern = r"(skills|technical skills)(.*?)(education|projects|experience|$)"
    skills = re.search(skills_pattern, text, re.DOTALL)
```
> This regex finds everything between the word "skills" and the next section heading.
> `re.DOTALL` makes `.` match newlines too (so it captures multi-line sections).
> `.*?` is non-greedy — it stops at the first match, not the last.

```python
    if skills:
        sections["skills"] = skills.group(2)
```
> `group(2)` returns the second captured group — the content between the section
> header and the next header (not the headers themselves).

---

### `modules/skill_extractor.py`

```python
def load_skills():
    with open("data/skills.txt", "r") as file:
        skills = file.read().splitlines()
    return [skill.lower() for skill in skills]
```
> Reads `data/skills.txt`, splits it into one skill per line, and lowercases all.
> `splitlines()` is better than `split("\n")` — it handles Windows `\r\n` line endings too.

```python
def extract_skills(text):
    skills_list = load_skills()
    text = text.lower()
    found_skills = []
    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)
    return found_skills
```
> Simple substring search — if "python" appears anywhere in the resume text,
> it is added to the found skills list. The entire text and all skills are lowercase
> so "Python", "PYTHON", and "python" all match.

---

### `modules/ats_calculator.py`

```python
ACTION_VERBS = [
    "developed", "built", "implemented", "designed", "created", "improved", ...
]
```
> A list of strong resume action verbs. A resume that uses these words in bullet points
> is more likely to pass ATS systems because it shows impact and ownership.

```python
SYNONYMS = {
    "machine learning": ["ml"],
    "natural language processing": ["nlp"],
    "react": ["react.js", "reactjs"],
    "node.js": ["nodejs", "node"],
    "javascript": ["js"],
}
```
> Maps full skill names to their common abbreviations and vice versa.
> This makes the keyword matching smarter — if a JD says "ML" and the resume
> says "machine learning", it still counts as a match.

```python
def _normalize(text):
    return re.sub(r"[^a-zA-Z0-9 ]", " ", text.lower())
```
> Removes all punctuation (commas, dots, slashes, hyphens) and lowercases everything.
> This ensures "Python," and "Python" both match "python". The leading `_` means
> this is a private helper function — not intended to be called from outside this file.

```python
def _expand_keywords(keywords):
    expanded = set()
    for kw in keywords:
        expanded.add(kw)
        if kw in SYNONYMS:
            expanded.update(SYNONYMS[kw])
        for key, vals in SYNONYMS.items():
            if kw in vals:
                expanded.add(key)
    return expanded
```
> For every keyword, adds the keyword itself plus all its synonyms.
> Also checks the reverse — if the keyword is a synonym value, adds the main key too.
> Returns a `set` so there are no duplicates.

```python
def _structure_score(skills, sections, resume_text):
    score = 0
    feedback = []

    skill_count = len(skills)
    if skill_count >= 8:
        score += 30
    elif skill_count >= 5:
        score += 20
    else:
        score += 10
        feedback.append("Too few skills detected — add technical skills")
```
> Awards 30 points if 8+ skills are found, 20 for 5–7 skills, 10 for fewer.
> If points are deducted, a human-readable tip is added to the feedback list.

```python
    verb_count = sum(len(re.findall(r"\b" + v + r"\b", text_lower)) for v in ACTION_VERBS)
```
> For each action verb, counts how many times it appears in the resume using `\b`
> word boundaries so "built" does not match "rebuilt". Sums all counts.

```python
    raw = (
        0.40 * jd_match_pct * 100 +
        0.35 * (struct_score / 65) * 100 +
        0.15 * verb_ratio * 100 +
        0.10 * fmt_score * 100
    )
    ats_score = round(min(raw, 100))
```
> The final weighted formula. Each component is normalised to a 0–1 or 0–100 range
> before being multiplied by its weight. `min(..., 100)` ensures the score never
> exceeds 100. `round()` gives a clean integer.

---

### `modules/role_matcher.py`

```python
def match_roles(user_skills):
    roles = {
        "Data Scientist": ["python", "machine learning", "pandas", "numpy", "nlp", ...],
        "Full Stack Developer": ["html", "css", "javascript", "react", "flask", "node.js", ...],
        ...
    }
    user_skills_lower = [s.lower() for s in user_skills]

    for role, required in roles.items():
        matched = len(set(user_skills_lower) & set(required))
        score = int((matched / len(required)) * 100)
        results[role] = score
```
> For each role, computes the intersection (`&`) of the user's skills and the
> role's required skills. Divides matched count by total required and multiplies
> by 100 to get a percentage. `set()` is used so duplicate skills don't inflate the score.

```python
    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
```
> Sorts the roles by score (highest first) so the best match appears at the top.
> `lambda x: x[1]` sorts by the value (score), not the key (role name).

---

### `modules/career_path_predictor.py`

```python
ALL_CAREER_PATHS = {
    "Data Scientist": {
        "icon": "🔬",
        "description": "Analyze complex data, build ML models, and derive business insights.",
        "levels": ["Junior Data Scientist", "Data Scientist", "Senior Data Scientist", ...],
        "core_skills": ["Python", "Statistics", "Machine Learning", ...],
        "salary_range": "₹6L – ₹35L"
    },
    ...
}
```
> A dictionary of 10 tech career paths. Each entry has an icon, description,
> career progression levels (from entry to senior), required skills, and salary range.
> This data is used both on the Career Result page and the dedicated Career Paths page.

```python
def predict_career_path(role):
    if role in ALL_CAREER_PATHS:
        return ALL_CAREER_PATHS[role]["levels"]
    role_lower = role.lower()
    for key in ALL_CAREER_PATHS:
        if role_lower in key.lower() or key.lower() in role_lower:
            return ALL_CAREER_PATHS[key]["levels"]
    return ["Junior Engineer", "Software Engineer", "Senior Engineer", ...]
```
> First tries an exact match. If that fails, tries a fuzzy match (does the role
> name appear inside any key, or vice versa). If nothing matches, returns a
> generic engineering progression as a fallback.

---

### `modules/skill_gap_analyzer.py`

```python
def analyze_skill_gap(user_skills, selected_role):
    roles = load_job_roles()              # reads data/job_roles.json
    required_skills = roles.get(selected_role, [])

    missing_skills = []
    for skill in required_skills:
        if skill not in user_skills:
            missing_skills.append(skill)

    return required_skills, missing_skills
```
> Loads the required skills for the selected role from `job_roles.json`.
> Checks each required skill against the user's detected skills.
> Returns both the full required list and only the missing ones.

---

### `modules/course_recommender.py`

```python
def recommend_courses(missing_skills):
    course_data = load_courses()          # reads data/courses.json
    recommendations = {}
    for skill in missing_skills:
        if skill in course_data:
            recommendations[skill] = course_data[skill]
    return recommendations
```
> For each missing skill, looks up its entry in `courses.json`.
> Only adds it to results if a course entry exists (skips skills with no course data).
> Returns a dictionary: `{ "python": { "free": [...], "paid": [...] }, ... }`.

---

### `modules/study_plan_generator.py`

```python
def generate_study_plan(missing_skills):
    study_plan = []
    week = 1
    for skill in missing_skills:
        plan = {"week": f"Week {week}", "task": f"Learn {skill}"}
        study_plan.append(plan)
        week += 1
    study_plan.append({"week": f"Week {week}", "task": "Build a mini project using learned skills"})
    return study_plan
```
> Creates one study week per missing skill, then adds a final "build a project" week.
> Returns a list of dictionaries, each with `week` and `task` keys.
> These are displayed as a table in `skill_gap.html`.

---

### `modules/skill_level_classifier.py`

```python
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
```
> Uses mention frequency as a proxy for skill depth. If a skill appears 3+ times
> in the resume (e.g. mentioned in skills section, a project, and experience), it
> is labelled Advanced. Once = Intermediate. Zero times but still detected = Beginner.

---

### `modules/career_dna_analyzer.py`

```python
def generate_career_dna(skills):
    profile = {}
    if "machine learning" in skills or "python" in skills:
        profile["type"] = "AI/Data Innovator"
    elif "javascript" in skills or "react" in skills:
        profile["type"] = "Web Technology Builder"
    else:
        profile["type"] = "Technology Explorer"
    profile["strengths"] = skills[:5]
    profile["growth_areas"] = ["Cloud Computing", "System Design", "Industry Projects"]
    return profile
```
> Creates a simple profile based on the student's top skills. Returns a dictionary
> with a `type` (career personality), `strengths` (first 5 skills), and standard
> `growth_areas` that benefit all tech students.

---

### `modules/career_readiness.py`

```python
def calculate_career_readiness(skills, projects, experience):
    score = 0
    if len(skills) >= 6:
        score += 40
    if projects.strip():
        score += 30
    if experience.strip():
        score += 30
    return score
```
> A simple readiness score (0–100). Having 6+ skills gives 40 points, having a
> projects section gives 30, and having any work experience gives 30.
> This tells the student how job-ready they are overall.

---


```python
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx2pdf import convert
```
> Imports from `python-docx` to build Word documents programmatically.
> `Pt` is "Points" — a unit for font size. `WD_ALIGN_PARAGRAPH` lets you center text.
> `convert` from `docx2pdf` converts the final DOCX to PDF.

```python
def generate_resume(name, role, skills, education, projects, experience, filetype):
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10)
```
> Creates a new blank Word document. Sets the default font to Calibri 10pt —
> an ATS-friendly standard font.

```python
    name_para = doc.add_paragraph()
    name_run = name_para.add_run(name.upper())
    name_run.bold = True
    name_run.font.size = Pt(14)
    name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
```
> Adds the candidate's name as a centered, bold, 14pt heading.
> `add_run()` creates a text segment inside a paragraph — runs can have different
> formatting within the same paragraph.

```python
    if filetype == "pdf":
        pdf_path = os.path.join("uploads", "generated_resume.pdf")
        convert(docx_path, pdf_path)
        return "generated_resume.pdf"
    return filename
```
> If the user chose PDF, converts the saved DOCX to PDF using `docx2pdf`.
> Returns the filename so Flask can send it as a download.

---

## 10. Page-by-Page Template Explanation

All HTML files are in `templates/` and use **Jinja2** template syntax.

### `login.html`
- Dark glassmorphism design with a blurred card effect
- `method="POST"` sends username and password to the `/` route
- `{% if error %}` shows the error banner only when Flask passes an error variable
- Links to `/signup` for new users

### `signup.html`
- Collects full name, username, college year, password, and confirm password
- `<select name="year">` lets student pick their college year
- On success, shows a green banner with a link back to login
- `method="POST"` sends data to the `/signup` route

### `index.html` (Dashboard)
- Shows two large clickable cards after login
- Blue card → `/ats-check` (requires JD)
- Purple card → `/career-path` (no JD needed)
- Yellow info box specifically guides 1st and 2nd year students

### `ats_check.html`
- Toggle between "Upload File" and "Write Bio" modes
- A hidden `<input name="input_mode">` stores which mode is active
- JavaScript function `switchMode()` shows/hides the correct section
- JD textarea is marked REQUIRED in the UI (red badge)
- Drag-and-drop zone with JavaScript event listeners

### `ats_result.html`
- Dynamic score ring using CSS `conic-gradient` — the ring fills based on the score
- Ring color changes: green (≥75), yellow (50–74), red (<50)
- Two columns: matched JD keywords (green tags) vs missing keywords (red tags)
- Sections detected panel shows which resume sections were found

### `career_path.html`
- Same toggle as ATS check (upload or bio)
- Purple theme to visually separate it from the blue ATS Check
- Info box explicitly says "No Job Description needed" to reassure 1st/2nd year students

### `career_result.html`
- Purple hero banner showing best matched role
- Animated bar chart for all 10 role match scores
- Career progression steps with the current level highlighted
- Skill gap form lets user pick any target role and click "Analyze Skill Gap"

### `skill_gap.html`
- Lists required skills (green) and missing skills (red)
- Courses section uses `{% for skill, course_data in courses_list %}` (tuple unpacking)
  — this is the fix for the `node.js` UndefinedError
- Free courses show in green, paid courses in yellow
- Study plan displayed as a week-by-week table


---

## 11. Data Files Explanation

### `data/skills.txt`
One skill per line. The `skill_extractor.py` module loads this and checks if each
skill appears anywhere in the resume text.

```
python
java
sql
machine learning
pandas
numpy
...
```

### `data/job_roles.json`
Maps each of 10 tech roles to a list of required skills.
Used by `skill_gap_analyzer.py` to find what a student is missing.

```json
{
  "Data Scientist": ["python", "pandas", "numpy", "machine learning", "sql"],
  "Full Stack Developer": ["html", "css", "javascript", "react", "flask", "node.js"],
  ...
}
```

### `data/courses.json`
Maps each skill to free and paid course objects.
Used by `course_recommender.py`. Each course has a `name` and a `link`.

```json
{
  "python": {
    "free": [
      {"name": "Python – freeCodeCamp", "link": "https://youtube.com/..."}
    ],
    "paid": [
      {"name": "Complete Python Bootcamp – Udemy", "link": "https://udemy.com/..."}
    ]
  }
}
```

### `data/users.json`
Auto-created when the first user signs up. Stores usernames and plain-text passwords.

```json
{
  "admin": "password123",
  "student": "college2024",
  "john": "mypassword"
}
```

> ⚠️ **Security Note:** This project stores passwords as plain text for simplicity.
> In a real production application, always hash passwords using `bcrypt` or
> `werkzeug.security.generate_password_hash` before storing them.

---

## 12. User Flow Diagram

```
Visit http://127.0.0.1:5000
           │
           ▼
    ┌─────────────┐
    │  Login Page │ ──── Don't have account? ──→ Signup Page → Create account → Login
    └──────┬──────┘
           │ Correct credentials
           ▼
    ┌─────────────────┐
    │   Dashboard     │
    │  (index.html)   │
    └────────┬────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
 ┌─────────┐   ┌──────────────┐
 │ ATS     │   │ Career Path  │
 │ Check   │   │ Explorer     │
 └────┬────┘   └──────┬───────┘
      │               │
      │ Resume/Bio     │ Resume/Bio only
      │ + JD required  │ (no JD needed)
      │               │
      ▼               ▼
 ┌──────────┐   ┌──────────────┐
 │ ATS      │   │ Career       │
 │ Result   │   │ Result       │
 │ Page     │   │ Page         │
 └──────────┘   └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │  Skill Gap   │
                │  Page        │
                │  + Courses   │
                │  + Study Plan│
                │              │
                │              │
                └──────────────┘
```

---

## 13. Demo Credentials

| Username | Password | Use For |
|---|---|---|
| `admin` | `password123` | Testing all features |
| `student` | `college2024` | Testing as a student |

Or create your own account by clicking **Sign Up** on the login page.

---

## 14. Known Limitations & Future Scope

### Current Limitations

| Limitation | Reason |
|---|---|
| Passwords stored as plain text | Simplified for college project. Use bcrypt in production |
| No real database | Uses JSON files. Data is lost if files are deleted |
| Section extraction is regex-based | May miss sections in unusual resume formats |
| `docx2pdf` may fail on some systems | Requires LibreOffice on Linux/Mac |
| Skill detection is keyword-based | Cannot understand context — "I don't know Python" would still match Python |

### Future Improvements

- Replace `users.json` with SQLite + Flask-SQLAlchemy
- Add password hashing with `werkzeug.security`
- Use spaCy NLP for smarter section and skill extraction
- Add resume scoring history — track progress over time
- Add LinkedIn job scraping to fetch real JDs automatically
- Deploy to Heroku, Railway, or AWS using Gunicorn + Nginx
- Add OAuth (Google/GitHub) login
- Add email OTP for password reset

---