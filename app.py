import streamlit as st
import pandas as pd
from utils.extractor import extract_text_from_pdf
from utils.preprocessor import clean_text
from utils.scorer import rank_resumes

# --- Page Config ---
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

# --- Header ---
st.title("📄 AI-Powered Resume Screener")
st.markdown("Upload resumes and a job description to automatically rank candidates.")
st.divider()

# --- Layout: Two columns ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Paste the job description here:",
        height=300,
        placeholder="e.g. We are looking for a Python developer with experience in ML, SQL, and Flask..."
    )

with col2:
    st.subheader("📁 Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload PDF resumes (multiple allowed)",
        type=["pdf"],
        accept_multiple_files=True
    )

st.divider()

# --- Run Button ---
if st.button("🚀 Screen Resumes", use_container_width=True):

    # Validation
    if not job_description.strip():
        st.error("⚠️ Please enter a job description.")
    elif not uploaded_files:
        st.error("⚠️ Please upload at least one resume.")
    else:
        with st.spinner("Analyzing resumes..."):

            # Extract and clean text from each resume
            resumes_dict = {}
            for file in uploaded_files:
                raw_text = extract_text_from_pdf(file)
                clean = clean_text(raw_text)
                resumes_dict[file.name] = clean

            # Clean job description too
            clean_jd = clean_text(job_description)

            # Rank resumes
            results = rank_resumes(clean_jd, resumes_dict)

        # --- Results ---
        st.success("✅ Screening complete!")
        st.subheader("🏆 Candidate Rankings")

        df = pd.DataFrame(results)
        df = df[["Rank", "Resume", "Match Score (%)", "Matched Skills", "Missing Skills"]]

        # Color code scores
        st.dataframe(
            df.style.background_gradient(subset=["Match Score (%)"], cmap="RdYlGn"),
            use_container_width=True
        )

        # --- Top Candidate Highlight ---
        st.subheader("🥇 Top Candidate")
        top = results[0]
        st.info(f"**{top['Resume']}** with a match score of **{top['Match Score (%)']}%**")

        # --- Download Results ---
        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Results as CSV",
            data=csv,
            file_name="screening_results.csv",
            mime="text/csv"
        )