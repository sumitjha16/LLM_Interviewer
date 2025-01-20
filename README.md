# Resume Q&A for Job Interviews

An interactive Streamlit application designed to help job seekers prepare for interviews. The app uses advanced AI to generate tailored interview questions based on the candidate's uploaded resume and desired job role. Users can respond using either text or voice input, and the app provides instant feedback on their answers.

---

## Features

- **Resume Parsing**: Extracts and analyzes text from uploaded PDF resumes.
- **Job-Specific Questions**: Generates tailored interview questions based on the selected job role and resume content.
- **Multiple Input Methods**: Supports both text and voice-based answers.
- **Instant Feedback**: Provides concise feedback on user responses to help improve performance.
- **User-Friendly Interface**: Built with Streamlit for an intuitive and interactive user experience.

---

## Technology Stack

- **Python Libraries**:
  - `Streamlit`: For building the web application.
  - `PyPDF2`: For extracting text from PDF resumes.
  - `speech_recognition`: For capturing and processing voice input.
  - `langchain_groq`: For generating interview questions and providing feedback.
  - `dotenv`: For securely managing API keys and environment variables.
- **Other Tools**:
  - **ChatGroq**: An AI model for generating questions and feedback.
  - **Docker**: For deployment and portability.

---

## How It Works

1. **Upload Resume**: Users upload their resume in PDF format.
2. **Select Job Role**: Choose a desired job role from a predefined list.
3. **Start Interview**: The app generates and displays relevant interview questions one by one.
4. **Answer Questions**: Users can provide answers via text or voice input.
5. **Get Feedback**: The app provides instant feedback on user responses.
6. **Complete the Interview**: After all questions are answered, the interview session concludes.

---

## Installation

### Prerequisites
- Python 3.8+
- `pip` package manager
- Environment file (`.env`) containing the following:
