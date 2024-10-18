import streamlit as st
import PyPDF2
from backend import qa_pipeline
from codes.csv import read_csv
from codes.ppt import read_ppt
from codes.doc import read_doc

# App Title
st.markdown("<h2 style='text-align: center;'>InsightBot🤖</h2>", unsafe_allow_html=True)  
st.markdown("<h2 style='text-align: center;'>Welcome Buddy👋</h2>", unsafe_allow_html=True)  # Centered welcome message

# File uploader
uploaded_file = st.file_uploader("Upload a document📃", type=["pdf", "txt", "csv", "pptx", "docx"])

# Initialize session state
if 'question_list' not in st.session_state:
    st.session_state.question_list = []  # List to hold (question, answer) pairs
if 'current_question' not in st.session_state:
    st.session_state.current_question = ""  # To reset the question input field

# Create a single input field for the current question at the top
question = st.text_input("Ask a question based on the uploaded document💭", value=st.session_state.current_question)

# Create a submit button
if st.button("Submit"):
    if question:  # Only process if there is a question
        # Process the uploaded document and get the answer
        if uploaded_file is not None:
            document_text = ""

            # Check file type
            if uploaded_file.type == "application/pdf":
                # Read PDF file
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    document_text += page.extract_text() + "\n"

            elif uploaded_file.type == "text/plain":
                # Read TXT file
                document_text = uploaded_file.read().decode("utf-8")

            elif uploaded_file.type == "text/csv":
                # Read CSV file
                document_text = read_csv(uploaded_file)

            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
                # Read PPTX file
                document_text = read_ppt(uploaded_file)

            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                # Read DOCX file
                document_text = read_doc(uploaded_file)

            st.success("Great, You uploaded successfully")  # Success message after upload
            
            # Get the answer
            answer = qa_pipeline(document_text, question)

            # Store the question and answer in session state
            st.session_state.question_list.append((question, answer))

            # Clear the input field by updating the session state variable
            st.session_state.current_question = ""  # Reset the session state variable after submission

# Display all previous questions and answers in a chat-style format
for i, (q, a) in enumerate(st.session_state.question_list):
    col1, col2 = st.columns([1, 1])  # Two equal columns

    with col2:
        st.markdown(f"<div style='background-color: black;border: 2px solid white; color: white; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>**Q{i+1}: {q}**</div>", unsafe_allow_html=True)  # Question
    
    with col1:
        st.markdown(f"<div style='background-color: white;border: 2px solid black; color: black; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>A{i+1}: {a}</div>", unsafe_allow_html=True)  # Answer
