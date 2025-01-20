import streamlit as st
import PyPDF2
import speech_recognition as sr
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from job_roles import job_roles  # Import the job roles

# Load the environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment
groq_api_key = os.getenv('GROQ_API_KEY')

# Initialize the ChatGroq model with the API key
if groq_api_key:
    model = ChatGroq(groq_api_key=groq_api_key)
else:
    st.error("GROQ API key is missing. Please make sure it's in the .env file.")


# Function to extract text from PDF resume
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Function to recognize speech input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please speak now...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I did not understand that."
    except sr.RequestError as e:
        return f"Speech Recognition error; {e}"


# Define the Streamlit app structure
st.title("Resume Q&A for Job Interviews")

# Create session state variables to manage the interview process
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "questions" not in st.session_state:
    st.session_state.questions = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Show initial fields if interview hasn't started
if not st.session_state.interview_started:
    st.header("Step 1: Upload Your Resume")
    uploaded_file = st.file_uploader("Upload your resume in PDF format", type="pdf")

    st.header("Step 2: Select Your Desired Job Role")
    job_role = st.selectbox("Select your desired job role", job_roles)

    st.header("Step 3: Choose Input Method")
    input_method = st.radio("Would you prefer text input or speech?", ("Text", "Speech"))

    start_interview = st.button("Start Interview")

    if start_interview and uploaded_file and job_role:
        st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
        st.session_state.job_role = job_role
        st.session_state.input_method = input_method
        st.session_state.interview_started = True

        # Generate the initial prompt to get questions for the interview
        prompt = PromptTemplate(
            template="You are a job interviewer for a {job_role}. The candidate's resume is as follows:\n\n{resume_text}\n\nAsk relevant interview questions one by one.",
            input_variables=["job_role", "resume_text"])
        formatted_prompt = prompt.format(job_role=job_role, resume_text=st.session_state.resume_text)

        # Generate a list of interview questions
        interview_questions = model.predict(formatted_prompt).split('\n')
        st.session_state.questions = [q for q in interview_questions if q]
        st.session_state.question_index = 0

    # Hide the initial fields and show the first question
    if st.session_state.interview_started:
        st.experimental_rerun()

# Display interview questions and handle responses
if st.session_state.interview_started:
    st.header("Interview in Progress")

    if st.session_state.question_index < len(st.session_state.questions):
        current_question = st.session_state.questions[st.session_state.question_index]
        st.write(f"### Interviewer: {current_question}")

        # Display the input fields based on the selected input method
        if st.session_state.input_method == "Text":
            user_answer = st.text_area("Your Answer:", key="user_answer_text")
        else:
            if st.button("Start Voice Input"):
                user_answer = recognize_speech()
                st.write(f"Your Answer: {user_answer}")
                st.session_state.user_answer = user_answer

        # Submit button to capture user input
        if st.button("Submit"):
            if st.session_state.input_method == "Text":
                st.session_state.user_answer = user_answer
            st.session_state.feedback = model.predict(
                f"Provide feedback on the following response (keep it short and under 100 words): {st.session_state.user_answer}")

            st.write(f"### Feedback: {st.session_state.feedback}")

            st.session_state.question_index += 1
            st.session_state.user_answer = ""  # Clear the answer field

            # If there are more questions, rerun to show the next question
            if st.session_state.question_index < len(st.session_state.questions):
                st.experimental_rerun()
            else:
                st.write("### You have answered all the questions!")
                st.session_state.interview_started = False
                st.session_state.question_index = 0
                st.session_state.questions = []
                st.session_state.resume_text = ""
                if st.button("Restart Interview"):
                    st.session_state.interview_started = False
                    st.session_state.question_index = 0
                    st.session_state.questions = []
                    st.session_state.resume_text = ""
                    st.experimental_rerun()

    else:
        st.write("### Interview Finished!")
        st.session_state.interview_started = False

    if st.button("End Interview"):
        st.session_state.interview_started = False
        st.session_state.question_index = 0
        st.session_state.questions = []
        st.session_state.resume_text = ""
        st.write("### The interview has been ended.")

# Restart button to refresh the app
if not st.session_state.interview_started:
    if st.button("Restart Interview"):
        st.session_state.interview_started = False
        st.session_state.question_index = 0
        st.session_state.questions = []
        st.session_state.resume_text = ""
        st.experimental_rerun()





