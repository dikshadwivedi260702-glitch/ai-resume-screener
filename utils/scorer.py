import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

# --- Common tech skills list for extraction ---
SKILLS_DB = [
    "python", "java", "sql", "machine learning", "deep learning",
    "data analysis", "pandas", "numpy", "tensorflow", "keras",
    "scikit-learn", "nlp", "flask", "django", "react", "javascript",
    "html", "css", "git", "docker", "aws", "power bi", "tableau",
    "excel", "communication", "leadership", "teamwork", "problem solving"
]

def extract_skills(text):
    """
    Extracts skills found in text by matching against SKILLS_DB.
    """
    text_lower = text.lower()
    found_skills = [skill for skill in SKILLS_DB if skill in text_lower]
    return list(set(found_skills))


def get_match_score(job_description, resume_text):
    """
    Uses TF-IDF + Cosine Similarity to compute match score.
    Returns a score between 0 and 100.
    """
    documents = [job_description, resume_text]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)


def get_keyword_gap(job_description, resume_text):
    """
    Finds skills in JD that are MISSING from the resume.
    """
    jd_skills = set(extract_skills(job_description))
    resume_skills = set(extract_skills(resume_text))
    missing = jd_skills - resume_skills
    return list(missing)


def rank_resumes(job_description, resumes_dict):
    """
    Ranks multiple resumes against a job description.
    
    resumes_dict = { "filename": "resume_text", ... }
    Returns sorted list of results.
    """
    results = []

    for filename, resume_text in resumes_dict.items():
        score = get_match_score(job_description, resume_text)
        matched_skills = extract_skills(resume_text)
        missing_skills = get_keyword_gap(job_description, resume_text)

        results.append({
            "Resume": filename,
            "Match Score (%)": score,
            "Matched Skills": ", ".join(matched_skills) if matched_skills else "None",
            "Missing Skills": ", ".join(missing_skills) if missing_skills else "None"
        })

    # Sort by score descending
    results = sorted(results, key=lambda x: x["Match Score (%)"], reverse=True)

    # Add rank
    for i, r in enumerate(results):
        r["Rank"] = i + 1

    return results