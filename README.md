# resume-screening-and-ranking
# AI-Powered Resume Screening and Ranking System

This project is an AI-powered application designed to streamline the resume screening process. It leverages Google's Gemini AI model to analyze resumes against job descriptions, extract relevant keywords, calculate match percentages, and rank candidates.

## Features

*   **Resume Upload:** Upload multiple resumes in PDF format.
*   **Job Description Input:** Input the job description for the role you're hiring for.
*   **AI-Powered Analysis:** Utilizes Google's Gemini AI to:
    *   Evaluate resumes against the job description.
    *   Extract key technical, analytical, and soft skills.
    *   Calculate a percentage match between the resume and job description.
    *   Provide a professional evaluation of the candidate's profile.
*   **Resume Ranking:** Ranks uploaded resumes based on their match scores.
*   **User-Friendly Interface:** Built with Streamlit for an intuitive web application experience.

## Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python 3.8+:**  The project is built using Python. You can check your Python version by running `python --version` or `python3 --version` in your terminal.
2.  **Poppler:** This is a PDF rendering library required for `pdf2image`.
    *   **Windows:**
        *   Download Poppler from https://github.com/oschwartz10612/poppler-windows/releases.
        *   Extract the downloaded zip file.
        *   Add the `bin` folder within the extracted Poppler directory to your system's `PATH` environment variable.
    *   **macOS:**
        *   Install using Homebrew: `brew install poppler`
    *   **Linux (Debian/Ubuntu):**
        *   Install using apt: `sudo apt-get update && sudo apt-get install -y poppler-utils`
3.  **Google Gemini API Key:**
    *   You'll need a Google Gemini API key to use the AI features.
    *   Get an API key from https://makersuite.google.com/app/apikey.
4.  **Git:** To clone the repository.

## Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
    Replace `<repository_url>` with the actual URL of your GitHub repository and `<repository_directory>` with the name of the directory.

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv  # Or python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    If you don't have a `requirements.txt` file, you can create one by running `pip freeze > requirements.txt` after installing the packages.

5.  **Create a `.env` File:**
    *   In the root directory of the project, create a file named `.env`.
    *   Add your Google Gemini API key to this file:
        ```
        API_KEY=YOUR_GEMINI_API_KEY
        ```
        Replace `YOUR_GEMINI_API_KEY` with your actual API key.

## Running the Application

1.  **Navigate to the Project Directory:**
    ```bash
    cd <repository_directory>
    ```
2.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```
    Or
    ```bash
    streamlit run Pro1.py
    ```
    (depending on which file is the main one)

3.  **Access the App:**
    *   Your web browser will automatically open the Streamlit app, usually at `http://localhost:8501`.

## Usage

1.  **Enter Job Description:** Paste the job description into the "Job Description" text area.
2.  **Upload Resumes:** Upload one or more PDF resumes using the file uploader.
3.  **Choose an Action:**
    *   **Tell Me About the Resume:** Get a detailed evaluation of each resume against the job description.
    *   **Get Keywords:** Extract key technical, analytical, and soft skills from the job description.
    *   **Percentage Match:** Calculate the percentage match between each resume and the job description.
    *   **Rank Resumes:** Rank the uploaded resumes based on their match scores.
4. **View Results:** The results will be displayed on the Streamlit app.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them.
4.  Push your changes to your forked repository.
5.  Submit a pull request.

## License

[Add your license information here, e.g., MIT License]
