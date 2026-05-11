import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


def generate_feedback(
    resume_text,
    job_description
):

    prompt = f"""

    You are an AI Resume Reviewer.

    Analyze the resume against the job description.

    Provide:
    1. Strengths
    2. Missing Skills
    3. Improvement Suggestions
    4. Hiring Recommendation

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """

    response = model.generate_content(prompt)

    return response.text
