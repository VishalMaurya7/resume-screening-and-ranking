import os
import streamlit as st
import pdf2image
from pdf2image.exceptions import PDFInfoNotInstalledError
import io
import json
import base64
import google.generativeai as genai
from dotenv import load_dotenv
import tempfile
import subprocess

# --- Streamlit App Setup (MUST BE FIRST) ---
st.set_page_config(page_title="AI-powered Resume Screening and Ranking System")

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI with the API key from .env
genai.configure(api_key=os.getenv('API_KEY'))

# --- Helper Functions ---

def check_poppler_installed():
    """Checks if Poppler is installed and accessible."""
    try:
        subprocess.run(["pdfinfo", "-v"], capture_output=True, check=True, text=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

# --- Cached Functions ---

@st.cache_data()
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if isinstance(pdf_content, list):
        response = model.generate_content([input, pdf_content[0], prompt])
    else:
        response = model.generate_content([input, prompt])
    return response.text

@st.cache_data()
def get_gemini_response_keywords(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if isinstance(pdf_content, list):
        response = model.generate_content([input, pdf_content[0], prompt])
    else:
        response = model.generate_content([input, prompt])
    
    try:
        # Attempt to find the JSON part within the response
        start_index = response.text.find('{')
        end_index = response.text.rfind('}')
        
        if start_index != -1 and end_index != -1 and end_index > start_index:
            json_string = response.text[start_index:end_index+1]
            return json.loads(json_string)
        else:
            st.warning("Could not find valid JSON in Gemini's response. Returning an empty dictionary.")
            return {}
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response: {e}")
        st.error(f"Raw response text: {response.text}")
        return {}

@st.cache_data()
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        if not check_poppler_installed():
            raise PDFInfoNotInstalledError("Poppler is not installed or not in PATH. Please install it and add it to your PATH.")
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            images = pdf2image.convert_from_path(temp_file_path)

            os.remove(temp_file_path)

            first_page = images[0]
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()
                }
            ]
            return pdf_parts
        except PDFInfoNotInstalledError as e:
            st.error(f"Poppler Error: {e}")
            raise
        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")
            raise
    else:
        raise FileNotFoundError("No file uploaded")

# --- Functions for Screening and Ranking ---

def calculate_resume_score(resume_keywords, job_description_keywords):
    """Calculates a score based on keyword overlap."""
    if not job_description_keywords:
        return 0
    
    common_keywords = set(resume_keywords) & set(job_description_keywords)
    
    # Improved scoring: Consider both recall and precision
    recall = len(common_keywords) / len(job_description_keywords) if job_description_keywords else 0
    precision = len(common_keywords) / len(resume_keywords) if resume_keywords else 0
    
    # Combine recall and precision using the F1-score formula (harmonic mean)
    if recall + precision == 0:
        score = 0
    else:
        score = 2 * (precision * recall) / (precision + recall)
    
    return score * 100

def get_resume_keywords(pdf_content, prompt):
    """Extracts keywords from the resume using Gemini."""
    response = get_gemini_response_keywords(prompt, pdf_content, "")
    if response:
        all_keywords = []
        for key in response:
            all_keywords.extend(response[key])
        return all_keywords
    return []

def rank_resumes(resume_scores):
    """Ranks resumes based on their scores."""
    ranked_resumes = sorted(resume_scores.items(), key=lambda item: item[1], reverse=True)
    return ranked_resumes

# --- Streamlit App ---

st.header("AI-powered Resume Screening and Ranking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_files = st.file_uploader("Upload your resumes(PDF)...", type=["pdf"], accept_multiple_files=True)

if 'resumes' not in st.session_state:
    st.session_state.resumes = []

if uploaded_files:
    st.write(f"{len(uploaded_files)} PDFs Uploaded Successfully")
    st.session_state.resumes = uploaded_files

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    submit1 = st.button("Tell Me About the Resume")

with col2:
    submit2 = st.button("Get Keywords")

with col3:
    submit3 = st.button("Percentage match")
    
with col4:
    submit4 = st.button("Rank Resumes")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
As an expert ATS (Applicant Tracking System) scanner with an in-depth understanding of AI and ATS functionality, 
your task is to evaluate a resume against a provided job description. Please identify the specific skills and keywords 
necessary to maximize the impact of the resume and provide response in json format as {Technical Skills:[], Analytical Skills:[], Soft Skills:[]}.

Note: Please do not make up the answer, only answer from the job description provided.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt_resume_keywords = """
As an expert ATS (Applicant Tracking System) scanner, extract all the keywords from the resume.
Return the keywords in json format as {Technical Skills:[], Analytical Skills:[], Soft Skills:[]}.
"""

if submit1:
    if st.session_state.resumes:
        for resume in st.session_state.resumes:
            try:
                pdf_content = input_pdf_setup(resume)
                response = get_gemini_response(input_prompt1, pdf_content, input_text)
                st.subheader(f"The Response for {resume.name} is")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.write("Please upload the resume")

elif submit2:
    if st.session_state.resumes:
        for resume in st.session_state.resumes:
            try:
                pdf_content = input_pdf_setup(resume)
                response = get_gemini_response_keywords(input_prompt2, pdf_content, input_text)
                st.subheader(f"Skills for {resume.name} are:")
                if response:
                    st.write(f"Technical Skills: {', '.join(response.get('Technical Skills', []))}.")
                    st.write(f"Analytical Skills: {', '.join(response.get('Analytical Skills', []))}.")
                    st.write(f"Soft Skills: {', '.join(response.get('Soft Skills', []))}.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.write("Please upload the resume")

elif submit3:
    if st.session_state.resumes:
        for resume in st.session_state.resumes:
            try:
                pdf_content = input_pdf_setup(resume)
                response = get_gemini_response(input_prompt3, pdf_content, input_text)
                st.subheader(f"The Response for {resume.name} is")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.write("Please upload the resume")

elif submit4:
    if st.session_state.resumes:
        try:
            job_description_keywords = get_gemini_response_keywords(input_prompt2, input_text, input_text)
            if job_description_keywords is None:
                st.error("Could not extract keywords from job description.")
            else:
                job_description_all_keywords = []
                for key in job_description_keywords:
                    job_description_all_keywords.extend(job_description_keywords[key])
                resume_scores = {}
                for resume in st.session_state.resumes:
                    pdf_content = input_pdf_setup(resume)
                    resume_keywords = get_resume_keywords(pdf_content, input_prompt_resume_keywords)
                    score = calculate_resume_score(resume_keywords, job_description_all_keywords)
                    resume_scores[resume.name] = score

                ranked_resumes = rank_resumes(resume_scores)

                st.subheader("Resume Ranking:")
                for rank, (resume_name, score) in enumerate(ranked_resumes):
                    st.write(f"**Rank {rank + 1}:** {resume_name} - Score: {score:.2f}%")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.write("Please upload the resumes")
