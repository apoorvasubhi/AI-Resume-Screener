import streamlit as st
import pandas as pd
import plotly.express as px

from utils.parser import extract_text_from_pdf
from utils.skills import extract_skills, missing_skills
from utils.scorer import calculate_match_score
from utils.ai_feedback import generate_feedback
from utils.interview_questions import generate_interview_questions

st.set_page_config(
    page_title="AI Resume Screening System",
    layout="wide"
)

st.title("AI-Powered Resume Screening & Candidate Ranking System")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    resume_files = st.file_uploader(
        "Upload Resume PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

with col2:

    job_description = st.text_area(
        "Paste Job Description"
    )

# MAIN LOGIC
if resume_files and job_description:

    results = []

    for resume_file in resume_files:

        # Extract resume text
        resume_text = extract_text_from_pdf(resume_file)

        # Extract skills
        skills = extract_skills(resume_text)

        # Calculate ATS score
        score = calculate_match_score(
            resume_text,
            job_description
        )

        # Find missing skills
        missing = missing_skills(
            skills,
            job_description
        )

        # Store results
        results.append({
            "Candidate": resume_file.name,
            "ATS Score": score,
            "Skills Found": len(skills),
            "Missing Skills": len(missing)
        })

    # Create dataframe
    df = pd.DataFrame(results)

    # Sort by ATS Score
    df = df.sort_values(
        by="ATS Score",
        ascending=False
    )

    # Add Rank Column
    df["Rank"] = range(1, len(df) + 1)

    st.markdown("---")

    st.subheader("Candidate Rankings")

    st.dataframe(df)

    # Top Candidate
    top_candidate = df.iloc[0]

    st.success(
        f"Top Candidate: {top_candidate['Candidate']} "
        f"with ATS Score {top_candidate['ATS Score']}%"
    )

    # Pie Chart
    chart_data = {
        "Category": ["Skills Found", "Missing Skills"],
        "Count": [
            int(df["Skills Found"].sum()),
            int(df["Missing Skills"].sum())
        ]
    }

    fig = px.pie(
        chart_data,
        names="Category",
        values="Count",
        title="Overall Skills Analysis"
    )

    st.plotly_chart(fig)

    # Download CSV
    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Rankings CSV",
        data=csv,
        file_name="candidate_rankings.csv",
        mime="text/csv"
    )

    # AI Feedback Section
    st.markdown("---")

    selected_candidate = st.selectbox(
        "Select Candidate for AI Review",
        df["Candidate"]
    )

    if st.button("Generate AI Feedback"):

        selected_resume = None

        for resume_file in resume_files:

            if resume_file.name == selected_candidate:

                selected_resume = resume_file

                break

        if selected_resume:

            resume_text = extract_text_from_pdf(selected_resume)

            with st.spinner("Generating AI Feedback..."):

                feedback = generate_feedback(
                    resume_text,
                    job_description
                )

                st.subheader("AI Resume Review")

                st.write(feedback)

    st.markdown("---")

    st.subheader("AI Interview Question Generator")

    if st.button("Generate Interview Question"):

        selected_resume = None

        for resume_file in resume_files:

            if resume_file.name == selected_candidate:

                selected_resume = resume_file

                break

        if selected_resume:

            resume_text = extract_text_from_pdf(selected_resume)

            with st.spinner("Generating Interview Questions..."):

                questions = generate_interview_questions(
                    resume_text,
                    job_description
                )

            st.subheader(
                "Generated Interview Questions"
            )

            st.write(questions)
