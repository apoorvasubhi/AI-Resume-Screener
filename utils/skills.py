skills_list = [
    "python",
    "sql",
    "power bi",
    "tableau",
    "machine learning",
    "excel",
    "pandas",
    "numpy",
    "data analysis"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skills in skills_list:
        if skills in text:
            found_skills.append(skills)

    return found_skills


def missing_skills(resume_skills, job_description):

    jd_skills = extract_skills(job_description)

    missing = []

    for skills in jd_skills:
        if skills not in resume_skills:
            missing.append(skills)

    return missing
