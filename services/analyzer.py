import re

# =========================
# 🔥 CLASSIFY: Resume vs JD
# =========================
def classify_text(text):
    resume_keywords = ["education", "skills", "projects", "experience", "cgpa"]
    jd_keywords = ["responsibilities", "requirements", "job", "role", "looking for"]

    text = text.lower()

    resume_score = sum(1 for word in resume_keywords if word in text)
    jd_score = sum(1 for word in jd_keywords if word in text)

    return "resume" if resume_score > jd_score else "jd"


# =========================
# 🧠 DOMAIN DETECTION
# =========================
def detect_domain(text):
    text = text.lower()

    software_keywords = [
        "python","java","c++","javascript","react","node","api","backend",
        "framework","ai","ml","llm","database","cloud","system","design"
    ]

    mechanical_keywords = [
        "mechanical","cad","solidworks","autocad","manufacturing",
        "design","industrial","simulation","production"
    ]

    nontech_keywords = [
        "customer","excel","communication","support",
        "documentation","management","operations"
    ]

    s = sum(1 for w in software_keywords if w in text)
    m = sum(1 for w in mechanical_keywords if w in text)
    n = sum(1 for w in nontech_keywords if w in text)

    if s >= m and s >= n:
        return "software"
    elif m >= s and m >= n:
        return "mechanical"
    else:
        return "nontech"


# =========================
# 📚 SKILL DATABASE
# =========================
SOFTWARE_SKILLS = {
    "python","java","c++","javascript",
    "react","node","nodejs","frontend","backend","fullstack",
    "html","css","api","rest","graphql",
    "sql","nosql","mongodb","database",
    "aws","cloud","docker","kubernetes",
    "git","github",
    "debugging","testing","optimization","scalability"
}

MECHANICAL_SKILLS = {
    "mechanical","cad","solidworks","autocad",
    "manufacturing","design","simulation","production"
}

NONTECH_SKILLS = {
    "excel","communication","customer","support",
    "management","documentation","operations"
}


# =========================
# 🔥 EXTRACT SKILLS
# =========================
def extract_skills(text, domain=None):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    words = text.split()

    if domain is None:
        domain = detect_domain(text)

    if domain == "software":
        db = SOFTWARE_SKILLS
    elif domain == "mechanical":
        db = MECHANICAL_SKILLS
    else:
        db = NONTECH_SKILLS

    return list(set([w for w in words if w in db]))


# =========================
# 🔥 FINAL ADVANCED MATCH
# =========================
def compare_skills(jd_text, resume_text):

    # Detect domains (for info only)
    jd_domain = detect_domain(jd_text)
    resume_domain = detect_domain(resume_text)

    # Extract skills
    jd_skills = set(extract_skills(jd_text, jd_domain))
    resume_skills = set(extract_skills(resume_text, resume_domain))

    # Core comparison
    matched = list(jd_skills & resume_skills)
    missing = list(jd_skills - resume_skills)
    extra = list(resume_skills - jd_skills)

    # 🎯 Score (never forced 0)
    score = 0
    if jd_skills:
        score = int((len(matched) / len(jd_skills)) * 100)

    # 💡 Improvements (smart suggestions)
    improvements = []

    if missing:
        improvements.append("Add missing skills from JD")
        improvements.append("Build projects using missing skills")

    if extra:
        improvements.append("Reduce less relevant skills")

    if jd_domain != resume_domain:
        improvements.append("Your domain is different from JD, consider aligning your profile")

    if score < 50:
        improvements.append("Improve overall alignment with job role")

    # ✅ RETURN FULL DATA (NO EMPTY OUTPUT EVER)
    return {
        "score": score,
        "jd_domain": jd_domain,
        "resume_domain": resume_domain,
        "jd_skills": list(jd_skills),
        "resume_skills": list(resume_skills),
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "improvements": improvements
    }