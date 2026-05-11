import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


def generate_interview_questions(
    resume_text,
    job_description
):

    prompt = f"""

    You are an AI Technical Interviewer.

    Based on the resume and job description,
    generate:

    1. SQL Interview Questions
    2. Python Interview Questions
    3. Project-Based Questions
    4. Behavioral Questions

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    """

    response = model.generate_content(prompt)

    return response.text
